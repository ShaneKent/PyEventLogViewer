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

    sleep_time = get_string(data[0])
    wake_time = get_string(data[1])

    record["account"] = "SYSTEM"
    record["description"] = "Wake Up"
    record["details"] = f'Wake Time: {wake_time[0:11]} {wake_time[11:23]} (UTC) | Sleep Start Time: ' \
                        f'{sleep_time[0:11]} {sleep_time[11:23]} (UTC)'

    return record


def parse_id_12(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "System Start"

    if len(data) == 7:
        time = get_string(data[6])
        record[
            "details"] = f'Starting Windows NT version {get_string(data[0])}. {get_string(data[1])}. {get_string(data[2])} ' \
                         f'at {time[0:10]} {time[11:23]} (UTC)'

    return record


def parse_id_13(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    time = get_string(data)

    record["account"] = "SYSTEM"
    record["description"] = "System Shutdown"
    record["details"] = f'Shutdown Time: {time[0:10]} {time[11:23]} (UTC)'

    return record


def parse_id_41(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "Shutdown Error"

    return record


def parse_id_42(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "Sleep Mode"
    reason = get_string(data[2])

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
    data = raw["Event"]["UserData"]["LogFileCleared"]

    record["account"] = data["SubjectUserName"]
    record["description"] = "Log Cleared"
    record[
        "details"] = f'System event log was cleared by the following account: {data["SubjectDomainName"]}\\{data["Channel"]}'

    return record


def parse_id_1074(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[6]).split("\\")[-1]
    if get_string(data[3]) == "0x500ff":
        record["description"] = "Shutdown Initiated"
    else:
        # record["description"] = "ERROR"
        return None

    record["details"] = f'Cause: {get_string(data[4])}'
    record["computer_name"] = get_string(data[1])

    return record


def parse_id_1102(raw, record):
    data = raw["Event"]["UserData"]["LogFileCleared"]

    record["description"] = "Log Cleared"
    record["account"] = data["SubjectUserSid"]
    record["details"] = f'Security event log was cleared by the following account: ' \
                        f'{data["SubjectUserSid"]}\\{data["SubjectDomainName"]}'
    record["session_id"] = data["SubjectLogonId"]

    return record


def parse_id_4616(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    new = get_string(data[5])
    old = get_string(data[4])

    record["description"] = "Time Change"
    record["account"] = get_string(data[1])
    record["details"] = f'Changed To: {new[0:10]} {new[11:23]} (UTC) | ' \
                        f'Previous Time: {old[0:10]} {old[11:23]} (UTC)'

    return record


def parse_id_4624(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[5])
    record["session_id"] = get_string(data[7])
    reason = get_string(data[8])

    if reason == "2":
        record["description"] = "Interactive Logon"
    elif reason == "3":
        record["description"] = "Network Connection"

        user = data[11]
        try:
            user = get_string(user)
        except:
            user = user["@Name"]

        record["details"] = f'From: {user} ({get_string(data[18])}) using ' \
                            f'{get_string(data[10])} auth as {get_string(data[6])}\\{get_string(data[5])}'
    elif reason == "7":
        record["description"] = "Unlock Workstation"
    elif reason == "10":
        record["description"] = "Remote Interactive Logon"
        record["details"] = f'From: {get_string(data[18])} using {get_string(data[10])} auth as ' \
                            f'{get_string(data[6])}\\{get_string(data[5])}'
    elif reason == "11":
        record["description"] = "Interactive Logon"
        record["details"] = f'Logon as {get_string(data[6])}\\{get_string(data[5])} using cached credentials'
    else:
        return None

    if record["account"] == "ANONYMOUS LOGON":
        return None

    return record


def parse_id_4634(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["session_id"] = get_string(data[3])
    record["account"] = get_string(data[1])
    record["description"] = "Logoff"

    t = get_string(data[4])
    if t == "2":
        record["details"] = "Logoff from Interactive session"
    elif t == "3":
        record["details"] = "End of Network Connection session"
    elif t == "7":
        record["details"] = "Unlock Workstation"
    elif t == "10":
        record["details"] = "Logoff from Remote Interactive Session"
    else:
        # record["details"] = "EXCLUDED"
        return None

    if record["account"] == "ANONYMOUS LOGON":
        return None

    return record


def parse_id_4647(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[1])
    record["description"] = "User Initiated Logoff"
    record["session_id"] = get_string(data[3])

    return record


def parse_id_4720(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[4])
    record["description"] = "Account Created"
    record["details"] = f'New account name: {get_string(data[0])} (RID {get_string(data[2])[41:45]}) ' \
                        f'was created by user account ({get_string(data[4])})'
    record["session_id"] = get_string(data[6])

    return record


def parse_id_4722(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[4])
    record["description"] = "Account Enabled"
    record["details"] = f'The user account {get_string(data[0])} (RID {get_string(data[2])[41:45]}) ' \
                        f'was enabled by user account ({get_string(data[4])})'
    record["session_id"] = get_string(data[6])

    return record


def parse_id_4723(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[4])
    record["description"] = "User Changed Password"
    record["details"] = f'The password of user account {get_string(data[0])} (RID {get_string(data[2])[41:45]}) ' \
                        f'was changed by the user ({get_string(data[4])})'
    record["session_id"] = get_string(data[6])

    return record


def parse_id_4724(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[4])
    record["description"] = "Privileged User Reset Password"
    record["details"] = f'The password of user account {get_string(data[0])} (RID {get_string(data[2])[41:45]}) ' \
                        f'was reset by a privileged user account ({get_string(data[4])})'
    record["session_id"] = get_string(data[6])

    return record


def parse_id_4725(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[4])
    record["description"] = "Account Disabled"
    record["details"] = f'The user account {get_string(data[0])} (RID {get_string(data[2])[41:45]}) ' \
                        f'was disabled by user account ({get_string(data[4])})'
    record["session_id"] = get_string(data[6])

    return record


def parse_id_4726(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = get_string(data[4])
    record["description"] = "Account Deleted"
    record["details"] = f'The user account {get_string(data[0])} (RID {get_string(data[2])[41:45]}) ' \
                        f'was deleted by user account ({get_string(data[4])})'
    record["session_id"] = get_string(data[6])

    return record


def parse_id_6008(raw, record):
    record["description"] = "Shutdown Error"

    return record


def parse_id_6013(raw, record):
    data = raw["Event"]["EventData"]["Data"]

    record["account"] = "SYSTEM"
    record["description"] = "System Status"

    uptime = get_string(data[4])
    timezone = get_string(data[6])

    record["details"] = f'System Uptime: {uptime} seconds. Time Zone Setting: {timezone}.'

    return record


def get_string(string):
    if isinstance(string, str):
        return string
    return string["#text"]
