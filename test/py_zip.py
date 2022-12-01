numbers = [1, 2, 3]
letters = ["A", "B", "C"]

data1 = zip(numbers, letters)
print(type(data1))
# <class 'zip'>
print(data1)
# <zip object at 0x0000023D15FB8880>
[print(d) for d in data1]
"""
(1, 'A')
(2, 'B')
(3, 'C')
"""

data2 = list(zip(numbers, letters))
print(data2)
# [(1, 'A'), (2, 'B'), (3, 'C')]

data3 = dict(zip(numbers, letters))
print(data3)
# {1: 'A', 2: 'B', 3: 'C'}


# unzip
numbers, letters = zip(*data2)
print(numbers, letters)
# (1, 2, 3) ('A', 'B', 'C')


# 사용 병렬처리 (하나씩 가져와서 처리)
for number, upper, lower in zip("12345", "ABCDE", "abcde"):
    print(number, upper, lower)
'''
1 A a
2 B b
3 C c
4 D d
5 E e
'''
