import random

a = ['1', '2', '3', '4', '5']

# 1-9 중에 3칸씩 띄워서
randrange = random.randrange(1, 10, 3)
# print(randrange)
# randrange : 7

# choice는 하나만 추출
choice = random.choices(a)
# print(choice)
# choice : ['4']

# choices는 중복 추출 가능
choices = random.choices(a, k=3)
# print(choices)
# choice : ['4', '1', '1']

# sample은 중복 추출 안됨
sample = random.sample(a, 3)
# print(sample)
# sample : ['4', '1', '3']
