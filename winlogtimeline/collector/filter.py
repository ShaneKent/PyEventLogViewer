

def filter_logs(project, config):
    """
    When given a list of log objects, returns only those that match the filters defined in config and project. The
    filters in project take priority over config.
    :param project: A project instance.
    :param config: A config dictionary.
    :return: A list of logs that satisfy the filters specified in the configuration.
    """
    #config = [('event_id', '=', 5061)]

    query = 'SELECT * FROM logs WHERE '
    for constraint in config:
        query += '{} {} {} AND '.format(*constraint)
    query = query[:-5]
    print(query)

    cur = project._conn.execute(query)

    logs = cur.fetchall()
    print('Found {} matches'.format(len(logs)))

    return logs


