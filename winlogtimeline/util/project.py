import os
import sqlite3 as sql
from datetime import datetime

from .data import get_package_data_path


class Project:
    def __init__(self, project_directory):
        """
        :param project_directory: The path to a project directory.
        """
        # Create the project directory if it doesn't exist.
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)

        # Set up the directory structure
        self._path = project_directory
        self._log_file = 'logs.sqlite'
        self._log_path = os.path.join(self._path, self._log_file)
        self._config_file = 'somefile.extension'
        self._config_path = os.path.join(self._path, self._config_file)

        # Create a database connection
        self._conn = sql.connect(self._log_path)
        schema_file = get_package_data_path(__file__, *('config/schema.sql'.split('/')))

        # Set up the database if not exists
        with open(schema_file) as schema:
            self._conn.executescript(schema.read())
            self._conn.commit()

        # Load the project config
        self._config = None

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

    def write_log_data(self, log):
        """
        Writes log data to the project as long as it is not a duplicate.
        :param log: The log to write, in the format returned by winlogtimeline.util.logs.parse_record.
        :return: None
        """
        if not self.is_duplicate(log):
            query = ('INSERT INTO logs '
                     '(timestamp_utc, timestamp_local, timestamp_tz, event_id, description, details, event_source,'
                     ' event_log, session_id, account, computer_name, record_number, recovered, source_file_hash) '
                     'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
            # TODO: remove test values on the next line
            values = (
                datetime.utcnow(), datetime.utcnow(), 0, 1111, 'Test', 'This is a test', 'Test Source', 'Test Log', 0,
                'Test User', 'Computer', 0, False, '1FC1FC')
            self._conn.execute(query, values)

    def write_verification_data(self, file_hash, log_file):
        """
        Used to store data for verifying the integrity of the data source.
        :param file_hash:
        :param log_file:
        :return: None
        """
        time = datetime.utcnow()

        cursor = self._conn.cursor()
        query = 'INSERT INTO source_files (file_name, hash, import_timestamp) VALUES (?, ?, ?)'
        values = (log_file, file_hash, time)

        cursor.execute(query, values)

    def get_all_logs(self):
        """
        :return: A list of all logs in project storage.
        """
        keys = (
            'timestamp_utc',
            'timestamp_local',
            'timestamp_tz',
            'event_id',
            'description',
            'details',
            'event_source',
            'event_log',
            'session_id',
            'account',
            'computer_name',
            'record_number',
            'recovered',
            'source_file_hash'
        )

        cursor = self._conn.cursor()
        query = 'SELECT * FROM logs'
        cursor.execute(query)
        rows = cursor.fetchall()

        # Convert the rows to an easy to use storage format. This should be changed once consensus is formed.
        logs = [dict(zip(keys, row)) for row in rows]

        return logs

    def is_duplicate(self, log):
        """

        :return:
        """
        # TODO: implement and document
        return False
