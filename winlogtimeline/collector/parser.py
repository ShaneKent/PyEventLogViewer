def parser(raw, record):
    # record["description"]
    # record["details"]
    # record["session_id"]
    # record["account"]

    event_id = record["event_id"]

    if event_id == "1":
        record = parse_id_1(raw, record)  # System    -   Wake Up
    elif event_id == "12":
        record = parse_id_12(raw, record)  # System    -   System Start
    elif event_id == "13":
        record = parse_id_13(raw, record)  # System    -   System Shutdown
    elif event_id == "41":
        record = parse_id_41(raw, record)  # System    -   Shutdown Error
    elif event_id == "42":
        record = parse_id_42(raw, record)  # System    -   Sleep Mode
    elif event_id == "104":
        record = parse_id_104(raw, record)  # System    -   Log Cleared
    elif event_id == "1074":
        record = parse_id_1074(raw, record)  # System    -   Shutdown Initiated
    elif event_id == "1102":
        record = parse_id_1102(raw, record)  # Security  -   Log Cleared
    elif event_id == "4616":
        record = parse_id_4616(raw, record)  # System    -   Time Change
    elif event_id == "4624":
        record = parse_id_4624(raw, record)  # System    -   Logon Events
    elif event_id == "4634":
        record = parse_id_4634(raw, record)  # Security  -   Logoff (Network Connection)
    elif event_id == "4647":
        record = parse_id_4647(raw, record)  # Security  -   User-Initiated Logoff
    elif event_id == "4720":
        record = parse_id_4720(raw, record)  # Security  -   Account Created
    elif event_id == "4722":
        record = parse_id_4722(raw, record)  # Security  -   Account Enabled
    elif event_id == "4723":
        record = parse_id_4723(raw, record)  # Security  -   User Changed Password
    elif event_id == "4724":
        record = parse_id_4724(raw, record)  # Security  -   Privileged User Reset Password
    elif event_id == "4725":
        record = parse_id_4725(raw, record)  # Security  -   Account Disabled
    elif event_id == "4726":
        record = parse_id_4726(raw, record)  # Security  -   Account Deleted
    elif event_id == "6008":
        record = parse_id_6008(raw, record)  # System    -   Shutdown Error
    elif event_id == "6013":
        record = parse_id_6013(raw, record)  # System    -   System Status
    else:
        record = None  # EventID isn't being tracked.

    return record


def parse_id_1(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "Wake Up"
    record["details"] = f'Wake Time: {data[1]["#text"][0:11]} {data[1]["#text"][11:23]} (UTC) | Sleep Start Time: ' \
                        f'{data[0]["#text"][0:11]} {data[0]["#text"][11:23]} (UTC)'

    return record


def parse_id_12(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "System Start"

    if len(data) == 7:
        # print(data)
        record["details"] = f'Starting Windows NT version {data[0]["#text"]}. {data[1]["#text"]}. {data[2]["#text"]} ' \
                            f'at {data[6]["#text"][0:10]} {data[6]["#text"][11:23]} (UTC)'

    return record


def parse_id_13(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "System Shutdown"
    record["details"] = f'Shutdown Time: {data["#text"][0:10]} {data["#text"][11:23]} (UTC)'

    return record


def parse_id_41(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "Shutdown Error"

    #print("Message", data)

    return record


def parse_id_42(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "Sleep Mode"
    reason = data[2]["#text"]

    if reason == "0":
        record["details"] = "Starting Sleep Mode. Reason: Power button/Close lid"
    elif reason == "2":
        record["details"] = "Starting Sleep Mode. Reason: Low battery"
    elif reason == "4":
        record["details"] = "Starting Sleep Mode. Reason: Application"
    elif reason == "7":
        record["details"] = "Starting Sleep Mode. Reason: System idle"
    else:
        record["details"] = "Starting Sleep Mode. Reason: Undefined*"

    return record


def parse_id_104(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[0]["#text"]
    record["description"] = "Log Cleared"
    record["details"] = f'System event log was cleared by the following account: {data[1]["#text"]}\\{data[0]["#text"]}'

    return record


def parse_id_1074(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[6]["#text"].split("\\")[-1]
    if data[3]["#text"] == "0x500ff":
        record["description"] = "Shutdown Initiated"
    else:
        record["description"] = "ERROR"
    record["details"] = f'Cause: {data[4]["#text"]}'
    record["computer_name"] = data[1]["#text"]

    return record


def parse_id_1102(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["description"] = "Log Cleared"
    record["account"] = data[1]["#text"]
    record["details"] = f'Security event log was cleared by the following account: ' \
                        f'{data[2]["#text"]}\\{data[1]["#text"]}'
    record["session_id"] = data[3]["#text"]

    return record


def parse_id_4616(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["description"] = "Time Change"
    record["account"] = data[1]["#text"]
    record["details"] = f'Changed To: {data[5]["#text"][0:10]} {data[5]["#text"][11:23]} (UTC) | ' \
                        f'Previous Time: {data[4]["#text"][0:10]} {data[4]["#text"][11:23]} (UTC)'

    return record


def parse_id_4624(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[5]["#text"]
    reason = data[8]["#text"]

    if reason == "2":
        record["description"] = "Interactive Logon"
    elif reason == "3":
        record["description"] = "Network Connection"
        try:
            record["details"] = f'From: {data[11]["#text"]} ({data[18]["#text"]}) using ' \
                                f'{data[10]["#text"]} auth as {data[6]["#text"]}\\{data[5]["#text"]}'
        except:
            record["details"] = f'From: {data[11]["@Name"]} ({data[18]["#text"]}) using ' \
                                f'{data[10]["#text"]} auth as {data[6]["#text"]}\\{data[5]["#text"]}'
    elif reason == "7":
        record["description"] = "Unlock Workstation"
    elif reason == "10":
        record["description"] = "Remote Interactive Logon"
        record["details"] = f'From: {data[18]["#text"]} using {data[10]["#text"]} auth as ' \
                            f'{data[6]["#text"]}\\{data[5]["#text"]}'
    elif reason == "11":
        record["description"] = "Interactive Logon"
        record["details"] = f'Logon as {data[6]["#text"]}\\{data[5]["#text"]} using cached credentials'

    record["session_id"] = data[7]["#text"]

    return record


def parse_id_4634(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[4]["#text"]
    record["description"] = "Logoff"

    if data[4]["#text"] == "3":
        record["details"] = "End of Network Connection session"
    else:
        record["details"] = "EXCLUDED"

    record["session_id"] = data[3]["#text"]

    return record


def parse_id_4647(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[1]["#text"]
    record["description"] = "User Initiated Logoff"
    record["session_id"] = data[3]["#text"]

    return record


def parse_id_4720(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[4]["#text"]
    record["description"] = "Account Created"
    record["details"] = f'New account name: {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                        f'was created by user account ({data[4]["#text"]})'
    record["session_id"] = data[6]["#text"]

    return record


def parse_id_4722(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[4]["#text"]
    record["description"] = "Account Enabled"
    record["details"] = f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                        f'was enabled by user account ({data[4]["#text"]})'
    record["session_id"] = data[6]["#text"]
    return record


def parse_id_4723(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[4]["#text"]
    record["description"] = "User Changed Password"
    record["details"] = f'The password of user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                        f'was changed by the user ({data[4]["#text"]})'
    record["session_id"] = data[6]["#text"]
    return record


def parse_id_4724(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[4]["#text"]
    record["description"] = "Privileged User Reset Password"
    record["details"] = f'The password of user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                        f'was reset by a privileged user account ({data[4]["#text"]})'
    record["session_id"] = data[6]["#text"]
    return record


def parse_id_4725(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[4]["#text"]
    record["description"] = "Account Disabled"
    record["details"] = f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                        f'was disabled by user account ({data[4]["#text"]})'
    record["session_id"] = data[6]["#text"]
    return record


def parse_id_4726(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = data[4]["#text"]
    record["description"] = "Account Deleted"
    record["details"] = f'The user account {data[0]["#text"]} (RID {data[2]["#text"][41:45]}) ' \
                        f'was deleted by user account ({data[4]["#text"]})'
    record["session_id"] = data[6]["#text"]
    return record


def parse_id_6008(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    #print("Message", data)

    record["description"] = "Shutdown Error"
    return record


def parse_id_6013(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "System Status"
    record["details"] = f'System Uptime: {data[4]["#text"]} seconds. Time Zone Setting: {data[6]["#text"]}.'

    return record
