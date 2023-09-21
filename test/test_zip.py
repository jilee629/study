numbers = [1, 2, 3]
letters = ["A", "B", "C"]

print(zip(numbers, letters))
print()
# <zip object at 0x00000234FFEA0480>

[print(d) for d in zip(numbers, letters)]
'''
(1, 'A')
(2, 'B')
(3, 'C')
'''


print(list(zip(numbers, letters)))
print()
'''
[(1, 'A'), (2, 'B'), (3, 'C')]
'''

print(dict(zip(numbers, letters)))
print()
'''
{1: 'A', 2: 'B', 3: 'C'}
'''

num, let = zip(*(zip(numbers, letters)))
print(num, let)
print()
'''
(1, 2, 3) ('A', 'B', 'C')
'''

for number, upper, lower in zip("12345", "ABCDE", "abcde"):
    print(number, upper, lower)
print()
'''
1 A a
2 B b
3 C c
4 D d
5 E e
'''

A = (1,2,3)
B = (4,5,6)
sum = tuple(sum(i) for i in zip(A, B))
print(sum)
print(sum[1])
'''
(5, 7, 9)
7
'''