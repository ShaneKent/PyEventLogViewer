import csv


class Export:
    """
    Current a very basic .csv exporter
    """

    def __init__(self, current_project):
        records = current_project.get_all_logs()

        with open(current_project.get_path() + '/timeline.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for record in records:
                spamwriter.writerow([record.timestamp_utc, record.event_id, record.description, record.details])
