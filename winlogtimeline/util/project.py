import os
import sqlite3 as sql
from datetime import datetime

from .data import get_package_data_path
from .logs import Record


class Project:
    def __init__(self, project_file):
        """
        Creates a new instance of a project. If an error occurs in creating/opening the project files. If successful,
        self.exception will be None. Otherwise, the instance should be discarded.
        :param project_file: The path to a .elv file.
        """
        self.exception = None
        try:
            # Create the project directory if it doesn't exist.
            project_directory = os.path.dirname(project_file)
            if not os.path.exists(project_directory):
                os.makedirs(project_directory)

            # Create the project file if it doesn't exist
            open(project_file, 'a').close()

            # Set up the directory structure
            self._path = project_directory
            self._log_file = 'logs.sqlite'
            self._log_path = os.path.join(self._path, self._log_file)
            self._config_file = os.path.basename(project_file)
            self._config_path = project_file

            # Create a database connection
            self._conn = sql.connect(self._log_path, check_same_thread=False)
            schema_file = get_package_data_path(__file__, *('config/schema.sql'.split('/')))

            # Set up the database if not exists
            with open(schema_file) as schema:
                self._conn.executescript(schema.read())
                self._conn.commit()

            # Fetch the column names
            self._columns = [col_info[1] for col_info in self._conn.execute('PRAGMA table_info(logs);')]

            # Load the project config
            self._config = None
        except Exception as e:
            self.exception = e

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

        # Close the configuration
        # TODO: review whether the configuration file needs an open file descriptor at all times. If not, the file can
        # be opened and closed during read/save, and nothing needs to be done here apart from deleting this comment.

    def write_log_data(self, record):
        """
        Writes log data to the project as long as it is not a duplicate.
        :param record: A Record object.
        :return: None
        """

        if not self.is_duplicate(record):
            query = ('INSERT INTO logs '
                     '(timestamp_utc, event_id, description, details, event_source, event_log, session_id, account,'
                     ' computer_name, record_number, recovered, record_hash, source_file_hash) '
                     'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
            values = (
                record.timestamp_utc, record.event_id, record.description, record.details, record.event_source,
                record.event_log, record.session_id, record.account, record.computer_name, record.record_number,
                record.recovered, record.record_hash, record.source_file_hash
            )
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
        query = 'SELECT * FROM logs'
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

    def is_duplicate(self, record):
        """

        :return:
        """
        # TODO: implement and document
        return False
