from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

now = datetime.now()
# print("now :", now)
# now : 2025-09-26 15:56:16.858232

date = now.date()
# print("date :", date)
# date : 2025-09-26

time = now.time()
# print("time :", time)
# time : 15:56:16.858232

timestamp = now.timestamp()
# print("timestamp :", timestamp)
# timestamp : 1758869776.858232

strftime = now.strftime('%Y-%m-%d %H:%M:%S %A')
# print("strftime :", strftime)
# strftime : 2025-09-26 15:56:16 Friday

timedelta = now - timedelta(days=2)
# print("timedelta :", timedelta)
#timedelta : 2025-09-24 15:56:16.858232

# timedelta와 다르게 음력까지 계산해서 정확하게 계산
# relativedelta = now - relativedelta(years=2)
print("relativedelta :", relativedelta)
# relativedelta : 2023-09-26 15:56:16.858232

# 비표준 날짜 형식을 datetime 객체로
time_string = "2025-09-12 15:53:22.269899"
time_format = "%Y-%m-%d %H:%M:%S.%f"
strptime = datetime.strptime(time_string, time_format)
# print("strptime :", strptime)
# strptime : 2025-09-12 15:53:22.269899

# ISO 8601 형식의 표준화된 문자열을 datetime 객체로
iso_string = "2023-10-27T07:14:20.000Z"
fromisoformat = datetime.fromisoformat(iso_string)
# print("fromisoformat :", fromisoformat)
# fromisoformat : 2025-04-27 07:14:20+00:00

# timezone aware를 native로 변환
native_time = fromisoformat.replace(tzinfo=None)
# print("native_time :", native_time)
# native_time : 2023-10-27 07:14:20

two_years_ago = now - relativedelta(years=2)
diff_time = native_time - two_years_ago
print(diff_time.days)
