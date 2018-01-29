# Run Instructions:
    # python3 setup.py test

import os
from xml.parsers.expat import ExpatError
from winlogtimeline.collector import collect
from winlogtimeline.collector import parser
from hashlib import md5
import xmltodict
import pyevtx


# path to log file
record_file = os.path.abspath('tests/Security.evtx')

with open(record_file, "rb") as file:
    file_hash = md5(file.read()).hexdigest()

# Open the file with pyevtx and parse.
log = pyevtx.open(record_file)
records = collect.collect_records(log)

def test_parser():
    for record in records:
        try:
            d = xmltodict.parse(record)
        except ExpatError:
            record = record.replace("\x00", "")  # This can not be the best way to do this...
            d = xmltodict.parse(record)

        sys = d['Event']['System']

        rec = {'timestamp_utc': sys['TimeCreated']['@SystemTime'],
               'event_id': sys['EventID'],
               'description': '',
               'details': '',
               'event_source': sys['Provider']['@Name'],
               'event_log': sys['Channel'],
               'session_id': '',
               'account': '',
               'computer_name': sys['Computer'],
               'record_number': sys['EventRecordID'],
               'recovered': True,
               'alias': 'Sample'
               }

        event_id = rec["event_id"]

        if event_id == "1":
            record = parser.parse_id_1(d, rec)  # System    -   Wake Up
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == "SYSTEM"
            assert(record["description"]) == "Wake Up"
            assert(record["details"]) == f'Wake Time: {data[1]["#text"][0:11]} {data[1]["#text"][11:23]} (UTC) | ' \
                                         f'Sleep Start Time: {data[0]["#text"][0:11]} {data[0]["#text"][11:23]} (UTC)'

        elif event_id == "12":
            record = parser.parse_id_12(d, rec)  # System    -   System Start
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == "SYSTEM"
            assert(record["description"]) == "System Start"
            if len(data) == 7:
                assert(record["details"]) == f'Starting Windows NT version {data[0]["#text"]}. {data[1]["#text"]}. ' \
                                             f'{data[2]["#text"]} at {data[6]["#text"][0:10]} {data[6]["#text"][11:23]} (UTC)'

        elif event_id == "13":
            record = parser.parse_id_13(d, rec)  # System    -   System Shutdown
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == "SYSTEM"
            assert(record["description"]) == "System Shutdown"
            assert(record["details"]) == f'Shutdown Time: {data["#text"][0:10]} {data["#text"][11:23]} (UTC)'

        elif event_id == "41":
            record = parser.parse_id_41(d, rec)  # System    -   Shutdown Error
            assert(record["account"]) == "SYSTEM"
            assert(record["description"]) == "Shutdown Error"

        elif event_id == "42":
            record = parser.parse_id_42(d, rec)  # System    -   Sleep Mode
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == "SYSTEM"
            assert(record["description"]) == "Sleep Mode"
            reason = data[2]["#text"]
            if reason == "0":
                assert(record["details"]) == "Starting Sleep Mode. Reason: Power button/Close lid"
            elif reason == "2":
                assert(record["details"]) == "Starting Sleep Mode. Reason: Low battery"
            elif reason == "4":
                assert(record["details"]) == "Starting Sleep Mode. Reason: Application"
            elif reason == "7":
                assert(record["details"]) == "Starting Sleep Mode. Reason: System idle"
            else:
                assert(record["details"]) == "Starting Sleep Mode. Reason: Undefined*"

        elif event_id == "104":
            record = parser.parse_id_104(d, rec)  # System    -   Log Cleared
            data = d["Event"]["UserData"]["LogFileCleared"]
            assert(record["account"]) == data["SubjectUserName"]
            assert(record["description"]) == "Log Cleared"
            assert(record["details"]) == f'System event log was cleared by the following account: ' \
                                         f'{data["SubjectDomainName"]}\\{data["Channel"]}'

        elif event_id == "1074":
            record = parser.parse_id_1074(d, rec)  # System    -   Shutdown Initiated
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[6]["#text"].split("\\")[-1]
            assert(record["details"]) == f'Cause: {data[4]["#text"]}'
            assert(record["computer_name"]) == data[1]["#text"]
            if data[3]["#text"] == "0x500ff":
                assert(record["description"]) == "Shutdown Initiated"
            else:
                assert(record["description"]) == "ERROR"

        elif event_id == "1102":
            record = parser.parse_id_1102(d, rec)  # Security  -   Log Cleared
            data = d["Event"]["EventData"]["Data"]
            assert(record["description"]) == "Log Cleared"
            assert(record["account"]) == data[1]["#text"]
            assert(record["details"]) == f'Security event log was cleared by the following account: ' \
                                f'{data[2]["#text"]}\\{data[1]["#text"]}'
            assert(record["session_id"]) == data[3]["#text"]

        elif event_id == "4616":
            record = parser.parse_id_4616(d, rec)  # System    -   Time Change
            data = d["Event"]["EventData"]["Data"]
            assert(record["description"]) == "Time Change"
            assert(record["account"]) == data[1]["#text"]
            assert(record["details"]) == f'Changed To: {data[5]["#text"][0:10]} {data[5]["#text"][11:23]} (UTC) | ' \
                                f'Previous Time: {data[4]["#text"][0:10]} {data[4]["#text"][11:23]} (UTC)'

        elif event_id == "4624":
            record = parser.parse_id_4624(d, rec)  # System    -   Logon Events
            data = d["Event"]["EventData"]["Data"]
            reason = data[8]["#text"]
            assert(record["account"]) == data[5]["#text"]
            if reason == "2":
                assert(record["description"]) == "Interactive Logon"
            elif reason == "3":
                assert(record["description"]) == "Network Connection"
            elif reason == "7":
                assert(record["description"]) == "Unlock Workstation"
            elif reason == "10":
                assert(record["description"]) == "Remote Interactive Logon"
                assert(record["details"]) == f'From: {data[18]["#text"]} using {data[10]["#text"]} auth as ' \
                                    f'{data[6]["#text"]}\\{data[5]["#text"]}'
            elif reason == "11":
                assert(record["description"]) == "Interactive Logon"
                assert(record["details"]) == f'Logon as {data[6]["#text"]}\\{data[5]["#text"]} using cached credentials'
            assert(record["session_id"]) == data[7]["#text"]

        elif event_id == "4634":
            record = parser.parse_id_4634(d, rec)  # Security  -   Logoff (Network Connection)
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[4]["#text"]
            assert(record["description"]) == "Logoff"
            if data[4]["#text"] == "3":
                assert(record["details"]) == "End of Network Connection session"
            else:
                assert(record["details"]) == "EXCLUDED"
            assert(record["session_id"]) == data[3]["#text"]

        elif event_id == "4647":
            record = parser.parse_id_4647(d, rec)  # Security  -   User-Initiated Logoff
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[1]["#text"]
            assert(record["description"]) == "User Initiated Logoff"
            assert(record["session_id"]) == data[3]["#text"]

        elif event_id == "4720":
            record = parser.parse_id_4720(d, rec)  # Security  -   Account Created
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[4]["#text"]
            assert(record["description"]) == "Account Created"
            assert(record["details"]) == f'New account name: {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                                f'was created by user account ({data[4]["#text"]})'
            assert(record["session_id"]) == data[6]["#text"]

        elif event_id == "4722":
            record = parser.parse_id_4722(d, rec)  # Security  -   Account Enabled
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[4]["#text"]
            assert(record["description"]) == "Account Enabled"
            assert(record["details"]) == f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                                f'was enabled by user account ({data[4]["#text"]})'
            assert(record["session_id"]) == data[6]["#text"]

        elif event_id == "4723":
            record = parser.parse_id_4723(d, rec)  # Security  -   User Changed Password
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[4]["#text"]
            assert(record["description"]) == "User Changed Password"
            assert(record["details"]) == f'The password of user account {data[0]["#text"]} ' \
                                         f'(RID {data[2]["#text"][41:45]}) was changed by the user ({data[4]["#text"]})'
            assert(record["session_id"]) == data[6]["#text"]

        elif event_id == "4724":
            record = parser.parse_id_4724(d, rec)  # Security  -   Privileged User Reset Password
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[4]["#text"]
            assert(record["description"]) == "Privileged User Reset Password"
            assert(record["details"]) == f'The password of user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                                f'was reset by a privileged user account ({data[4]["#text"]})'
            assert(record["session_id"]) == data[6]["#text"]

        elif event_id == "4725":
            record = parser.parse_id_4725(d, rec)  # Security  -   Account Disabled
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[4]["#text"]
            assert(record["description"]) == "Account Disabled"
            assert(record["details"]) == f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                                f'was disabled by user account ({data[4]["#text"]})'
            assert(record["session_id"]) == data[6]["#text"]

        elif event_id == "4726":
            record = parser.parse_id_4726(d, rec)  # Security  -   Account Deleted
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == data[4]["#text"]
            assert(record["description"]) == "Account Deleted"
            assert(record["details"]) == f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                                f'was deleted by user account ({data[4]["#text"]})'
            assert(record["session_id"]) == data[6]["#text"]

        elif event_id == "6008":
            record = parser.parse_id_6008(d, rec)  # System    -   Shutdown Error
            record["description"] = "Shutdown Error"
        elif event_id == "6013":
            record = parser.parse_id_6013(d, rec)  # System    -   System Status
            data = d["Event"]["EventData"]["Data"]
            assert(record["account"]) == "SYSTEM"
            assert(record["description"]) == "System Status"
            assert(record["details"]) == f'System Uptime: {data[4]["#text"]} seconds. ' \
                                         f'Time Zone Setting: {data[6]["#text"]}.'