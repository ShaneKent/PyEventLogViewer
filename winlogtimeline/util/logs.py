import hashlib


class Record:
    def __init__(self, **kwargs):
        # TODO: Remove/limit string casts once log imports are standardized/filtered properly.
        self.timestamp_utc = kwargs['timestamp_utc']
        self.event_id = kwargs['event_id']
        self.description = kwargs['description']
        self.details = kwargs['details']
        self.event_source = kwargs['event_source']
        self.event_log = kwargs['event_log']
        self.session_id = kwargs['session_id']
        self.account = kwargs['account']
        self.computer_name = kwargs['computer_name']
        self.record_number = kwargs['record_number']
        self.recovered = kwargs['recovered']
        self.source_file_alias = kwargs['alias']
        self.record_hash = self.__hash__()

    def get_tuple(self):
        return (
            self.timestamp_utc, self.event_id, self.description, self.details, self.event_source, self.event_log,
            self.session_id, self.account, self.computer_name, self.record_number, self.record_hash,
            self.source_file_alias
        )

    @classmethod
    def get_headers(cls):
        return (
            'Timestamp (UTC)', 'Event ID', 'Description', 'Details', 'Event Source', 'Event Log', 'Session ID',
            'Account', 'Computer Name', 'Record Number', 'Record Hash', 'Source File Alias'
        )

    def __key__(self):
        key_string = ""
        key_string += self.timestamp_utc
        key_string += str(self.event_id)
        key_string += self.description
        key_string += self.computer_name
        key_string += self.event_source
        key_string += self.event_log
        return key_string

    def __hash__(self):
        return hashlib.md5(bytes(self.__key__(), 'utf-8')).hexdigest()


def sort_logs(logs, property, descending=False):
    """
    :param logs: A list of event logs.
    :param property: The property to sort by.
    :param descending: Whether to sort ascending or descending.
    :return: A sorted list of event logs.
    """

    logs = sorted(logs, key=lambda x: getattr(x, property), reverse=descending)

    return logs


def filter_logs(logs, property, keep=True):
    """
    :param logs: A list of event logs.
    :param property: The property to filter by.
    :param keep: Keep or delete records specified by property
    :return: A list of logs that meet the filter conditions
    """
    pass
