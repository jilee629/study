import pandas as pd

data = {'name' : ['A', 'B', 'C'], 'id' : ['a', 'b', 'c'], 'age' : ['11', '12', '13']}
index = ['1', '2', '3']
df = pd.DataFrame(data, index=index)
df.to_excel('test_pandas1.xlsx', engine='openpyxl')
# index 지정하지 않으면 0부터

data = [['A', 'a', '11'], ['B', 'b', '12'], ['C', 'c', '13']]
columns = ['name', 'id', 'age']
df = pd.DataFrame(data, columns=columns)
df.index += 2
df.to_excel('test_pandas2.xlsx', engine='openpyxl')