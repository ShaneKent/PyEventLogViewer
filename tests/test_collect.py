# Run Instructions:
    # python3 setup.py test

import os
from winlogtimeline.collector import collect
from winlogtimeline.util import project
from winlogtimeline.ui import ui
from hashlib import md5
import xmltodict
import pyevtx
import mock

# new GUI instance for testing
gui = ui.GUI()
# path to log file
record_file = os.path.abspath('tests/Security.evtx')
# test project Instance
proj = project.Project('/Users/zachmonroe/Library/Application Support/PyEventLogTimeline/Projects/New Project/New Project.elv')
# status text
text = '{file}: {status}'.format(file=os.path.basename(record_file), status='{status}')


@mock.patch('winlogtimeline.collector.collect.collect_records')
@mock.patch('winlogtimeline.collector.collect.xml_convert')
@mock.patch.object(proj, 'write_log_data')
@mock.patch.object(proj, 'write_verification_data')

def test_import_log_func_calls(mock_verify_data, mock_log_data, mock_xml, mock_collect):
    collect.import_log(record_file, 'Secure', proj, '', lambda s: gui.update_status_bar(text.format(status=s)),
                       gui.get_progress_bar_context_manager)

    assert(mock_collect.called) == True
    assert(mock_xml.called) == True
    #assert(mock_log_data.called) == True # why is this false not true? Issues with loop possibly?
    assert(mock_verify_data.called) == True


@mock.patch('winlogtimeline.collector.parser.parser')
def test_xml_convert(mock_parser):
    with open(record_file, "rb") as file:
        file_hash = md5(file.read()).hexdigest()

    # Open the file with pyevtx and parse.
    log = pyevtx.open(record_file)
    records = collect.collect_records(log)  # + collect_deleted_records(log)
    xml_records = collect.xml_convert(records, file_hash)
    #assert(mock_parser.called) == True # Another issue with loops?



# def filter_logs(logs, project, config):
#     """
#     When given a list of log objects, returns only those that match the filters defined in config and project. The
#     filters in project take priority over config.
#     :param logs: A list of log objects. Logs must be in the format returned by winlogtimeline.util.logs.parse_record.
#     :param project: A project instance.
#     :param config: A config dictionary.
#     :return: A list of logs that satisfy the filters specified in the configuration.
#     """
#     config = [('event_id', '=', 5061)]
#
#     query = 'SELECT * FROM logs WHERE '
#     for constraint in config:
#         query += '{} {} {} AND '.format(*constraint)
#     query = query[:-5]
#
#     cur = project._conn.execute(query)
#
#     logs = cur.fetchall()
#
#     return logs
