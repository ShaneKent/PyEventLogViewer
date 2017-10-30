from pprint import PrettyPrinter


def parser(record, object):
    # object["description"]
    # object["details"]
    # object["session_id"]
    # object["account"]

    event_id = object["event_id"]

    if event_id == "1":
        object = parse_id_1(record, object)  # System    -   Wake Up
    elif event_id == "12":
        object = parse_id_12(record, object)  # System    -   System Start
    elif event_id == "13":
        object = parse_id_13(record, object)  # System    -   System Shutdown
    elif event_id == "41":
        object = parse_id_41(record, object)  # System    -   Shutdown Error
    elif event_id == "42":
        object = parse_id_42(record, object)  # System    -   Sleep Mode
    elif event_id == "104":
        object = parse_id_104(record, object)  # System    -   Log Cleared
    elif event_id == "1074":
        object = parse_id_1074(record, object)  # System    -   Shutdown Initiated
    elif event_id == "1102":
        object = parse_id_1102(record, object)  # Security  -   Log Cleared
    elif event_id == "4616":
        object = parse_id_4616(record, object)  # System    -   Time Change
    elif event_id == "4624":
        object = parse_id_4624(record, object)  # System    -   Logon Events
    elif event_id == "4634":
        object = parse_id_4634(record, object)  # Security  -   Logoff (Network Connection)
    elif event_id == "4647":
        object = parse_id_4647(record, object)  # Security  -   User-Initiated Logoff
    elif event_id == "4720":
        object = parse_id_4720(record, object)  # Security  -   Account Created
    elif event_id == "4722":
        object = parse_id_4722(record, object)  # Security  -   Account Enabled
    elif event_id == "4723":
        object = parse_id_4723(record, object)  # Security  -   User Changed Password
    elif event_id == "4724":
        object = parse_id_4724(record, object)  # Security  -   Privileged User Reset Password
    elif event_id == "4725":
        object = parse_id_4725(record, object)  # Security  -   Account Disabled
    elif event_id == "4726":
        object = parse_id_4726(record, object)  # Security  -   Account Deleted
    elif event_id == "6008":
        object = parse_id_6008(record, object)  # System    -   Shutdown Error
    elif event_id == "6013":
        object = parse_id_6013(record, object)  # System    -   System Status
    else:
        object = None  # EventID isn't being tracked.

    return object

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


def parse_id_1(record, object):
    object["description"] = "Wake Up"
    return object


def parse_id_12(record, object):
    object["description"] = "System Start"
    return object


def parse_id_13(record, object):
    object["description"] = "System Shutdown"
    return object


def parse_id_41(record, object):
    object["description"] = "Shutdown Error"
    return object


def parse_id_42(record, object):
    object["description"] = "Sleep Mode"
    return object


def parse_id_104(record, object):
    object["description"] = "Log Cleared"
    return object


def parse_id_1074(record, object):
    object["description"] = "Shutdown Initiated"
    return object


def parse_id_1102(record, object):
    object["description"] = "Log Cleared"
    return object


def parse_id_4616(record, object):
    object["description"] = "Time Change"
    return object


def parse_id_4624(record, object):
    object["description"] = "Logon Events"
    return object


def parse_id_4634(record, object):
    object["description"] = "Logoff (Network Connection)"
    return object


def parse_id_4647(record, object):
    object["description"] = "User-Initiated Logoff"
    return object


def parse_id_4720(record, object):
    object["description"] = "Account Created"
    return object


def parse_id_4722(record, object):
    object["description"] = "Account Enabled"
    return object


def parse_id_4723(record, object):
    object["description"] = "User Changed Password"
    return object


def parse_id_4724(record, object):
    object["description"] = "Privileged User Reset Password"
    return object


def parse_id_4725(record, object):
    object["description"] = "Account Disabled"
    return object


def parse_id_4726(record, object):
    object["description"] = "Account Deleted"
    return object


def parse_id_6008(record, object):
    object["description"] = "Shutdown Error"
    return object


def parse_id_6013(record, object):
    object["description"] = "System Status"
    return object
