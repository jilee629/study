import random

a = ['1', '2', '3', '4', '5']

# 1-9 중에 3칸씩 띄워서
randrange = random.randrange(1, 10, 3)
print(f"randrange : {randrange}")

# choice는 하나만 추출
choice = random.choices(a)
print(f"choice : {choice}")

# choices는 중복 추출 가능
choices = random.choices(a, k=3)
print(f"choice : {choices}")

# sample은 중복 추출 안됨
sample = random.sample(a, 3)
print(f"sample : {sample}")