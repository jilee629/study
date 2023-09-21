import pandas as pd

# dict data 일경우, key는 columns에 value는 index에 들어감
data = {'name' : ['A', 'B', 'C'], 'id' : ['a', 'b', 'c'], 'age' : ['11', '12', '13']}
df = pd.DataFrame(data)
print(df)
# name id age
# 0    A  a  11
# 1    B  b  12
# 2    C  c  13

data = [['A', 'a', '11'], ['B', 'b', '12'], ['C', 'c', '13']]
columns = ['name', 'id', 'age']
index = ['1', '2', '3']
df = pd.DataFrame(data, columns=columns, index=index)
print(df)
'''
name id age
1    A  a  11
2    B  b  12
3    C  c  13
'''


data2 = [('A', 'a', '11'), ('B', 'b', '12'), ('C', 'c', '13')]
columns = ['name', 'id', 'age']
index = ['1', '2', '3']
df = pd.DataFrame(data, columns=columns, index=index)
print(df)
'''
name id age
1    A  a  11
2    B  b  12
3    C  c  13
'''