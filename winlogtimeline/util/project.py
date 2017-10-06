class Project:
    def __init__(self, project_directory):
        """
        :param project_directory: The path to a project directory.
        """
        self.path = project_directory
        self.config = {}
        self.log_file = 'logs.sqlite'

        self.conn = None  # TODO: implement sqlite db for log storage.

    def save(self):
        """
        Writes changes to the database and project configuration file.
        :return: None
        """
        pass

    def close(self):
        """
        Closes any open file objects.
        :return: None
        """
        pass

    def write_log_data(self, log):
        """
        Writes log dat to the project as long as it is not a duplicate.
        :param log: The log to write, in the format returned by winlogtimeline.util.logs.parse_record.
        :return: None
        """
        pass

    def write_verification_data(self, file_hash, log_file):
        """
        Used to store data for verifying the integrity of the data source.
        :param file_hash:
        :param log_file:
        :return: None
        """
        pass

    def get_all_logs(self):
        """
        :return: A list of all logs in project storage.
        """
        pass
