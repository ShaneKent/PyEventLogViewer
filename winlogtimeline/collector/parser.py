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
        record["details"] = f'Starting Windows NT version {get_string(data[0])}. {get_string(data[1])}. ' \
                            f'{get_string(data[2])} at {time[0:10]} {time[11:23]} (UTC)'

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
    record["details"] = f'System event log was cleared by the following account: ' \
                        f'{data["SubjectDomainName"]}\\{data["Channel"]}'

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

        u = data[11]
        try:
            user = get_string(u)
        except (ValueError, TypeError):
            user = u["@Name"]

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


def parse_id_20001(raw, record):
    data = raw['Event']['UserData']['InstallDeviceID']

    record['description'] = "Device installation completed"

    driver = data['DriverName']
    device_id = data['DeviceInstanceID']
    status = data['InstallStatus']

    record['details'] = (f'Driver Management concluded the process to install driver {driver} for Device Instance ID '
                         f'{device_id} with the following status: {status}')

    return record


def parse_id_20003(raw, record):
    data = raw['Event']['UserData']['AddServiceID']

    record['description'] = 'Service installation complete'

    service = data['ServiceName']
    device_id = data['DeviceInstanceID']
    status = data['AddServiceStatus']

    record['details'] = (f'Driver Management has concluded the process to add Service {service} for Device Instance ID '
                         f'{device_id} with the following status: {status}')
    return record


parsers = {
    'Microsoft-Windows-Power-Troubleshooter': {
        '1': parse_id_1,  # [System] Wake Up
    },
    'Microsoft-Windows-Kernel-General': {
        '12': parse_id_12,  # [System] System Start
        '13': parse_id_13,  # [System] System Shutdown
    },
    'Microsoft-Windows-Kernel-Power': {
        '41': parse_id_41,  # [System] Shutdown Error
        '42': parse_id_42,  # [System] Sleep Mode
    },
    'Microsoft-Windows-Eventlog': {
        '104': parse_id_104,  # [System] Log Cleared
        '1102': parse_id_1102,  # [Security] Log Cleared
    },
    'User32': {
        '1074': parse_id_1074,  # [System] Shutdown Initiated
    },
    'Microsoft-Windows-Security-Auditing': {
        '4616': parse_id_4616,  # [System] Time Change
        '4624': parse_id_4624,  # [System] Logon Events
        '4634': parse_id_4634,  # [Security] Logoff (Network Connection)
        '4647': parse_id_4647,  # [Security] User-Initiated Logoff
        '4720': parse_id_4720,  # [Security] Account Created
        '4722': parse_id_4722,  # [Security] Account Enabled
        '4723': parse_id_4723,  # [Security] User Changed Password
        '4724': parse_id_4724,  # [Security] Privileged User Reset Password
        '4725': parse_id_4725,  # [Security] Account Disabled
        '4726': parse_id_4726,  # [Security] Account Deleted
    },
    'EventLog': {
        '6008': parse_id_6008,  # [System] Shutdown Error
        '6013': parse_id_6013,  # [System] System Status
    },
    'Microsoft-Windows-UserPnp': {
        '20001': parse_id_20001,  # [System] Device Installation
        '20003': parse_id_20003,  # [System] Service Installation
    }
}


def user_parser(raw, record):
    """
    This is the parser used when a record is parsed because the user specified it. Records that have a built-in parser
    will not be passed to this method.
    :param raw:
    :param record:
    :return:
    """
    record['description'] = 'User defined event. Double-click to view XML.'

    return record


def parser(raw, record, user_parsers):
    parse_record = parsers.get(record['event_source'], {}).get(record['event_id'], None)

    if parse_record is None:
        if record['event_id'] in user_parsers.get(record['event_source'], []):
            parse_record = user_parser

    if get_event_data_section(raw) is False:
        print('NOTE: A corrupted record was almost parsed with EventID ', record['event_id'])
        return None

    if parse_record is not None:
        try:
            record = parse_record(raw, record)
        except:
            record['description'] = 'Unable to parse record xml'
    else:
        record = None

    return record


def get_string(string):
    """
    Takes in either a str or an object that has the str inside of an index ["#text"]. This helps parsing of almost
    all different records.
    :param string:
    :return:
    """
    if isinstance(string, str):
        return string
    return string["#text"]


def get_event_data_section(raw):
    """
    Helper to get the 'EventData' or 'UserData' key of the base XML for each record. If this fails, it is very likely that the
    record is corrupted due to the log recovery software.
    :param raw:
    :return: whether or not the key exists.
    """

    if 'EventData' not in raw['Event'] and 'UserData' not in raw['Event']:
        return False

    return True
