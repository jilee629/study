import pandas as pd
from datetime import date

# dict
data = {
   'name' : ['A', 'B', 'C'],
   'id' : ['a', 'b', 'c'],
   'age' : ['11', '12', '13']
}
index = ['1', '2', '3']
df = pd.DataFrame(data, index=index)
df.to_excel('pandas1.xlsx', engine='openpyxl')

# list나 tuple
data2 = [
   ('A', 'a', '11'),
   ('B', 'b', '12'),
   ('C', 'c', '13')
]
columns = ['name', 'id', 'age']
index = ['1', '2', '3']
df = pd.DataFrame(data2, columns=columns, index=index, )
df.to_excel('pandas2.xlsx', engine='openpyxl')