import pandas as pd

data1 = {
    'phone' : ['1111', '2222', '3333'],
    'name' : ['lee', 'kim', 'park'],
    'color' : ['yellow', 'green', 'red'],
    }
df1 = pd.DataFrame(data1)
print(df1)

data2 = [
    ['1111', 'lee', 'yellow'],
    ['2222', 'kim', 'green'],
    ['3333', 'park', 'red'],
    ]
columns=['phone', 'name', 'color']
df2 = pd.DataFrame(data2, columns=columns)
print(df2)