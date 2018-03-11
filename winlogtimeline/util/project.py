import json
import os
import sqlite3 as sql
from datetime import datetime

from .data import get_package_data_path, open_config
from .logs import Record


class Project:
    def __init__(self, project_file_path):
        """
        Creates a new instance of a project. If an error occurs in creating/opening the project files. If successful,
        self.exception will be None. Otherwise, the instance should be discarded.
        :param project_file_path: The path to a .elv file.
        """
        self.exception = None
        try:
            # Create the project directory if it doesn't exist.
            project_directory = os.path.dirname(project_file_path)
            if not os.path.exists(project_directory):
                os.makedirs(project_directory)

            # Set up the directory structure
            self._path = project_directory
            self._file_name = os.path.basename(self._path)
            self._log_file = f'{self._file_name}.sqlite'
            self._log_path = os.path.join(self._path, self._log_file)
            self._config_file = os.path.basename(project_file_path)
            self._config_path = project_file_path

            # Create the project file if it doesn't exist
            open(project_file_path, 'a').close()

            # Read config
            with open(project_file_path, 'r') as config:
                data = config.read()
                if not data:
                    self.config = open_config()
                else:
                    self.config = json.loads(data)

            # Create a database connection
            self._conn = sql.connect(self._log_path, check_same_thread=False)
            schema_file = get_package_data_path(__file__, *('config/schema.sql'.split('/')))

            # Set up the database if not exists
            with open(schema_file) as schema:
                self._conn.executescript(schema.read())
                self._conn.commit()

            # Fetch the column names
            self._columns = [col_info[1] for col_info in self._conn.execute('PRAGMA table_info(logs);')]

            # State vars
            if 'state' not in self.config.keys():
                self.config['state'] = dict()
            # Enabled/disabled column state
            if 'columns' not in self.config['state'].keys():
                self.config['state']['columns'] = Record.get_headers()
            if 'timezone_offset' not in self.config['state'].keys():
                self.config['state']['timezone_offset'] = 0

        except Exception as e:
            self.exception = e
            raise e

    def get_path(self):
        """
        Returns the absolute path to the project root.
        :return:
        """
        return os.path.abspath(self._path)

    def save(self):
        """
        Writes changes to the database and project configuration file.
        :return: None
        """
        # Save the log data
        self._conn.commit()

        # Save the configuration
        with open(self._config_path, 'w') as config:
            config.write(json.dumps(self.config))

    def save_as(self):
        """
        Changes the location of the project file and then calls save.
        :return: None
        """
        pass

    def close(self):
        """
        Saves and closes all open file objects.
        :return: None
        """
        # Save any changes
        self.save()

        # Close the log file
        self._conn.close()

    def write_log_data(self, record, xml):
        """
        Writes log data to the project.
        :param record: A Record object.
        :param xml: The raw xml for the record.
        :return: None
        """

        query = ('INSERT INTO logs '
                 '(timestamp_utc, event_id, description, details, event_source, event_log, session_id, account,'
                 ' computer_name, record_number, recovered, record_hash, alias) '
                 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')

        values = (
            record.timestamp_utc, record.event_id, record.description, record.details, record.event_source,
            record.event_log, record.session_id, record.account, record.computer_name, record.record_number,
            record.recovered, record.record_hash, record.source_file_alias
        )
        self._conn.execute(query, values)

        query = ('INSERT INTO raw_xml_data '
                 '(record_hash, raw_xml) '
                 'VALUES (?, ?)')

        values = (record.record_hash, xml)
        self._conn.execute(query, values)

    def write_verification_data(self, file_hash, log_file, alias):
        """
        Used to store data for verifying the integrity of the data source.
        :param file_hash:
        :param log_file:
        :param alias:
        :return: None
        """
        time = datetime.utcnow()

        query = 'INSERT INTO source_files (file_name, hash, import_timestamp, alias) VALUES (?, ?, ?, ?)'
        values = (log_file, file_hash, time, alias)

        self._conn.execute(query, values)

    def get_all_logs(self):
        """
        :return: A list of all logs in project storage.
        """
        offset = self.config['state']['timezone_offset']
        if not isinstance(offset, int) or not (-12 <= offset <= 12):
            self.config['state']['timezone_offset'] = offset = 0

        query = (f'SELECT strftime(\'%Y-%m-%d %H:%M:%f\', timestamp_utc, \'{offset:+d} hours\'), event_id, description,'
                 f' details, event_source, event_log, session_id, account, computer_name, record_number, recovered, '
                 f'alias, record_hash FROM logs')
        rows = self._conn.execute(query).fetchall()

        # Convert the rows to an easy to use storage format. This should be changed once consensus is formed.
        logs = [Record(**dict(zip(self._columns, row))) for row in rows]

        return logs

    def get_alias_names(self):
        """
        :return: A list of all alias names that are stored in the project.
        """
        query = 'SELECT * FROM source_files'
        rows = self._conn.execute(query).fetchall()

        aliases = [row[3] for row in rows]

        return aliases

    def cleanup_import(self, alias):
        """
        Ensures that a failed import is cleaned up correctly.
        :param alias: The alias used for the import.
        :return:
        """
        self._conn.execute('DELETE FROM source_Files WHERE alias=?', (alias,))
        self._conn.execute('DELETE FROM logs WHERE alias=?', (alias,))

    def filter_logs(self, dedup):
        """
        When given a list of log objects, returns only those that match the filters defined in config and project. The
        filters in project take priority over config.
        :param config: A config dictionary.
        :param dedup: Int var specifying deduplication
        :return: A list of logs that satisfy the filters specified in the configuration.
        """
        config = self.config['filters']
        headers = Record.get_headers()

        info = self._conn.execute('PRAGMA table_info(logs);')  # (id, column name, type, not null, pk, auto-inc)
        id, columns, types, n, p, a = zip(*info)

        filters = []

        # col, operator, value, flag = config[0]
        for col, operator, value, flag in config:
            if not flag:
                continue  # Only add active filters

            idx = headers.index(col)
            col = columns[idx]
            datatype = types[idx]  # Data type for this column

            if operator == 'Contains':
                operator = 'like'
                value = "'%" + value + "%'"

            if operator == 'In':
                if datatype == 'INTEGER':
                    values = []
                    for v in value.split(','):
                        v = v.strip()
                        try:
                            int(v)
                            values.append(v)
                        except:
                            continue
                    if len(values) == 0: continue  # No valid values
                    value = ', '.join(values)

                value = "(" + value + ")"  # Add parentheses for sql list
            elif datatype == 'DATETIME':
                value = "'" + value + "'"
                if len(value.split()) == 1:
                    col = 'date(' + col + ')'
            elif datatype == 'INTEGER':
                try:
                    int(value)  # Non-integer values for int type columns are invalid
                except:
                    continue
            filters.append((col, operator, value))

        # Timestamp offset
        offset = self.config['state']['timezone_offset']
        if not isinstance(offset, int) or not (-12 <= offset <= 12):
            self.config['state']['timestamp_offset'] = offset = 0

        query = (f'SELECT strftime(\'%Y-%m-%d %H:%M:%f\', timestamp_utc, \'{offset:+d} hours\'), event_id, description,'
                 f' details, event_source, event_log, session_id, account, computer_name, record_number, recovered, '
                 f'alias, record_hash FROM logs WHERE ')
        query += ' AND'.join('{} {} {}'.format(*constraint) for constraint in filters)
        query = query.rstrip(' WHERE ')
        if dedup.get() != 0:
            query += ' GROUP BY record_hash'

        cur = self._conn.execute(query)
        logs = cur.fetchall()

        logs = [Record(**dict(zip(columns, row))) for row in logs]

        return logs