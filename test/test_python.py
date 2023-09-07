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

def list_test_1():
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

def list_test_2():
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

def request_test_1():
    import requests
    res = requests.get("https://jsonplaceholder.typicode.com/users/1")
    print(res)
    print(res.content)
    print(res.headers)
    print('\nContent-Type: ', res.headers['Content-Type'])

if __name__ == "__main__":
    
    request_test_1()