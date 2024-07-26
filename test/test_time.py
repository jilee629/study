import time

print(f"time: {time.time()}")
print(f"ctime: {time.ctime()}")
print(f"localtime: {time.localtime()}")
print(f"strftime: {time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}")

# time: 1722001162.7722661
# ctime: Fri Jul 26 22:39:22 2024
# localtime: time.struct_time(tm_year=2024, tm_mon=7, tm_mday=26, tm_hour=22, tm_min=39, tm_sec=22, tm_wday=4, tm_yday=208, tm_isdst=0)
# strftime: 2024-07-26-22-39-22