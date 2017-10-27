import xmltodict
from xml.parsers.expat import ExpatError
from time import time
import pyevtx
from winlogtimeline.util.logs import Record


# Note: It may be useful to take config out of this whole equation. Config could store the default filter configuration,
# and that could be copied into the project config to allow user modifications.
def import_log(log_file, project, config, status_callback):
    """
    Main routine to import an event log file.
    :param log_file: A path to an event log file.
    :param project: A project instance.
    :param config: A config dictionary.
    :param status_callback: A function to relay status info the the GUI. Should accept status as a string.
    :return: None
    """

    status_callback('Parsing file...')
    start = time()
    log = pyevtx.open(log_file)
    records = collect_records(log)  # + collect_deleted_records(log)
    xml_records = xml_convert(records)
    i = 0
    for record in xml_records:
        project.write_log_data(Record(**record))
        i += 1
    stop = time()

    taken = stop - start

    status_callback('Loaded {} records in {:0.3f} seconds.'.format(i, taken))


def xml_convert(records):
    for record in records:
        try:
            d = xmltodict.parse(record)
        except ExpatError:
            record = record.replace("\x00", "")  # This can not be the best way to do this...
            d = xmltodict.parse(record)
        sys = d['Event']['System']

        yield {
            'timestamp_utc': sys['TimeCreated']['@SystemTime'],
            'event_id': sys['EventID'],
            'description': '',
            'details': '',
            'event_source': sys['Provider']['@Name'],
            'event_log': sys['Channel'],
            'session_id': '',
            'account': '',
            'computer_name': sys['Computer'],
            'record_number': sys['EventRecordID'],
            'recovered': False,
            'source_file_hash': ''
        }


def collect_records(event_file):
    """
    :param event_file: An event log object.
    :return: A list of event records in the format returned by libevtx-python.
    """
    for i in range(event_file.get_number_of_records()):
        yield event_file.get_record(i).xml_string


def collect_deleted_records(event_file):
    """
    :param event_file: An event log object.
    :return: A list of deleted event records in the format returned by libevtx-python.
    """
    pass


def get_machine_name(records):
    """
    Parses a log file to determine the machine it originated from.
    :param event_file: An event log object.
    :return: A unique identifier for the machine.
    """
    # TODO: determine a unique identifier for machines that can be pulled from the event logs.

    return ''


def filter_logs(logs, project, config):
    """
    When given a list of log objects, returns only those that match the filters defined in config and project. The
    filters in project take priority over config.
    :param logs: A list of log objects. Logs must be in the format returned by winlogtimeline.util.logs.parse_record.
    :param project: A project instance.
    :param config: A config dictionary.
    :return: A list of logs that satisfy the filters specified in the configuration.
    """
    return logs


def get_log_file_hash(log_file):
    """
    :param log_file: A path to an event log file.
    :return: The hash of the event log file.
    """
    # TODO: discuss which algorithm to use for hashing.
    return ''
