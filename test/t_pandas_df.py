import pandas as pd

# dict로 dataframe 만들기
data1 = {
    'phone' : ['1111', '2222', '3333'],
    'name' : ['lee', 'kim', 'park'],
    'color' : ['yellow', 'green', 'red'],
    }
df1 = pd.DataFrame(data1)
# print(df1)
"""
  phone  name   color
0  1111   lee  yellow
1  2222   kim   green
2  3333  park     red
"""

# list로 dataframe 만들기
data2 = [
    ['1111', 'lee', 'yellow'],
    ['2222', 'kim', 'green'],
    ['3333', 'park', 'red'],
    ]
columns=['phone', 'name', 'color']
df2 = pd.DataFrame(data2, columns=columns)
# print(df2)
"""
  phone  name   color
0  1111   lee  yellow
1  2222   kim   green
2  3333  park     red
"""
