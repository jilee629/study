from datetime import datetime, timedelta
import time

now = datetime.now()

print(f"now : {now}")
# now : 2025-09-12 15:53:22.269899

print(f"date : {now.date()}")
# date : 2025-09-12

print(f"time : {now.time()}")
# time : 15:53:22.269899

print(f"strftime : {now.strftime('%Y-%m-%d %H:%M:%S %A')}")
# strftime : 2025-09-12 15:53:22 Friday

timestamp = now.timestamp()
print(f"timestamp: {timestamp}")
# timestamp: 1757660002.269899

yesterday = now - timedelta(days=1)
print(f"timedelta: {yesterday}")
# timedelta: 2025-09-11 15:53:22.269899

