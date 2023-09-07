def test_zip_1():
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

def test_zip_2():
    numbers = [1, 2, 3]
    letters = ["A", "B", "C"]
    data = list(zip(numbers, letters))
    print(data)
"""
[(1, 'A'), (2, 'B'), (3, 'C')]
"""

def ztest_zip_3():
    numbers = [1, 2, 3]
    letters = ["A", "B", "C"]
    data = dict(zip(numbers, letters))
    print(data)
"""
{1: 'A', 2: 'B', 3: 'C'}
"""

# unzip
def test_zip_4():
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
def test_zip_5():
    for number, upper, lower in zip("12345", "ABCDE", "abcde"):
        print(number, upper, lower)
"""
1 A a
2 B b
3 C c
4 D d
5 E e
"""

def test_list_1():
    list1 = ['a', 'b', 'c']
    list2 = ['e', 'f', 'g']
    list1.append(list2)
    print(list1)    
"""
list1 = ['a', 'b', 'c']
list2 = ['e', 'f', 'g']
list1.append(list2)
print('append:', list1)
"""

def test_list_2():
    list1 = ['a', 'b', 'c']
    list2 = ['e', 'f', 'g']
    list1.extend(list2)
    print(list1)
"""
list3 = ['a', 'b', 'c']
list4 = ['e', 'f', 'g']
list3.extend(list4)
print('extend:', list3)
"""

def test_request_1():
    import requests
    res = requests.get("https://jsonplaceholder.typicode.com/users/1")
    print(res)
    print(res.content)
    print(res.headers)
    print('\nContent-Type: ', res.headers['Content-Type'])

def test_enum_1():
    for i, letter in enumerate(['A', 'B', 'C']):
        print(i, letter)   
"""
0 A
1 B
2 C
"""

def test_enum_2():
    for entry in enumerate(['A', 'B', 'C']):
        print(entry)
"""
(0, 'A')
(1, 'B')
(2, 'C')
"""

if __name__ == "__main__":
    
    test_enum_2()