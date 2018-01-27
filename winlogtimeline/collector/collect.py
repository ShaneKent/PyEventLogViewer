import xmltodict
from xml.parsers.expat import ExpatError
import pyevtx
from winlogtimeline.util.logs import Record
from .parser import parser

from hashlib import md5


# Note: It may be useful to take config out of this whole equation. Config could store the default filter configuration,
# and that could be copied into the project config to allow user modifications.
def import_log(log_file, alias, project, config, status_callback, progress_context_manager):
    """
    Main routine to import an event log file.
    :param log_file: A path to an event log file.
    :param alias: A string for the alias of the log file.
    :param project: A project instance.
    :param config: A config dictionary.
    :param status_callback: A function to relay status info the the GUI. Should accept status as a string.
    :param progress_context_manager: A function that takes a max_value and returns a context manager used for updating
        the progress bar.
    :return: None
    """

    status_callback('Parsing {} file as {}.'.format(log_file, alias))

    # Get hash of the record.
    with open(log_file, "rb") as file:
        file_hash = md5(file.read()).hexdigest()

    # Open the file with pyevtx and parse.
    log = pyevtx.open(log_file)
    records = collect_records(log)  # + collect_deleted_records(log)
    xml_records = xml_convert(records, alias)

    status_callback('Parsing records...')

    with progress_context_manager(log.get_number_of_records()) as progress_bar:
        for i, record in enumerate(xml_records):
            # Write records to the sqlite db.

            if record[0] is not None:
                project.write_log_data(Record(**record[0]), record[1])

            # Update the status bar so we know that things are happening.
            if i % 100 == 0:
                progress_bar.update_progress(100)

    status_callback('Finished parsing records')
    # Write project information to the sqlite db.
    project.write_verification_data(file_hash, log_file, alias)

    return


def xml_convert(records, source_file_alias, recovered=True):
    for record in records:
        try:
            d = xmltodict.parse(record)
        except ExpatError:
            record = record.replace("\x00", "")  # This can not be the best way to do this...
            d = xmltodict.parse(record)

        sys = d['Event']['System']

        dictionary = parser(d, {
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
            'recovered': recovered,
            'alias': source_file_alias
        })

        yield [dictionary, record]


def collect_records(event_file):
    """
    :param event_file: An event log object.
    :return: A list of event records in the format returned by libevtx-python.
    """
    for i in range(event_file.get_number_of_records()):
        yield event_file.get_record(i).xml_string


def filter_logs(logs, project, config):
    """
    When given a list of log objects, returns only those that match the filters defined in config and project. The
    filters in project take priority over config.
    :param logs: A list of log objects. Logs must be in the format returned by winlogtimeline.util.logs.parse_record.
    :param project: A project instance.
    :param config: A config dictionary.
    :return: A list of logs that satisfy the filters specified in the configuration.
    """
    #config = [('event_id', '=', 5061)]

    query = 'SELECT * FROM logs WHERE '
    for constraint in config:
        query += '{} {} {} AND '.format(*constraint)
    query = query[:-5]
    print(query)

    #cur = project._conn.execute(query)

    #logs = cur.fetchall()

    return logs