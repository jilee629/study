import pandas as pd

data = ['kim', 'park', 'kim', 'lee', 'choi']

columns = ['name']
df = pd.DataFrame(data, columns=columns)
print(df)

print("\n Add colums by dataframe")
age = ['20', '22', '21', '22', '21']
df['age'] = pd.DataFrame(age)
print(df)

print("\n Add columns by list")
city = ['seoul', 'seoul', 'yeosu', 'incheon', 'daegu']
df['city']  = city
print(df)

print("\n Concatenate each dataframe")
sex = ['male', 'female', 'male', 'female', 'female']
df1 = pd.DataFrame(sex, columns=['sex'])
df2 = pd.concat([df, df1], axis=1)
print(df2)

