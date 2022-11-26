import pandas as pd

data1 = {
   'name' : ['A', 'B', 'C'],
   'id' : ['a', 'b', 'c'],
   'age' : ['11', '12', '13']
}
df = pd.DataFrame(data1)
print(df, '\n')

data2 = [
   ['A', 'a', '11'],
   ['B', 'b', '12'],
   ['C', 'c', '13']
]
columns = ['name', 'id', 'age']
index = ['1', '2', '3']
df = pd.DataFrame(data2, columns=columns, index=index)
print(df, '\n')

data2 = [
   ('A', 'a', '11'),
   ('B', 'b', '12'),
   ('C', 'c', '13')
]
columns = ['name', 'id', 'age']
df = pd.DataFrame(data2, columns=columns)
print(df, '\n')
