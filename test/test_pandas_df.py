import pandas as pd

data = {'name' : ['A', 'B', 'C'], 'id' : ['a', 'b', 'c'], 'age' : ['11', '12', '13']}
df = pd.DataFrame(data)
print(df)

# data = [['A', 'a', '11'], ['B', 'b', '12'], ['C', 'c', '13']]
# columns = ['name', 'id', 'age']
# index = ['1', '2', '3']
# df = pd.DataFrame(data, columns=columns, index=index)
# print(df)


print(f"\n{df.values.tolist()}")

print(f"\n{df['age']}")

print(f"\n{df['age'][1]}")




