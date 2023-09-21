from tqdm import tqdm
import time

n = 0
for i in tqdm(range(50, 120, 50)):
    time.sleep(.1)
    n += 1
print(n, 'times click')
'''
전체개수가 증가값을 / 값으로 표시됨
'''


i = 0
n = 155
value =10
pbar = tqdm(total= n)
while i < n:
    time.sleep(.1)
    i += value
    pbar.update(value)




