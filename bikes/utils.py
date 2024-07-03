from datetime import datetime, timezone

import pytz
from dateutil.parser import parser


def cast_to_aware(dt_string):
    try:
        aware_dt = parser.isoparse(dt_string)
        if aware_dt.tzinfo is not None:
            return dt_string

        naive_dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        aware_dt = pytz.utc.localize(naive_dt)

        aware_dt_string = aware_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")

        return aware_dt_string
    except ValueError:
        return dt_string
    except Exception as e:
        return f"Error: {e}"

def is_in_past(input_datetime):
    current_datetime = datetime.now(timezone.utc)

    if input_datetime.tzinfo is None:
        input_datetime = input_datetime.replace(tzinfo=timezone.utc)

    return input_datetime < current_datetime