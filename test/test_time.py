from datetime import datetime, timedelta
import time

print(f"-> time.time: {time.time()}")
print(f"-> time.ctime: {time.ctime()}")
print(f"-> time.localtime: {time.localtime()}")
print(f"-> time strftime: {time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}")

print()

print(f"-> datetime.now: {datetime.now()}")
print(f"-> datetime.now.time: {datetime.now().time()}")
print(f"-> datetime.now.date: {datetime.now().date()}")
print(f"-> datetime strftime: {datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")

t = datetime.now()
print(f"-> datetime format: {t.year, t.month, t.day, t.hour, t.minute, t.second}")

start = datetime.now().timestamp()
time.sleep(1)
print(f"-> timedelta: {timedelta(seconds=datetime.now().timestamp() - start)}")