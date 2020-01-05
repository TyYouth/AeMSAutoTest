#!/usr/bin/env python
# coding=utf-8
import datetime

"""
日期格式化符号:
%y 两位数的年份表示（00-99） %Y 四位数的年份表示（000-9999）
%m 月份（01-12） %d 月内中的一天（0-31）
%H 24小时制小时数（0-23）%I 12小时制小时数（01-12）%M 分钟数（00=59）%S 秒（00-59）
%a 本地简化星期名称 %A 本地完整星期名称 %b 本地简化的月份名称 %B 本地完整的月份名称
%c 本地相应的日期表示和时间表示 %j 年内的一天（001-366） %p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始 %w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始 %x 本地相应的日期表示 %X 本地相应的时间表示
%Z 当前时区的名称 %% %号本身
"""


class DateTime(object):
    _current_time = datetime.datetime.now()
    _current_utc_time = datetime.datetime.now(tz=datetime.timezone.utc)

    def get_current_time(self):
        return DateTime.to_str_time_by(self._current_time)

    def get_current_utc_time(self):
        return DateTime.to_str_time_by(self._current_utc_time)

    @staticmethod
    def to_str_time_by(datetime_type, time_format="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strftime(datetime_type, time_format)

    @staticmethod
    def to_datetime_by(str_type, time_format="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strptime(str_type, time_format)

    @staticmethod
    def delta_time(days_delta=0, hours_delta=0, minutes_delta=0):
        return datetime.timedelta(days=days_delta, hours=hours_delta, minutes=minutes_delta)

    @staticmethod
    def expected_time(days_delta=0, hours_delta=0, minutes_delta=0):
        return DateTime._current_time + DateTime.delta_time(days_delta, hours_delta, minutes_delta)


if __name__ == "__main__":
    test = DateTime()
    print(test.expected_time())
    print(test.get_current_time())
