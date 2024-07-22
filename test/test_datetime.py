from datetime import datetime, timedelta
import time

now = datetime.now()

print(now)
# 2024-07-22 13:31:47.496295

print(now.strftime("%Y-%m-%d %H:%M:%S %A"))
# 2024-07-22 13:31:47 Monday

print(now.time())
# 13:31:47.496295

print(now.date())
# 2024-07-22

print(now.strftime('%Y-%m-%d %H:%M:%S'))
# 2024-07-22 13:31:47

print(timedelta(datetime.now().timestamp() - now.timestamp()))
# 0:00:09.249115