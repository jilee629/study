from datetime import datetime, timedelta
import time

print(f"-> time.time: {time.time()}")
# 1694076225.113485
print(f"-> time.ctime: {time.ctime()}")
# Thu Sep  7 17:43:45 2023
print(f"-> time.localtime: {time.localtime()}")
#time.struct_time(tm_year=2024, tm_mon=2, tm_mday=5, tm_hour=14, tm_min=25, tm_sec=37, tm_wday=0, tm_yday=36, tm_isdst=0)
print(f"-> time strftime: {time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}")
# 2024-02-05

print()

print(f"-> datetime.now: {datetime.now()}")
# 2023-09-07 17:43:45.092355
print(f"-> datetime.now.time: {datetime.now().time()}")
t = datetime.now()
print(f"-> datetime format: {t.year, t.month, t.day, t.hour, t.minute, t.second}")
# 2023 9 7 17 43 45
print(f"-> datetime strftime: {datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")

start = time.time()
time.sleep(1)
delta = time.time() - start
print(f"-> timedelta: {timedelta(seconds=delta)}")