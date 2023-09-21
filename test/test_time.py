from datetime import datetime
from datetime import timedelta
import time

print(datetime.now())
'''
2023-09-07 17:43:45.092355

'''

t = datetime.now()
print(t.year, t.month, t.day, t.hour, t.minute, t.second)
'''
2023 9 7 17 43 45
'''

print(time.time())
'''
1694076225.113485
'''

print(time.ctime())
'''
Thu Sep  7 17:43:45 2023
'''

start = time.time()
time.sleep(1)
end = time.time()
sec = end - start
print(timedelta(seconds=sec))