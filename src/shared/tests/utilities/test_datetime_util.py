# type: ignore
from datetime import datetime, timedelta

import pytest
from shared.utilities.datetime import DateTimeUtil
from main import settings


class TestDateTimeUtil:
    def test_success__get_now(self):
        # action
        now = DateTimeUtil.now()

        # assert
        assert isinstance(now, datetime)
        assert now.tzinfo.tzname(now) == settings.TIME_ZONE

    @pytest.mark.parametrize(
        "days,seconds,microseconds,milliseconds,minutes,hours,weeks",
        [
            (1, 0, 0, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0, 0, 0),
            (0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 1, 0, 0),
            (0, 0, 0, 0, 0, 1, 0),
            (0, 0, 0, 0, 0, 0, 1),
            (1, 1, 1, 1, 1, 1, 1),
        ],
    )
    def test_success__get_time_from_now(
        self, days, seconds, microseconds, milliseconds, minutes, hours, weeks, mocker
    ):
        # arrange
        now = DateTimeUtil.now()

        # mock time now
        mocker.patch("shared.utilities.datetime.DateTimeUtil.now", return_value=now)

        # action
        result = DateTimeUtil.get_time_from_now(
            days, seconds, microseconds, milliseconds, minutes, hours, weeks
        )

        # assert
        assert result == now + timedelta(
            days, seconds, microseconds, milliseconds, minutes, hours, weeks
        )
        assert result.tzinfo.tzname(result) == settings.TIME_ZONE

    def test_success__to_timezone__valid_timezone(self):
        # arrange
        tz = "Asia/Ho_Chi_Minh"
        utc_now = datetime.utcnow()

        # action
        result = DateTimeUtil.to_timezone(utc_now, tz)

        # assert
        assert result.tzinfo.tzname(result) == "+07"

    def test_success__to_timezone__invalid_timezone(self):
        # arrange
        tz = "Asia/INVALID_TIMEZONE"
        utc_now = datetime.utcnow()

        # action
        result = DateTimeUtil.to_timezone(utc_now, tz)

        # assert
        assert result.tzinfo is None

    @pytest.mark.parametrize(
        "tz_name,year,month,day,hour,minute,second",
        [
            ("UTC", 2023, 2, 7, 2, 40, 15),
            ("Asia/Ho_Chi_Minh", 2023, 2, 7, 9, 40, 15),
        ],
    )
    def test_success__convert_ts_to_timezone(self, tz_name, year, month, day, hour, minute, second):
        # arrange
        timestamp = 1675737615

        # action
        result = DateTimeUtil.convert_ts_to_timezone(timestamp, tz_name)

        # assert
        assert result.year == year
        assert result.month == month
        assert result.day == day
        assert result.hour == hour
        assert result.minute == minute
        assert result.second == second

    @pytest.mark.parametrize(
        "range_1, range_2, equal, expected",
        [
            [
                (datetime(2021, 1, 1), datetime(2021, 1, 2)),
                (datetime(2021, 1, 2), datetime(2021, 1, 3)),
                True,
                True
            ],
            [
                (datetime(2021, 1, 1), datetime(2021, 1, 2)),
                (datetime(2021, 1, 2), datetime(2021, 1, 3)),
                False,
                False
            ],
            [
                (datetime(2021, 1, 1), datetime(2021, 1, 2)),
                (datetime(2021, 1, 3), datetime(2021, 1, 4)),
                True,
                False
            ],
            [
                (datetime(2021, 1, 1), datetime(2021, 1, 2)),
                (datetime(2021, 1, 3), datetime(2021, 1, 4)),
                False,
                False
            ],
            [
                (datetime(2021, 1, 1), datetime(2021, 1, 2)),
                (datetime(2020, 1, 3), datetime(2020, 1, 4)),
                True,
                False
            ],
            [
                (datetime(2021, 1, 1), datetime(2021, 1, 2)),
                (datetime(2020, 1, 3), datetime(2020, 1, 4)),
                False,
                False
            ],
            [
                (datetime(2021, 1, 2), datetime(2021, 1, 5)),
                (datetime(2021, 1, 1), datetime(2021, 1, 3)),
                True,
                True
            ],
            [
                (datetime(2021, 1, 2), datetime(2021, 1, 5)),
                (datetime(2021, 1, 1), datetime(2021, 1, 3)),
                False,
                True
            ],
            [
                (datetime(2021, 1, 2), datetime(2021, 1, 5)),
                (datetime(2021, 1, 3), datetime(2021, 1, 6)),
                True,
                True
            ],
            [
                (datetime(2021, 1, 2), datetime(2021, 1, 5)),
                (datetime(2021, 1, 3), datetime(2021, 1, 6)),
                False,
                True
            ],
            [
                (datetime(2021, 1, 2), datetime(2021, 1, 5)),
                (datetime(2021, 1, 1), datetime(2021, 1, 2)),
                True,
                True
            ],
            [
                (datetime(2021, 1, 2), datetime(2021, 1, 5)),
                (datetime(2021, 1, 1), datetime(2021, 1, 2)),
                False,
                False
            ],
        ]
    )
    def test_success__is_time_range_overlap(self, range_1, range_2, equal, expected):
        # action
        result = DateTimeUtil.is_time_range_overlap(range_1, range_2, equal)

        # assert
        assert result == expected
