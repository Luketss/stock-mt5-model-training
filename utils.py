import time
import csv
from datetime import datetime
import pytz


def transform_data(date, timezone="Brazil/East"):
    """create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset"""
    timezone = pytz.timezone(timezone)
    utc_to_dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone)
    return utc_to_dt


def check_timezones():
    print(pytz.all_timezones)

    br_timezones = [timezone for timezone in pytz.all_timezones if "Brazil" in timezone]
    print(br_timezones)


def transform_time_to_timestamp(full_date):
    """
    full_date sample: "2024-04-01 14:08:00"
    """
    element = datetime.strptime(full_date, "%Y-%m-%d %H:%M:%S")

    tuple = element.timetuple()
    timestamp = time.mktime(tuple)

    return timestamp


def read_time_from_csv(file_path: str):
    rows = []
    fields = []
    with open(f"{file_path}.csv", "r") as f:
        lines = csv.reader(f, delimiter=",")

        for index, line in enumerate(lines):
            if index == 0:
                fields.extend(line)
            if index > 0 and len(line) > 0:
                columns = line
                temp = [
                    columns[0].strip(),
                    transform_time_to_timestamp(columns[1].strip()),
                    *map(str.strip, columns[2:9]),
                ]
                rows.append(temp)
    with open(f"{file_path}_timestamp.csv", "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)


if __name__ == "__main__":
    read_time_from_csv("WEGE3")
    # transform_time_to_timestamp()
