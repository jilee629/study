import time

print(time.time())
# 1732713087.7830682

print(time.ctime())
# Wed Nov 27 22:11:27 2024

print(time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime()))
# 2024-11-27 22:16:44 Wednesday

print(time.localtime())
# time.struct_time(tm_year=2024, tm_mon=11, tm_mday=27, tm_hour=22, tm_min=11, tm_sec=27, tm_wday=2, tm_yday=332, tm_isdst=0)


