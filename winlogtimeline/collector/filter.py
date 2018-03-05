from winlogtimeline.util.logs import Record

def filter_logs(project, config, dedup):
    """
    When given a list of log objects, returns only those that match the filters defined in config and project. The
    filters in project take priority over config.
    :param project: A project instance.
    :param config: A config dictionary.
    :param dedup: Int var specifying deduplication
    :return: A list of logs that satisfy the filters specified in the configuration.
    """

    headers = Record.get_headers()

    info = project._conn.execute('PRAGMA table_info(logs);') #(id, column name, type, not null, pk, auto-inc)
    id, columns, types, n, p, a = zip(*info)

    filters = []

    #col, operator, value, flag = config[0]
    for col, operator, value, flag in config:
        if not flag:
            continue

        if operator == 'Contains':
            operator = 'like'
            value = "'%" + value + "%'"
        elif operator == 'In':
            value = "(" + value + ")" #Add parentheses for sql list

        idx = headers.index(col)
        col = columns[idx]
        datatype = types[idx] #Data type for this column
        if datatype == 'DATETIME':
            value = "'" + value + "'"
            if len(value.split()) == 1:
                col = 'date(' + col + ')'
        elif datatype == 'INTEGER':
            try: int(value) #Non-integer values for int type columns are invalid
            except: continue
        filters.append((col, operator, value))

    # Timestamp offset
    offset = project.config['state']['timezone_offset']
    if not isinstance(offset, int) or not (-12 <= offset <= 12):
        project.config['state']['timestamp_offset'] = offset = 0

    query = (f'SELECT strftime(\'%Y-%m-%d %H:%M:%f\', timestamp_utc, \'{offset:+d} hours\'), event_id, description,'
             f' details, event_source, event_log, session_id, account, computer_name, record_number, recovered, '
             f'alias, record_hash FROM logs WHERE ')
    for constraint in filters:
        query += '{} {} {} AND '.format(*constraint)
    query = query[:-5]
    if dedup.get() != 0: query += ' GROUP BY record_hash'
    print(query)

    cur = project._conn.execute(query)
    logs = cur.fetchall()
    print('Found {} records'.format(len(logs)))

    logs = [Record(**dict(zip(columns, row))) for row in logs]

    return logs


