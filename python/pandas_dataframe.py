import pandas as pd

data = {
   'Year' : ['2001', '2002', '2003'],
   'GDP rate' : ['2.2', '2,3', '3.5'],
   'GDP' : ['1,44M', '2.22M', '2.45M']
}
df = pd.DataFrame(data)
print(df)
print("*"*50)

data = [
   ['2002', '2003', '2004'],
   ['2.2', '2,3', '3.5'],
   ['1,44M', '2.22M', '2.45M']
]
columns = ['Year', 'GDP rate', 'GDP']
index = ['1', '2', '3']
df = pd.DataFrame(data, columns=columns, index=index)
print(df)
print("*"*50)