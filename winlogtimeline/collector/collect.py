import re
import sys
import xmltodict
from xml.parsers.expat import ExpatError
import pyevtx
from winlogtimeline.util.logs import Record
from .parser import parser
from .parser import get_string

from hashlib import md5
from itertools import chain


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

    user_parsers = project.config.get('events', {}).get('custom', {})

    # Open the file with pyevtx and parse.
    log = pyevtx.open(log_file)
    records = collect_records(log)
    recovered = collect_deleted_records(log)
    xml_records = chain(xml_convert(records, alias, user_parsers),
                        xml_convert(recovered, alias, user_parsers, recovered=True))

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


def build_illegal_charset_regex():
    """
    The XML parsing library we use doesn't play too nicely with unicode strings. The regex built by this function will
    remove a large number of the illegal characters, but not all.
    :return:
    """
    _illegal_unichrs = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F),
                        (0x7F, 0x84), (0x86, 0x9F),
                        (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)]
    if sys.maxunicode >= 0x10000:  # not narrow build
        _illegal_unichrs.extend([(0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF),
                                 (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF),
                                 (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
                                 (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
                                 (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF),
                                 (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
                                 (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
                                 (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF)])

    _illegal_ranges = ["%s-%s" % (chr(low), chr(high))
                       for (low, high) in _illegal_unichrs]
    return re.compile(r'[{}]'.format(''.join(_illegal_ranges)))


def xml_convert(records, source_file_alias, user_parsers, recovered=False):
    illegal_charset = build_illegal_charset_regex()

    for record in records:
        try:
            d = xmltodict.parse(record)
        except ExpatError:
            # The string contains illegal xml characters and is giving xmltodict some trouble. Attempt to sanitize it.
            subbed_record = re.sub(illegal_charset, '?', record)

            try:
                d = xmltodict.parse(subbed_record)
            except ExpatError:
                # Unable to sanitize the string using a list of known bad unicode characters. Toss it.
                continue

        sys_info = d['Event']['System']

        event_id = get_string(sys_info['EventID'])

        dictionary = parser(d, {
            'timestamp_utc': sys_info['TimeCreated']['@SystemTime'],
            'event_id': event_id,
            'description': '',
            'details': '',
            'event_source': sys_info['Provider']['@Name'],
            'event_log': sys_info['Channel'],
            'session_id': '',
            'account': '',
            'computer_name': sys_info['Computer'],
            'record_number': sys_info['EventRecordID'],
            'recovered': recovered,
            'alias': source_file_alias
        }, user_parsers)

        yield (dictionary, record)


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
    :return: A list of event records in the format returned by libevtx-python.
    """
    list = []
    for i in range(event_file.get_number_of_recovered_records()):
        try:
            list.append(event_file.get_recovered_record(i).xml_string)
        except OSError:
            continue

    return list


def filter_logs(logs, project, config):
    """
    When given a list of log objects, returns only those that match the filters defined in config and project. The
    filters in project take priority over config.
    :param logs: A list of log objects. Logs must be in the format returned by winlogtimeline.util.logs.parse_record.
    :param project: A project instance.
    :param config: A config dictionary.
    :return: A list of logs that satisfy the filters specified in the configuration.
    """
    # config = [('event_id', '=', 5061)]

    query = 'SELECT * FROM logs WHERE '
    for constraint in config:
        query += '{} {} {} AND '.format(*constraint)
    query = query[:-5]
    print(query)

    # cur = project._conn.execute(query)

    # logs = cur.fetchall()

    return logs
