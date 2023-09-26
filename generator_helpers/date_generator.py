from dateutil.tz import gettz, tzlocal, tzutc
from calendar import timegm
from datetime import datetime, date, timedelta
import random


class ParseError(ValueError):
    pass


def datetime_to_timestamp(dt):
    if getattr(dt, "tzinfo", None) is not None:
        dt = dt.astimezone(tzutc())
    return timegm(dt.timetuple())


def _parse_date_time(value, tzinfo=None):
    if isinstance(value, (datetime, date)):
        return datetime_to_timestamp(value)
    now = datetime.now(tzinfo)
    if isinstance(value, timedelta):
        return datetime_to_timestamp(now + value)
    if isinstance(value, str):
        if value == "now":
            return datetime_to_timestamp(datetime.now(tzinfo))
        time_params = _parse_date_string(value)
        return datetime_to_timestamp(now + timedelta(**time_params))
    if isinstance(value, int):
        return datetime_to_timestamp(now + timedelta(value))
    raise ParseError(f"Invalid format for date {value!r}")


import re

timedelta_pattern = r""
for name, sym in [
    ("years", "y"),
    ("months", "M"),
    ("weeks", "w"),
    ("days", "d"),
    ("hours", "h"),
    ("minutes", "m"),
    ("seconds", "s"),
]:
    timedelta_pattern += r"((?P<{}>(?:\+|-)\d+?){})?".format(name, sym)
regex = re.compile(timedelta_pattern)


def _parse_date_string(value):
    parts = regex.match(value)
    if not parts:
        raise ParseError(f"Can't parse date string `{value}`")
    parts = parts.groupdict()
    time_params = {}
    for (name_, param_) in parts.items():
        if param_:
            time_params[name_] = int(param_)

    if "years" in time_params:
        if "days" not in time_params:
            time_params["days"] = 0
        time_params["days"] += 365.24 * time_params.pop("years")
    if "months" in time_params:
        if "days" not in time_params:
            time_params["days"] = 0
        time_params["days"] += 30.42 * time_params.pop("months")

    if not time_params:
        raise ParseError(f"Can't parse date string `{value}`")
    return time_params


def date_time_between(start_date="-30y", end_date="now", tzinfo=None):
    """
    Get a DateTime object based on a random date between two given dates.
    Accepts date strings that can be recognized by strtotime().

    :param start_date Defaults to 30 years ago
    :param end_date Defaults to "now"
    :param tzinfo: timezone, instance of datetime.tzinfo subclass
    :example DateTime('1999-02-02 11:42:52')
    :return DateTime
    """
    start_date = _parse_date_time(start_date, tzinfo=tzinfo)
    end_date = _parse_date_time(end_date, tzinfo=tzinfo)
    if end_date - start_date <= 1:
        ts = start_date + random.random()
    else:
        ts = random.randint(start_date, end_date)
    if tzinfo is None:
        return datetime(1970, 1, 1, tzinfo=tzinfo) + timedelta(seconds=ts)
    else:
        return (
            datetime(1970, 1, 1, tzinfo=tzutc()) + timedelta(seconds=ts)
        ).astimezone(tzinfo)


def date_between_dates(date_start=None, date_end=None):
    """
    Takes two Date objects and returns a random date between the two given dates.
    Accepts Date or Datetime objects

    :param date_start: Date
    :param date_end: Date
    :return Date
    """
    return date_time_between_dates(date_start, date_end).date()


def date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None):
    """
    Takes two DateTime objects and returns a random datetime between the two
    given datetimes.
    Accepts DateTime objects.

    :param datetime_start: DateTime
    :param datetime_end: DateTime
    :param tzinfo: timezone, instance of datetime.tzinfo subclass
    :example DateTime('1999-02-02 11:42:52')
    :return DateTime
    """
    if datetime_start is None:
        datetime_start = datetime.now(tzinfo)

    if datetime_end is None:
        datetime_end = datetime.now(tzinfo)

    timestamp = random.randint(
        datetime_to_timestamp(datetime_start), datetime_to_timestamp(datetime_end)
    )
    try:
        if tzinfo is None:
            pick = datetime.fromtimestamp(timestamp, tzlocal())
            pick = pick.astimezone(tzutc()).replace(tzinfo=None)
        else:
            pick = datetime.fromtimestamp(timestamp, tzinfo)
    except OverflowError:
        raise OverflowError(
            "You specified an end date with a timestamp bigger than the maximum allowed on this"
            " system. Please specify an earlier date."
        )
    return pick
