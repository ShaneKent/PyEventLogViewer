# Run Instructions:
    # python3 setup.py test
    # pytest tests/test_parser.py -s
    # pip3 install --upgrade .
    # pip3 install --user --upgrade .

import os
from xml.parsers.expat import ExpatError
from winlogtimeline.collector import collect
from winlogtimeline.collector import parser
from hashlib import md5
import xmltodict
import pyevtx


#path to log file
#record_file = os.path.abspath('tests/System.evtx')

#with open(record_file, "rb") as file:
    #file_hash = md5(file.read()).hexdigest()

#Open the file with pyevtx and parse.
#log = pyevtx.open(record_file)
#records = collect.collect_records(log)

def test_parser_id_1():
    xmlInput = '<Event xmlns = "http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Kernel-General" Guid="{A68CA8B7-004F-D7B6-A698-07E2DE0F1F5D}"/>' +\
    '<EventID>1</EventID>' +\
    '<Version>1</Version>' +\
    '<Level>4</Level>' +\
    '<Task>5</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8000000000000010</Keywords>' +\
    '<TimeCreated SystemTime="2017-01-02T00:28:02.499911900Z"/>' +\
    '<EventRecordID>521</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="4" ThreadID="372"/>' +\
    '<Channel>System</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="NewTime">2017-01-02T00:28:02.500000000Z</Data>' +\
    '<Data Name="OldTime">2017-01-01T22:19:39.790389600Z</Data>' +\
    '<Data Name="Reason">2</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_1(d, rec)
    assert(record["account"]) == "SYSTEM"
    assert(record["description"]) == "Wake Up"
    assert (record["details"]) == "Wake Time: 2017-01-01T 22:19:39.790 (UTC) | " +\
           "Sleep Start Time: 2017-01-02T 00:28:02.500 (UTC)"


def test_parser_id_12():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Kernel-General" Guid="{A68CA8B7-004F-D7B6-A698-07E2DE0F1F5D}"/>' +\
    '<EventID>12</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>4</Level>' +\
    '<Task>1</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8000000000000080</Keywords>' +\
    '<TimeCreated SystemTime="2017-01-01T21:18:30.833529000Z"/>' +\
    '<EventRecordID>1</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="4" ThreadID="8"/>' +\
    '<Channel>System</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security UserID="S-1-5-18"/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="MajorVersion">10</Data>' +\
    '<Data Name="MinorVersion">0</Data>' +\
    '<Data Name="BuildVersion">14393</Data>' +\
    '<Data Name="QfeVersion">576</Data>' +\
    '<Data Name="ServiceVersion">0</Data>' +\
    '<Data Name="BootMode">0</Data>' +\
    '<Data Name="StartTime">2017-01-01T21:18:30.493716600Z</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_12(d, rec)
    assert(record["account"]) == "SYSTEM"
    assert(record["description"]) == "System Start"
    assert(record["details"]) == 'Starting Windows NT version 10. 0. 14393 at 2017-01-01 21:18:30.493 (UTC)'


def test_parser_id_13():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Kernel-General" Guid="{A68CA8B7-004F-D7B6-A698-07E2DE0F1F5D}"/>' +\
    '<EventID>13</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>4</Level>' +\
    '<Task>2</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8000000000000080</Keywords>' +\
    '<TimeCreated SystemTime="2017-01-01T21:23:31.105184900Z"/>' +\
    '<EventRecordID>308</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="4" ThreadID="400"/>' +\
    '<Channel>System</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="StopTime">2017-01-01T21:23:31.105183800Z</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_13(d, rec)
    assert(record["account"]) == "SYSTEM"
    assert(record["description"]) == "System Shutdown"
    assert(record["details"]) == "Shutdown Time: 2017-01-01 21:23:31.105 (UTC)"


def test_parser_id_41():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Kernel-Power" Guid="{331C3B3A-2005-44C2-AC5E-77220C37D6B4}"/>' +\
    '<EventID>41</EventID>' +\
    '<Version>4</Version>' +\
    '<Level>1</Level>' +\
    '<Task>63</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8000400000000002</Keywords>' +\
    '<TimeCreated SystemTime="2017-01-16T17:25:11.723879500Z"/>' +\
    '<EventRecordID>1569</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="4" ThreadID="8"/>' +\
    '<Channel>System</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security UserID="S-1-5-18"/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="BugcheckCode">0</Data>' +\
    '<Data Name="BugcheckParameter1">0x0000000000000000</Data>' +\
    '<Data Name="BugcheckParameter2">0x0000000000000000</Data>' +\
    '<Data Name="BugcheckParameter3">0x0000000000000000</Data>' +\
    '<Data Name="BugcheckParameter4">0x0000000000000000</Data>' +\
    '<Data Name="SleepInProgress">4</Data>' +\
    '<Data Name="PowerButtonTimestamp">0</Data>' +\
    '<Data Name="BootAppStatus">0</Data>' +\
    '<Data Name="Checkpoint">0</Data>' +\
    '<Data Name="ConnectedStandbyInProgress">false</Data>' +\
    '<Data Name="SystemSleepTransitionsToOn">12</Data>' +\
    '<Data Name="CsEntryScenarioInstanceId">0</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_41(d, rec)
    assert (record["account"]) == "SYSTEM"
    assert (record["description"]) == "Shutdown Error"


def test_parser_id_42():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Kernel-Power" Guid="{331C3B3A-2005-44C2-AC5E-77220C37D6B4}"/>' +\
    '<EventID>42</EventID>' +\
    '<Version>3</Version>' +\
    '<Level>4</Level>' +\
    '<Task>64</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8000400000000404</Keywords>' +\
    '<TimeCreated SystemTime="2017-01-01T22:19:38.726978700Z"/>' +\
    '<EventRecordID>519</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="4" ThreadID="372"/>' +\
    '<Channel>System</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="TargetState">4</Data>' +\
    '<Data Name="EffectiveState">4</Data>' +\
    '<Data Name="Reason">0</Data>' +\
    '<Data Name="Flags">4</Data>' +\
    '<Data Name="TransitionsToOn">1</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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


def test_parser_id_104():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Eventlog" Guid="{fc65ddd8-d6ef-4962-83d5-6e5cfe9ce148}"/>' +\
    '<EventID>104</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>4</Level>' +\
    '<Task>104</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8000000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2018-01-27T04:17:28.719000600Z"/>' +\
    '<EventRecordID>4294</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="1560" ThreadID="13028"/>' +\
    '<Channel>System</Channel>' +\
    '<Computer>DESKTOP-C0O9EV0</Computer>' +\
    '<Security UserID="S-1-5-21-1990300061-1030431749-3499390798-1001"/>' +\
    '</System>' +\
    '<UserData>' +\
    '<LogFileCleared xmlns="http://manifests.microsoft.com/win/2004/08/windows/eventlog">' +\
    '<SubjectUserName>Shane Kent</SubjectUserName>' +\
    '<SubjectDomainName>DESKTOP-C0O9EV0</SubjectDomainName>' +\
    '<Channel>System</Channel>' +\
    '<BackupPath>\\DESKTOP-C0O9EV0\\Users\Shane Kent\Desktop\System - Personal.evtx</BackupPath>' +\
    '</LogFileCleared>' +\
    '</UserData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_104(d, rec)  # System    -   Log Cleared
    assert(record["account"]) == "Shane Kent"
    assert(record["description"]) == "Log Cleared"
    assert(record["details"]) == "System event log was cleared by the following account: DESKTOP-C0O9EV0\System"


def test_parser_id_1074_unwanted():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="User32" Guid="{b0aa8734-56f7-41cc-b2f4-de228e98b946}" EventSourceName="User32"/>' +\
    '<EventID Qualifiers="32768">1074</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>4</Level>' +\
    '<Task>0</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8080000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2017-01-01T21:23:26.117277400Z"/>' +\
    '<EventRecordID>299</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="516" ThreadID="532"/>' +\
    '<Channel>System</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security UserID="S-1-5-18"/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="param1">C:\WINDOWS\system32\winlogon.exe (LAPTOP-9KUQNI2Q)</Data>' +\
    '<Data Name="param2">LAPTOP-9KUQNI2Q</Data>' +\
    '<Data Name="param3">Operating System: Upgrade (Planned)</Data>' +\
    '<Data Name="param4">0x80020003</Data>' +\
    '<Data Name="param5">restart</Data>' +\
    '<Data Name="param6"/>' +\
    '<Data Name="param7">NT AUTHORITY\SYSTEM</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_1074(d, rec)  # System    -   Shutdown Initiated
    assert (record) == None  # This is the case because Bruce "tosses" any 1074 records where Data param4 != 0x500ff.


def test_parser_id_1074_wanted():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="User32" Guid="{b0aa8734-56f7-41cc-b2f4-de228e98b946}" EventSourceName="User32"/>' +\
    '<EventID Qualifiers="32768">1074</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>4</Level>' +\
    '<Task>0</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8080000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2017-04-25T02:13:31.902135000Z"/>' +\
    '<EventRecordID>10296</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="744" ThreadID="900"/>' +\
    '<Channel>System</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security UserID="S-1-5-21-26884411-4197249062-1617423603-1001"/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="param1">C:\WINDOWS\system32\winlogon.exe (LAPTOP-9KUQNI2Q)</Data>' +\
    '<Data Name="param2">LAPTOP-9KUQNI2Q</Data>' +\
    '<Data Name="param3">No title for this reason could be found</Data>' +\
    '<Data Name="param4">0x500ff</Data>' +\
    '<Data Name="param5">power off</Data>' +\
    '<Data Name="param6"/>' +\
    '<Data Name="param7">LAPTOP-9KUQNI2Q\sarah</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_1074(d, rec)  # System    -   Shutdown Initiated
    data = d["Event"]["EventData"]["Data"]
    assert(record["account"]) == "sarah"
    assert(record["details"]) == "Cause: power off"
    assert(record["computer_name"]) == "LAPTOP-9KUQNI2Q"
    if data[3]["#text"] == "0x500ff":
       assert(record["description"]) == "Shutdown Initiated"
    else:
       assert(record["description"]) == "ERROR"


def test_parser_id_1102():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Eventlog" Guid="{fc65ddd8-d6ef-4962-83d5-6e5cfe9ce148}"/>' +\
    '<EventID>1102</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>4</Level>' +\
    '<Task>104</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x4020000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2018-01-27T04:17:18.549878600Z"/>' +\
    '<EventRecordID>19830</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="1560" ThreadID="7180"/>' +\
    '<Channel>Security</Channel>' +\
    '<Computer>DESKTOP-C0O9EV0</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<UserData>' +\
    '<LogFileCleared xmlns="http://manifests.microsoft.com/win/2004/08/windows/eventlog">' +\
    '<SubjectUserSid>S-1-5-21-1990300061-1030431749-3499390798-1001</SubjectUserSid>' +\
    '<SubjectUserName>Shane Kent</SubjectUserName>' +\
    '<SubjectDomainName>DESKTOP-C0O9EV0</SubjectDomainName>' +\
    '<SubjectLogonId>0x000000000105f3cd</SubjectLogonId>' +\
    '</LogFileCleared>' +\
    '</UserData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_1102(d, rec)  # Security  -   Log Cleared
    assert(record["description"]) == "Log Cleared"
    assert(record["account"]) == "S-1-5-21-1990300061-1030431749-3499390798-1001"
    assert (record["details"]) == "Security event log was cleared by the following account: S-1-5-21-1990300061-1030431749-3499390798-1001\DESKTOP-C0O9EV0"
    assert (record["session_id"]) == "0x000000000105f3cd"


def test_parser_id_4616():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-A5BA-3E3B0328C30D}"/>' +\
    '<EventID>4616</EventID>' +\
    '<Version>1</Version>' +\
    '<Level>0</Level>' +\
    '<Task>12288</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8020000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2017-09-30T06:45:03.871307200Z"/>' +\
    '<EventRecordID>81180</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="4" ThreadID="188"/>' +\
    '<Channel>Security</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="SubjectUserSid">S-1-5-19</Data>' +\
    '<Data Name="SubjectUserName">LOCAL SERVICE</Data>' +\
    '<Data Name="SubjectDomainName">NT AUTHORITY</Data>' +\
    '<Data Name="SubjectLogonId">0x00000000000003e5</Data>' +\
    '<Data Name="PreviousTime">2017-09-30T06:45:03.871437900Z</Data>' +\
    '<Data Name="NewTime">2017-09-30T06:45:03.871000000Z</Data>' +\
    '<Data Name="ProcessId">0x000000000000046c</Data>' +\
    '<Data Name="ProcessName">C:\Windows\System32\svchost.exe</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_4616(d, rec)  # Security  -   Log Cleared
    assert (record["description"]) == "Time Change"
    assert (record["account"]) == "LOCAL SERVICE"
    assert (record["details"]) == "Changed To: 2017-09-30 06:45:03.871 (UTC) | Previous Time: 2017-09-30 06:45:03.871 (UTC)"


def test_parser_id_4624():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-A5BA-3E3B0328C30D}"/>' +\
    '<EventID>4624</EventID>' +\
    '<Version>2</Version>' +\
    '<Level>0</Level>' +\
    '<Task>12544</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8020000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2017-09-20T22:07:05.888823900Z"/>' +\
    '<EventRecordID>74756</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="952" ThreadID="11908"/>' +\
    '<Channel>Security</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="SubjectUserSid">S-1-5-18</Data>' +\
    '<Data Name="SubjectUserName">LAPTOP-9KUQNI2Q$</Data>' +\
    '<Data Name="SubjectDomainName">WORKGROUP</Data>' +\
    '<Data Name="SubjectLogonId">0x00000000000003e7</Data>' +\
    '<Data Name="TargetUserSid">S-1-5-21-26884411-4197249062-1617423603-1001</Data>' +\
    '<Data Name="TargetUserName">sarahb2626@gmail.com</Data>' +\
    '<Data Name="TargetDomainName">MicrosoftAccount</Data>' +\
    '<Data Name="TargetLogonId">0x00000000070cb74f</Data>' +\
    '<Data Name="LogonType">7</Data>' +\
    '<Data Name="LogonProcessName">Negotiat</Data>' +\
    '<Data Name="AuthenticationPackageName">Negotiate</Data>' +\
    '<Data Name="WorkstationName">LAPTOP-9KUQNI2Q</Data>' +\
    '<Data Name="LogonGuid">{00000000-0000-0000-0000-000000000000}</Data>' +\
    '<Data Name="TransmittedServices">-</Data>' +\
    '<Data Name="LmPackageName">-</Data>' +\
    '<Data Name="KeyLength">0</Data>' +\
    '<Data Name="ProcessId">0x00000000000003b8</Data>' +\
    '<Data Name="ProcessName">C:\Windows\System32\lsass.exe</Data>' +\
    '<Data Name="IpAddress">-</Data>' +\
    '<Data Name="IpPort">-</Data>' +\
    '<Data Name="ImpersonationLevel">%%1833</Data>' +\
    '<Data Name="RestrictedAdminMode">-</Data>' +\
    '<Data Name="TargetOutboundUserName">-</Data>' +\
    '<Data Name="TargetOutboundDomainName">-</Data>' +\
    '<Data Name="VirtualAccount">%%1843</Data>' +\
    '<Data Name="TargetLinkedLogonId">0x00000000070cb92a</Data>' +\
    '<Data Name="ElevatedToken">%%1842</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_4624(d, rec)
    data = d["Event"]["EventData"]["Data"]
    reason = data[8]["#text"]
    assert(record["account"]) == "sarahb2626@gmail.com"

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
        assert(record["details"]) == "Logon as MicrosoftAccount\sarahb2626@gmail.com using cached credentials"

    assert(record["session_id"]) == "0x00000000070cb74f"


def test_parser_id_4634():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-A5BA-3E3B0328C30D}"/>' +\
    '<EventID>4634</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>0</Level>' +\
    '<Task>12545</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8020000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2017-09-20T22:07:05.889512400Z"/>' +\
    '<EventRecordID>74759</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="952" ThreadID="6700"/>' +\
    '<Channel>Security</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="TargetUserSid">S-1-5-21-26884411-4197249062-1617423603-1001</Data>' +\
    '<Data Name="TargetUserName">sarah</Data>' +\
    '<Data Name="TargetDomainName">LAPTOP-9KUQNI2Q</Data>' +\
    '<Data Name="TargetLogonId">0x00000000070cb92a</Data>' +\
    '<Data Name="LogonType">7</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_4634(d, rec)
    data = d["Event"]["EventData"]["Data"]
    assert (record["account"]) == "sarah"  # This was being incorrectly parsed originally.
    assert(record["description"]) == "Logoff"

    temp = data[4]["#text"]
    if temp == "2":
        assert (record["details"]) == "Logoff from Interactive session"
    elif temp == "3":
        assert (record["details"]) == "End of Network Connection session"
    elif temp == "7":
        assert (record["details"]) == "Unlock Workstation"
    elif temp == "10":
        assert (record["details"]) == "Logoff from Remote Interactive Session"
    else:
        assert (record["details"]) == None

    assert (record["session_id"]) == "0x00000000070cb92a"


def test_parser_id_4647():
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-A5BA-3E3B0328C30D}"/>' +\
    '<EventID>4647</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>0</Level>' +\
    '<Task>12545</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8020000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2017-07-14T02:58:51.707545100Z"/>' +\
    '<EventRecordID>57191</EventRecordID>' +\
    '<Correlation ActivityID="{ED7488E8-FACA-0001-0989-74EDCAFAD201}"/>' +\
    '<Execution ProcessID="944" ThreadID="10404"/>' +\
    '<Channel>Security</Channel>' +\
    '<Computer>LAPTOP-9KUQNI2Q</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="TargetUserSid">S-1-5-21-26884411-4197249062-1617423603-1001</Data>' +\
    '<Data Name="TargetUserName">sarah</Data>' +\
    '<Data Name="TargetDomainName">LAPTOP-9KUQNI2Q</Data>' +\
    '<Data Name="TargetLogonId">0x000000000005a6d8</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_4647(d, rec)
    assert(record["account"]) == "sarah"
    assert(record["description"]) == "User Initiated Logoff"
    assert(record["session_id"]) == "0x000000000005a6d8"


def test_parser_id_4720(): # Do not have
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-A5BA-3E3B0328C30D}"/>' +\
    '<EventID>4720</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>0</Level>' +\
    '<Task>13824</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8020000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2018-01-23T01:13:22.594362700Z"/>' +\
    '<EventRecordID>17</EventRecordID>' +\
    '<Correlation ActivityID="{59F9FAA3-93E7-0006-E2FA-F959E793D301}"/>' +\
    '<Execution ProcessID="744" ThreadID="748"/>' +\
    '<Channel>Security</Channel>' +\
    '<Computer>DESKTOP-BPKOOQH</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="TargetUserName">WDAGUtilityAccount</Data>' +\
    '<Data Name="TargetDomainName">DESKTOP-BPKOOQH</Data>' +\
    '<Data Name="TargetSid">S-1-5-21-888870700-3316484737-701128759-504</Data>' +\
    '<Data Name="SubjectUserSid">S-1-5-18</Data>' +\
    '<Data Name="SubjectUserName">DESKTOP-BPKOOQH$</Data>' +\
    '<Data Name="SubjectDomainName">WORKGROUP</Data>' +\
    '<Data Name="SubjectLogonId">0x00000000000003e7</Data>' +\
    '<Data Name="PrivilegeList">-</Data>' +\
    '<Data Name="SamAccountName">WDAGUtilityAccount</Data>' +\
    '<Data Name="DisplayName">%%1793</Data>' +\
    '<Data Name="UserPrincipalName">-</Data>' +\
    '<Data Name="HomeDirectory">%%1793</Data>' +\
    '<Data Name="HomePath">%%1793</Data>' +\
    '<Data Name="ScriptPath">%%1793</Data>' +\
    '<Data Name="ProfilePath">%%1793</Data>' +\
    '<Data Name="UserWorkstations">%%1793</Data>' +\
    '<Data Name="PasswordLastSet">%%1794</Data>' +\
    '<Data Name="AccountExpires">%%1794</Data>' +\
    '<Data Name="PrimaryGroupId">513</Data>' +\
    '<Data Name="AllowedToDelegateTo">-</Data>' +\
    '<Data Name="OldUacValue">0x0</Data>' +\
    '<Data Name="NewUacValue">0x15</Data>' +\
    '<Data Name="UserAccountControl">%%2080%%2082%%2084</Data>' +\
    '<Data Name="UserParameters">%%1793</Data>' +\
    '<Data Name="SidHistory">-</Data>' +\
    '<Data Name="LogonHours">%%1797</Data>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_4720(d, rec)  # Security  -   Account Created
    assert(record["account"]) == "DESKTOP-BPKOOQH$"
    assert(record["description"]) == "Account Created"
    assert(record["details"]) == "New account name: WDAGUtilityAccount (RID 04) was created by user account (DESKTOP-BPKOOQH$)"
    assert(record["session_id"]) == "0x00000000000003e7"


# def test_parser_id_4722(): # Do not have
#     xmlInput = ""
#     d = xmltodict.parse(xmlInput)
#     sys = d['Event']['System']
#     rec = {'timestamp_utc': sys['TimeCreated']['@SystemTime'],
#            'event_id': sys['EventID'],
#            'description': '',
#            'details': '',
#            'event_source': sys['Provider']['@Name'],
#            'event_log': sys['Channel'],
#            'session_id': '',
#            'account': '',
#            'computer_name': sys['Computer'],
#            'record_number': sys['EventRecordID'],
#            'recovered': True,
#            'alias': 'Sample'
#            }
#     record = parser.parse_id_4722(d, rec)  # Security  -   Account Enabled
#     data = d["Event"]["EventData"]["Data"]
#     assert (record["account"]) == data[4]["#text"]
#     assert (record["description"]) == "Account Enabled"
#     assert (record["details"]) == f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
#                                   f'was enabled by user account ({data[4]["#text"]})'
#     assert (record["session_id"]) == data[6]["#text"]


# def test_parser_id_4723(): # Do not have
#     xmlInput = ""
#     d = xmltodict.parse(xmlInput)
#     sys = d['Event']['System']
#     rec = {'timestamp_utc': sys['TimeCreated']['@SystemTime'],
#            'event_id': sys['EventID'],
#            'description': '',
#            'details': '',
#            'event_source': sys['Provider']['@Name'],
#            'event_log': sys['Channel'],
#            'session_id': '',
#            'account': '',
#            'computer_name': sys['Computer'],
#            'record_number': sys['EventRecordID'],
#            'recovered': True,
#            'alias': 'Sample'
#            }
#     record = parser.parse_id_4723(d, rec)  # Security  -   User Changed Password
#     data = d["Event"]["EventData"]["Data"]
#     assert (record["account"]) == data[4]["#text"]
#     assert (record["description"]) == "User Changed Password"
#     assert (record["details"]) == f'The password of user account {data[0]["#text"]} ' \
#                                   f'(RID {data[2]["#text"][41:45]}) was changed by the user ({data[4]["#text"]})'
#     assert (record["session_id"]) == data[6]["#text"]


# def test_parser_id_4724(): # Do not have
#     xmlInput = ""
#     d = xmltodict.parse(xmlInput)
#     sys = d['Event']['System']
#     rec = {'timestamp_utc': sys['TimeCreated']['@SystemTime'],
#            'event_id': sys['EventID'],
#            'description': '',
#            'details': '',
#            'event_source': sys['Provider']['@Name'],
#            'event_log': sys['Channel'],
#            'session_id': '',
#            'account': '',
#            'computer_name': sys['Computer'],
#            'record_number': sys['EventRecordID'],
#            'recovered': True,
#            'alias': 'Sample'
#            }
#     record = parser.parse_id_4724(d, rec)  # Security  -   Privileged User Reset Password
#     data = d["Event"]["EventData"]["Data"]
#     assert (record["account"]) == data[4]["#text"]
#     assert (record["description"]) == "Privileged User Reset Password"
#     assert (record["details"]) == f'The password of user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
#                                   f'was reset by a privileged user account ({data[4]["#text"]})'
#     assert (record["session_id"]) == data[6]["#text"]


# def test_parser_id_4725(): # Do not have
#     xmlInput = ""
#     d = xmltodict.parse(xmlInput)
#     sys = d['Event']['System']
#     rec = {'timestamp_utc': sys['TimeCreated']['@SystemTime'],
#            'event_id': sys['EventID'],
#            'description': '',
#            'details': '',
#            'event_source': sys['Provider']['@Name'],
#            'event_log': sys['Channel'],
#            'session_id': '',
#            'account': '',
#            'computer_name': sys['Computer'],
#            'record_number': sys['EventRecordID'],
#            'recovered': True,
#            'alias': 'Sample'
#            }
#     record = parser.parse_id_4725(d, rec)  # Security  -   Account Disabled
#     data = d["Event"]["EventData"]["Data"]
#     assert(record["account"]) == data[4]["#text"]
#     assert(record["description"]) == "Account Disabled"
#     assert(record["details"]) == f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
#                         f'was disabled by user account ({data[4]["#text"]})'
#     assert(record["session_id"]) == data[6]["#text"]


# def test_parser_id_4726(): # Do not have
#     xmlInput = ""
#     d = xmltodict.parse(xmlInput)
#     sys = d['Event']['System']
#     rec = {'timestamp_utc': sys['TimeCreated']['@SystemTime'],
#            'event_id': sys['EventID'],
#            'description': '',
#            'details': '',
#            'event_source': sys['Provider']['@Name'],
#            'event_log': sys['Channel'],
#            'session_id': '',
#            'account': '',
#            'computer_name': sys['Computer'],
#            'record_number': sys['EventRecordID'],
#            'recovered': True,
#            'alias': 'Sample'
#            }
#     record = parser.parse_id_4726(d, rec)  # Security  -   Account Deleted
#     data = d["Event"]["EventData"]["Data"]
#     assert(record["account"]) == data[4]["#text"]
#     assert(record["description"]) == "Account Deleted"
#     assert(record["details"]) == f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
#                         f'was deleted by user account ({data[4]["#text"]})'
#     assert(record["session_id"]) == data[6]["#text"]


# def test_parser_id_6008(): # Do not have
#     xmlInput = ""
#     d = xmltodict.parse(xmlInput)
#     sys = d['Event']['System']
#     rec = {'timestamp_utc': sys['TimeCreated']['@SystemTime'],
#            'event_id': sys['EventID'],
#            'description': '',
#            'details': '',
#            'event_source': sys['Provider']['@Name'],
#            'event_log': sys['Channel'],
#            'session_id': '',
#            'account': '',
#            'computer_name': sys['Computer'],
#            'record_number': sys['EventRecordID'],
#            'recovered': True,
#            'alias': 'Sample'
#            }
#     record = parser.parse_id_6008(d, rec)  # System    -   Shutdown Error
#     assert(record["description"]) == "Shutdown Error"


def test_parser_id_6013(): # Do not have
    xmlInput = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="EventLog"/>' +\
    '<EventID Qualifiers="32768">6013</EventID>' +\
    '<Level>4</Level>' +\
    '<Task>0</Task>' +\
    '<Keywords>0x0080000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2018-02-04T20:19:48.217770800Z"/>' +\
    '<EventRecordID>12140</EventRecordID>' +\
    '<Channel>System</Channel>' +\
    '<Computer>CARTER-LAPTOP</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data/>' +\
    '<Data/>' +\
    '<Data/>' +\
    '<Data/>' +\
    '<Data>2349980</Data>' +\
    '<Data>60</Data>' +\
    '<Data>480 Pacific Standard Time</Data>' +\
    '<Binary>31002E003100000030000000570069006E0064006F007700730020003100300020005' \
    '00072006F000000310030002E0030002E003100360032003900390020004200750069006C0064' \
    '002000310036003200390039002000200000004D0075006C0074006900700072006F006300650' \
    '0730073006F007200200046007200650065000000310036003200390039002E00720073003300' \
    '5F00720065006C0065006100730065002E003100370030003900320038002D003100350033003' \
    '40000003500390065003000360062003500630000004E006F007400200041007600610069006C' \
    '00610062006C00650000004E006F007400200041007600610069006C00610062006C006500000' \
    '03900000038000000380030003100340000003400300039000000430041005200540045005200' \
    '2D004C004100500054004F00500000000000</Binary>' +\
    '</EventData>' +\
    '</Event>'
    d = xmltodict.parse(xmlInput)
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
    record = parser.parse_id_6013(d, rec)  # System    -   System Status
    assert(record["account"]) == "SYSTEM"
    assert(record["description"]) == "System Status"
    assert(record["details"]) == "System Uptime: 2349980 seconds. Time Zone Setting: 480 Pacific Standard Time."


def test_parse_unwanted():
    xmlUnwanted = '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">' +\
    '<System>' +\
    '<Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-A5BA-3E3B0328C30D}"/>' +\
    '<EventID>4826</EventID>' +\
    '<Version>0</Version>' +\
    '<Level>0</Level>' +\
    '<Task>13573</Task>' +\
    '<Opcode>0</Opcode>' +\
    '<Keywords>0x8020000000000000</Keywords>' +\
    '<TimeCreated SystemTime="2018-01-23T01:13:21.021327600Z"/>' +\
    '<EventRecordID>1</EventRecordID>' +\
    '<Correlation/>' +\
    '<Execution ProcessID="4" ThreadID="208"/>' +\
    '<Channel>Security</Channel>' +\
    '<Computer>DESKTOP-BPKOOQH</Computer>' +\
    '<Security/>' +\
    '</System>' +\
    '<EventData>' +\
    '<Data Name="SubjectUserSid">S-1-5-18</Data>' +\
    '<Data Name="SubjectUserName">-</Data>' +\
    '<Data Name="SubjectDomainName">-</Data>' +\
    '<Data Name="SubjectLogonId">0x00000000000003e7</Data>' +\
    '<Data Name="LoadOptions">-</Data>' +\
    '<Data Name="AdvancedOptions">%%1843</Data>' +\
    '<Data Name="ConfigAccessPolicy">%%1846</Data>' +\
    '<Data Name="RemoteEventLogging">%%1843</Data>' +\
    '<Data Name="KernelDebug">%%1843</Data>' +\
    '<Data Name="VsmLaunchType">%%1848</Data>' +\
    '<Data Name="TestSigning">%%1843</Data>' +\
    '<Data Name="FlightSigning">%%1843</Data>' +\
    '<Data Name="DisableIntegrityChecks">%%1843</Data>' +\
    '<Data Name="HypervisorLoadOptions">-</Data>' +\
    '<Data Name="HypervisorLaunchType">%%1848</Data>' +\
    '<Data Name="HypervisorDebug">%%1843</Data>' +\
    '</EventData>' +\
    '</Event>'
    try:
        d = xmltodict.parse(xmlUnwanted)
    except ExpatError:
        xmlUnwanted = xmlUnwanted.replace("\x00", "")  # This can not be the best way to do this...
        d = xmltodict.parse(xmlUnwanted)
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
    assert(parser.parser(d, rec)) is None


def test_parse_wanted():
    xmlWanted = '<Event xmlns = "http://schemas.microsoft.com/win/2004/08/events/event">' + \
               '<System>' + \
               '<Provider Name="Microsoft-Windows-Kernel-General" Guid="{A68CA8B7-004F-D7B6-A698-07E2DE0F1F5D}"/>' + \
               '<EventID>1</EventID>' + \
               '<Version>1</Version>' + \
               '<Level>4</Level>' + \
               '<Task>5</Task>' + \
               '<Opcode>0</Opcode>' + \
               '<Keywords>0x8000000000000010</Keywords>' + \
               '<TimeCreated SystemTime="2017-01-02T00:28:02.499911900Z"/>' + \
               '<EventRecordID>521</EventRecordID>' + \
               '<Correlation/>' + \
               '<Execution ProcessID="4" ThreadID="372"/>' + \
               '<Channel>System</Channel>' + \
               '<Computer>LAPTOP-9KUQNI2Q</Computer>' + \
               '<Security/>' + \
               '</System>' + \
               '<EventData>' + \
               '<Data Name="NewTime">2017-01-02T00:28:02.500000000Z</Data>' + \
               '<Data Name="OldTime">2017-01-01T22:19:39.790389600Z</Data>' + \
               '<Data Name="Reason">2</Data>' + \
               '</EventData>' + \
               '</Event>'
    d = xmltodict.parse(xmlWanted)
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
    assert(parser.parser(d, rec)) is not None


# def test_parser():
#     for record in records:
#         try:
#             d = xmltodict.parse(record)
#         except ExpatError:
#             record = record.replace("\x00", "")  # This can not be the best way to do this...
#             d = xmltodict.parse(record)
#
#         sys = d['Event']['System']
#
#         rec = {'timestamp_utc': sys['TimeCreated']['@SystemTime'],
#                'event_id': sys['EventID'],
#                'description': '',
#                'details': '',
#                'event_source': sys['Provider']['@Name'],
#                'event_log': sys['Channel'],
#                'session_id': '',
#                'account': '',
#                'computer_name': sys['Computer'],
#                'record_number': sys['EventRecordID'],
#                'recovered': True,
#                'alias': 'Sample'
#                }
#
#         try:
#             event_id = rec["event_id"]["#text"]
#         except TypeError:
#             event_id = rec["event_id"]
#
#
#         if event_id == "1074":
#             data = d["Event"]["EventData"]["Data"]
#             if data[3]["#text"] == "0x500ff":
#                 print(record)
#                 break
#
#         if event_id == "4722": # Do not have
#             print(record)
#             break
#
#         if event_id == "4723": # Do not have
#             print(record)
#             break
#
#         if event_id == "4724": # Do not have
#             print(record)
#             break
#
#         if event_id == "4725": # Do not have
#             print(record)
#             break
#
#         if event_id == "4726": # Do not have
#             print(record)
#             break
#
#         if event_id == "6008": # Do not have
#             print(record)
#             break
#
#         if event_id == "6013": # Do not have
#             print(record)
#             break