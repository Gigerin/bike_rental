from datetime import datetime, timezone

import pytz
from dateutil.parser import parser
import math


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
    "Проверка в прошлом время или нет"
    current_datetime = datetime.now(timezone.utc)

    if input_datetime.tzinfo is None:
        input_datetime = input_datetime.replace(tzinfo=timezone.utc)

    return input_datetime < current_datetime


def calculate_total_price(bike):
    "Считает финальную сумму по часам округляя вверх"
    start_datetime = bike.rented_from
    current_datetime = datetime.now(timezone.utc)
    time_difference = current_datetime - start_datetime
    hours_difference = time_difference.total_seconds() / 3600
    hours_passed = math.ceil(hours_difference)
    price_per_hour = bike.price
    total_price = price_per_hour * hours_passed
    return total_price
