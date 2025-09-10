from datetime import datetime, timedelta
import time

now = datetime.now()

print(f"now : {now}")

print(f"date : {now.date()}")

print(f"time : {now.time()}")

print(f"strftime : {now.strftime('%Y-%m-%d %H:%M:%S %A')}")

timestamp = now.timestamp()
print(f"timestamp: {timestamp}")

yesterday = now - timedelta(days=-1)
print(f"timedelta: {yesterday}")


