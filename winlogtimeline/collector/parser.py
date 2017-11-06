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

    """
    session_id = None
    if event_log == "Security":
        try:
            data = event["EventData"]["Data"]
        except:
            continue

        for item in data:
            if item["@Name"] == "TargetLogonId":
                session_id = item["#text"]
    """


def parse_id_1(raw, record):
    record["description"] = "Wake Up"
    return record


def parse_id_12(raw, record):
    record["description"] = "System Start"
    return record


def parse_id_13(raw, record):
    record["description"] = "System Shutdown"
    return record


def parse_id_41(raw, record):
    record["description"] = "Shutdown Error"
    return record


def parse_id_42(raw, record):
    record["description"] = "Sleep Mode"
    return record


def parse_id_104(raw, record):
    record["description"] = "Log Cleared"
    return record


def parse_id_1074(raw, record):
    record["description"] = "Shutdown Initiated"
    return record


def parse_id_1102(raw, record):
    record["description"] = "Log Cleared"
    return record


def parse_id_4616(raw, record):
    record["description"] = "Time Change"
    return record


def parse_id_4624(raw, record):
    record["description"] = "Logon Events"
    return record


def parse_id_4634(raw, record):
    record["description"] = "Logoff (Network Connection)"
    return record


def parse_id_4647(raw, record):
    record["description"] = "User-Initiated Logoff"
    return record


def parse_id_4720(raw, record):
    record["description"] = "Account Created"
    return record


def parse_id_4722(raw, record):
    record["description"] = "Account Enabled"
    return record


def parse_id_4723(raw, record):
    record["description"] = "User Changed Password"
    return record


def parse_id_4724(raw, record):
    record["description"] = "Privileged User Reset Password"
    return record


def parse_id_4725(raw, record):
    record["description"] = "Account Disabled"
    return record


def parse_id_4726(raw, record):
    record["description"] = "Account Deleted"
    return record


def parse_id_6008(raw, record):
    record["description"] = "Shutdown Error"
    return record


def parse_id_6013(raw, record):
    record["description"] = "System Status"
    return record
