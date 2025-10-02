from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

now = datetime.now()
# print(now)
# 2025-10-02 09:32:13.896043

date = now.date()
# print(date)
# 2025-10-02

time = now.time()
# print(time)
# 2025-10-02

timestamp = now.timestamp()
# print(timestamp)
# 1759365211.12254

strftime = now.strftime('%Y-%m-%d %H:%M:%S %A')
# print(strftime)
# 2025-10-02 09:33:54 Thursday

timedelta = now - timedelta(days=2)
# print(now, timedelta)
# 2025-10-02 09:35:11.158943 2025-09-30 09:35:11.158943

relative_2yr_ago = now - relativedelta(years=2)
# print(now, relative_2yr_ago)
# 2025-10-02 09:36:05.067939 2023-10-02 09:36:05.067939

relative_2day_ago = now - relativedelta(days=2)
# print(now, relative_2day_ago)
# 2025-10-02 09:36:05.067939 2023-10-02 09:36:05.067939

# 비표준 날짜 형식을 datetime 객체로
time_string = "2025-09-12 15:53:22.269899"
time_format = "%Y-%m-%d %H:%M:%S.%f"
strptime = datetime.strptime(time_string, time_format)
# print(strptime)
# 2025-09-12 15:53:22.269899

# ISO 8601 형식의 표준화된 문자열을 datetime 객체로
iso_string = "2023-10-27T07:14:20.000Z"
fromisoformat = datetime.fromisoformat(iso_string)
# print(fromisoformat)
# 2023-10-27 07:14:20+00:00

# timezone aware를 native로 변환
native_time = fromisoformat.replace(tzinfo=None)
# print(native_time)
# # native_time : 2023-10-27 07:14:20

diff_time = (now - native_time)
# print(diff_time.days)
# 706
# diff_time_days = (now - native_time).days
# print(diff_time_days)
# 706
