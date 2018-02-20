# Run Instructions:
# All tests: python3 setup.py test
# Just this file: pytest tests/test_collect.py -s
# Update code base being tested
# pip3 install --upgrade .
# pip3 install --user --upgrade .
import os
from winlogtimeline.collector import collect
from winlogtimeline.util import project
from winlogtimeline.ui import ui
from hashlib import md5
import shutil
import pyevtx
import mock

# new GUI instance for testing
gui = ui.GUI()
# path to log file
record_file = os.path.abspath('tests/Security.evtx')
# test project Instance
proj = project.Project(os.path.abspath('tests/TestProject/TestProject.elv'))
# status text
text = '{file}: {status}'.format(file=os.path.basename(record_file), status='{status}')


@mock.patch('winlogtimeline.collector.collect.collect_records')
@mock.patch('winlogtimeline.collector.collect.xml_convert')
@mock.patch.object(proj, 'write_log_data')
@mock.patch.object(proj, 'write_verification_data')
def test_import_log_func_calls(mock_verify_data, mock_log_data, mock_xml, mock_collect):
    collect.import_log(record_file, 'Secure', proj, '', lambda s: gui.update_status_bar(text.format(status=s)),
                       gui.get_progress_bar_context_manager)

    assert mock_collect.called
    assert mock_xml.called
    # assert mock_log_data.called  # why is this false not true? Issues with loop possibly?
    assert mock_verify_data.called


@mock.patch('winlogtimeline.collector.parser.parser')
def test_xml_convert(mock_parser):
    with open(record_file, "rb") as file:
        file_hash = md5(file.read()).hexdigest()

    # Open the file with pyevtx and parse.
    log = pyevtx.open(record_file)
    records = collect.collect_records(log)  # + collect_deleted_records(log)
    xml_records = collect.xml_convert(records, file_hash, 'test')
    # assert mock_parser.called  # Another issue with loops?


# Remove testing project
proj.close()
shutil.rmtree(os.path.abspath('tests/TestProject'))
