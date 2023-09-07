def zip_test_1():
    numbers = [1, 2, 3]
    letters = ["A", "B", "C"]
    data = zip(numbers, letters)
    print(type(data))
    [print(d) for d in data]
"""
<class 'zip'>
(1, 'A')
(2, 'B')
(3, 'C')
"""

def zip_test_2():
    numbers = [1, 2, 3]
    letters = ["A", "B", "C"]
    data = list(zip(numbers, letters))
    print(data)
"""
[(1, 'A'), (2, 'B'), (3, 'C')]
"""

def zip_test_3():
    numbers = [1, 2, 3]
    letters = ["A", "B", "C"]
    data = dict(zip(numbers, letters))
    print(data)
"""
{1: 'A', 2: 'B', 3: 'C'}
"""

# unzip
def zip_test_4():
    numbers = [1, 2, 3]
    letters = ["A", "B", "C"]
    data = list(zip(numbers, letters))
    print(data)
    numbers, letters = zip(*data)
    print(numbers, letters)
"""
[(1, 'A'), (2, 'B'), (3, 'C')]
(1, 2, 3) ('A', 'B', 'C')
"""

# 병렬처리
def zip_test_5():
    for number, upper, lower in zip("12345", "ABCDE", "abcde"):
        print(number, upper, lower)
"""
1 A a
2 B b
3 C c
4 D d
5 E e
"""

if __name__ == "__main__":
    
    zip_test_1()