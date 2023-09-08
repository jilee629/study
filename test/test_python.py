def sep(num):
    print(f"test({str(num)}) {'-' * 40}")

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
    
    sep(1)
    print(datetime.now())
    # 2023-09-07 17:43:45.092355
    
    sep(2)
    t = datetime.now()
    print(t.year, t.month, t.day, t.hour, t.minute, t.second)
    # 2023 9 7 17 43 45

def test_time():
    import time

    sep(1)
    print(time.time())
    # 1694076225.113485
    
    sep(2)
    print(time.ctime())
    # Thu Sep  7 17:43:45 2023

def test_pandas_df():
    import pandas as pd

    sep(1)
    # dict data 일경우, key는 columns에 value는 index에 들어감
    data = {'name' : ['A', 'B', 'C'], 'id' : ['a', 'b', 'c'], 'age' : ['11', '12', '13']}
    df = pd.DataFrame(data)
    print(df)
    # name id age
    # 0    A  a  11
    # 1    B  b  12
    # 2    C  c  13

    sep(2)
    data = [['A', 'a', '11'], ['B', 'b', '12'], ['C', 'c', '13']]
    columns = ['name', 'id', 'age']
    index = ['1', '2', '3']
    df = pd.DataFrame(data, columns=columns, index=index)
    print(df)
    # name id age
    # 1    A  a  11
    # 2    B  b  12
    # 3    C  c  13

    sep(3)
    data2 = [('A', 'a', '11'), ('B', 'b', '12'), ('C', 'c', '13')]
    columns = ['name', 'id', 'age']
    index = ['1', '2', '3']
    df = pd.DataFrame(data, columns=columns, index=index)
    print(df)
    # name id age
    # 1    A  a  11
    # 2    B  b  12
    # 3    C  c  13

def test_pandas_save():
    import pandas as pd

    sep(1)
    data = {'name' : ['A', 'B', 'C'], 'id' : ['a', 'b', 'c'], 'age' : ['11', '12', '13']}
    index = ['1', '2', '3']
    df = pd.DataFrame(data, index=index)
    df.to_excel('test_pandas1.xlsx', engine='openpyxl')
    # index 지정하지 않으면 0부터

    sep(2)
    data = [['A', 'a', '11'], ['B', 'b', '12'], ['C', 'c', '13']]
    columns = ['name', 'id', 'age']
    df = pd.DataFrame(data, columns=columns)
    df.index += 2
    df.to_excel('test_pandas2.xlsx', engine='openpyxl')



if __name__ == "__main__":
    import sys
    test = getattr(sys.modules[__name__], sys.argv[1])
    test()