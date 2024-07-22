from datetime import datetime, timedelta
import time

print(f"-> time.time: {time.time()}")
print(f"-> time.ctime: {time.ctime()}")
print(f"-> time.localtime: {time.localtime()}")
print(f"-> time strftime: {time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}")

print()

