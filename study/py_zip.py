numbers = [1, 2, 3]
letters = ["A", "B", "C"]

# zip
print('='*40)

data1 = zip(numbers, letters)
print(type(data1))
print(data1)
[print(d) for d in data1]
"""
<class 'zip'>
<zip object at 0x0000024F322DFA80>
(1, 'A')
(2, 'B')
(3, 'C')
"""

# list
print('='*40)

data2 = list(zip(numbers, letters))
print(type(data2))
print(data2)
print(type(data2[0]))
'''
[(1, 'A'), (2, 'B'), (3, 'C')]
<class 'tuple'>
'''

# dict
print('='*40)

data3 = dict(zip(numbers, letters))
print(type(data3))
print(data3)
'''
<class 'dict'>
{1: 'A', 2: 'B', 3: 'C'}
'''

# unzip
print('='*40)

numbers, letters = zip(*data2)
print(numbers)
print(letters)
'''
(1, 2, 3)
('A', 'B', 'C')
'''

# 사용 병렬처리 (하나씩 가져와서 처리)
print('='*40)

for number, upper, lower in zip("12345", "ABCDE", "abcde"):
    print(number, upper, lower)
'''
1 A a
2 B b
3 C c
4 D d
5 E e
'''
