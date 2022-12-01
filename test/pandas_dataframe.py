import pandas as pd

# # dict로 선언한 경우, key를 기준으로 columns(세로) 입력
# data1 = {
#    'name' : ['A', 'B', 'C'],
#    'id' : ['a', 'b', 'c'],
#    'age' : ['11', '12', '13']
# }
# df = pd.DataFrame(data1)
# print(df, '\n')
# '''
#   name id age
# 1    A  a  11
# 2    B  b  12
# 3    C  c  13
# '''

# list나 tupled로 선언할경우, row값에 들어간다.
data2 = [
   ['A', 'a', '11'],
   ['B', 'b', '12'],
   ['C', 'c', '13']
]
columns = ['name', 'id', 'age']
index = ['1', '2', '3']
df = pd.DataFrame(data2, columns=columns, index=index)
print(df, '\n')
'''
  name id age
1    A  a  11
2    B  b  12
3    C  c  13
'''

# data3 = [
#    ('A', 'a', '11'),
#    ('B', 'b', '12'),
#    ('C', 'c', '13')
# ]
# columns = ['name', 'id', 'age']
# df = pd.DataFrame(data3, columns=columns)
# print(df, '\n')
# '''
#   name id age
# 0    A  a  11
# 1    B  b  12
# 2    C  c  13
# '''