# -*- coding: utf-8 -*-
import datetime as dt
from datetime import datetime, timedelta
from typing import Union

import pytz  # type: ignore
from django.conf import settings


class DateTimeUtil:
    @staticmethod
    def now(tz_name: str = settings.TIME_ZONE) -> datetime:
        tz = pytz.timezone(tz_name)
        return datetime.now(tz=tz)

    @staticmethod
    def get_time_from_now(  # noqa: CFQ002
        days: int = 0,
        seconds: int = 0,
        microseconds: int = 0,
        milliseconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        weeks: int = 0,
    ) -> datetime:
        """
        kwargs: Params in timedelta function. eg: minutes=5, hours=1,
        """
        return DateTimeUtil.now() + timedelta(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )

    @staticmethod
    def to_timezone(dt: datetime, tz_name: str = settings.TIME_ZONE) -> datetime:
        """Convert datetime to timezone datetime

        Args:
            dt (datetime) - The datetime object
            tz_name (str) - The name of timezone

        Returns:
            datetime - The datetime object with new timezone, invalid timezone
                       name make no effect

        """
        try:
            tz = pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            return dt

        return dt.astimezone(tz)

    @staticmethod
    def convert_ts_to_timezone(
        timestamp: int,
        tz_name: str = settings.TIME_ZONE,
        is_millisecond: bool = False,
    ) -> datetime:
        if is_millisecond:
            timestamp = int(timestamp / 1000)
        return DateTimeUtil.to_timezone(
            datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.UTC),
            tz_name=tz_name,
        )

    @staticmethod
    def is_time_range_overlap(
        time_range_1: tuple[Union[datetime, dt.date], Union[datetime, dt.date]],
        time_range_2: tuple[Union[datetime, dt.date], Union[datetime, dt.date]],
        should_check_equal: bool = False,
    ) -> bool:
        max_start = max(time_range_1[0], time_range_2[0])
        min_end = min(time_range_1[1], time_range_2[1])
        if not should_check_equal:
            return max_start < min_end
        return max_start <= min_end
