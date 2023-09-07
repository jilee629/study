def sep(num):
    print(str(num), '-' * 80)

def test_zip():
    numbers = [1, 2, 3]
    letters = ["A", "B", "C"]
    data = zip(numbers, letters)
    
    sep(1)
    print(type(data))
    # <class 'zip'>
    
    sep(2)
    print(data)
    # <zip object at 0x00000234FFEA0480>

    sep(3)
    [print(d) for d in data]
    # (1, 'A')
    # (2, 'B')
    # (3, 'C')
    
    sep(4)
    data = list(zip(numbers, letters))
    print(data)
    # [(1, 'A'), (2, 'B'), (3, 'C')

    sep(5)
    data = dict(zip(numbers, letters))
    print(data)
    # {1: 'A', 2: 'B', 3: 'C'}

    sep(6)
    data = list(zip(numbers, letters))
    num, let = zip(*data)
    print(num, let)
    # (1, 2, 3) ('A', 'B', 'C')

    sep(7)
    for number, upper, lower in zip("12345", "ABCDE", "abcde"):
        print(number, upper, lower)
    # 1 A a
    # 2 B b
    # 3 C c
    # 4 D d
    # 5 E e

def test_list():
    sep(1)
    list1 = ['a', 'b', 'c']
    list2 = ['e', 'f', 'g']
    list1.append(list2)
    print(list1)
    # ['a', 'b', 'c', ['e', 'f', 'g']]    

    sep(2)
    list1 = ['a', 'b', 'c']
    list2 = ['e', 'f', 'g']
    list1.extend(list2)
    print(list1)
    # ['a', 'b', 'c', ['e', 'f', 'g']]

def test_enum():
    sep(1)
    for i, letter in enumerate(['A', 'B', 'C']):
        print(i, letter)   
    # 0 A
    # 1 B
    # 2 C

    sep(2)
    for entry in enumerate(['A', 'B', 'C']):
        print(entry)
    # (0, 'A')
    # (1, 'B')
    # (2, 'C')

def test_datetime():
    from datetime import datetime
    import time

    sep(1)
    print(datetime.now())
    # 2023-09-07 17:43:45.092355
    
    sep(2)
    t = datetime.now()
    print(t.year, t.month, t.day, t.hour, t.minute, t.second)
    # 2023 9 7 17 43 45

    sep(3)
    print(time.time())
    # 1694076225.113485
    
    sep(4)
    print(time.ctime())
    # Thu Sep  7 17:43:45 2023

def test_request_1():
    import requests
    res = requests.get("https://jsonplaceholder.typicode.com/users/1")

    sep(1)
    print(res)

    sep(2)
    print(res.content)

    sep(3)
    print(res.headers)

    sep(4)
    print(res.headers['Content-Type'])



if __name__ == "__main__":
    import sys
    test = getattr(sys.modules[__name__], sys.argv[1])
    test()