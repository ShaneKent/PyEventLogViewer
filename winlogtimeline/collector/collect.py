import pyevtx
import Evtx.Evtx as evtx
import lxml.etree
import winlogtimeline.util as util


# Note: It may be useful to take config out of this whole equation. Config could store the default filter configuration,
# and that could be copied into the project config to allow user modifications.
def import_log(log_file, project, config):
    """
    Main routine to import an event log file into a project.
    :param log_file: A path to an event log file.
    :param project: A project instance.
    :param config: A config dictionary.
    :return: None
    """
    with evtx.Evtx(log_file) as log:            # Open the event logs.
        records = collect_records(log)          # Get existing records.
        machine_name = get_machine_name(records)

        print(machine_name)

    # Pull the logs from the event log file
    # event_records = collect_records(event_file) + collect_deleted_records(event_file)
    # machine_name = get_machine_name(event_file)
    # logs = (util.logs.parse_record(record, machine_name) for record in event_records)
    # logs = filter_logs(logs, project, config)
    # for log in logs:
    #    project.write_log_data(log)

    # Pull verification data from the event log file
    # file_hash = get_log_file_hash(log_file)
    # project.write_verification_data(file_hash, log_file)

    # Close the event log
    # event_file.close()


def collect_records(event_file):
    """
    :param event_file: An event log object.
    :return: A list of event records in the format returned by libevtx-python.
    """
    records = event_file.records()

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

    names = []

    for record in records:
        roots = record.lxml().getchildren()
        children = roots[0]

        name = children.find("{http://schemas.microsoft.com/win/2004/08/events/event}Computer").text

        if name not in names:
            names.append(name)

    print(names)

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
