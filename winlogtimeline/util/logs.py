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