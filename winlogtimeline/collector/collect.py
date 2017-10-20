import xmltodict
from time import time
import pyevtx

# Note: It may be useful to take config out of this whole equation. Config could store the default filter configuration,
# and that could be copied into the project config to allow user modifications.
def import_log(log_file, project, config):
    """
    Main routine to import an event log file.
    :param log_file_param: A path to an event log file.
    :param project: A project instance.
    :param config: A config dictionary.
    :return: None
    """

    start = time()
    log = pyevtx.open(log_file)
    records = collect_records(log)  # + collect_deleted_records(log)
    xml_records = xml_convert(records)
    stop = time()

    taken = str(stop - start).split(".")[0]

    return "Finished opening event log file. It took " + taken + " seconds."


def xml_convert(records):
    xmls = []
    for i in range(0, len(records)):
        record = records[i]

        try:
            xmls.append(xmltodict.parse(record))
        except:
            record = record.replace("\x00", "")  # This can not be the best way to do this...
            xmls.append(xmltodict.parse(record))

    return xmls

def collect_records(event_file):
    """
    :param event_file: An event log object.
    :return: A list of event records in the format returned by libevtx-python.
    """

    records = [event_file.get_record(i).xml_string for i in range(0, event_file.get_number_of_records())]

    return records


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
