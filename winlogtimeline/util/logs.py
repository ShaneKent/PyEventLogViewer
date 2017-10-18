import hashlib

class Record:
    def __init__(self, **kwargs):
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
        self.source_file_hash = kwargs['source_file_hash']
        self.record_hash = self.__hash__()


    # get unique id function that returns unique id for each log
    # __hash__ function (override)
    # timestamp_utc, event_id, description, computer name, event source, event log
    def __key__(self):
        key_string = ""
        key_string += self.timestamp_utc
        key_string += self.event_id
        key_string += self.description
        key_string += self.computer_name
        key_string += self.event_source
        key_string += self.event_log
        return key_string


    def __hash__(self):
        return hashlib.md5(bytes(self.__key__(),'utf-8')).hexdigest()


def parse_record(record, machine):
    """
    Takes a record as returned by libevtx-python and returns a dictionary representing the relevant log fields.
    :param record: A record object from libevtx-python.
    :param machine: The machine that the record was pulled from.
    :return: A dictionary containing the relevant log data.
    """
    pass


def sort_logs(logs, property, ascending=True):
    """
    :param logs: A list of event logs.
    :param property: The property to sort by.
    :param ascending: Whether to sort ascending or descending.
    :return: A sorted list of event logs.
    """
    return logs
