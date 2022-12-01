from datetime import datetime
import time

print('# datetime')
print('datetime.now():', datetime.now())
# 2022-12-01 16:03:24.346999
t = datetime.now()
print('datetime.now:', t.year, t.month, t.day, t.hour, t.minute, t.second)
# 2022 12 1 16 3 24

print('# time')
print('time.time():', time.time())
# 1669878336.8988504
print('time.ctime():', time.ctime())
# Thu Dec  1 16:05:36 2022
print('time.localtime():', time.localtime())
# time.struct_time(tm_year=2022, tm_mon=12, tm_mday=1, tm_hour=16, tm_min=5, tm_sec=36, tm_wday=3, tm_yday=335, tm_isdst=0)    
t = time.localtime()
print('time.localtime:', t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
# 2022 12 1 16 5 36
