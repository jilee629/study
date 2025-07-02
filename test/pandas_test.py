import pandas as pd 

data = [
    ["이름1", "01035917425", 0, 0],
    ["이름2", "1035917425", 0, 0],
    ["이름3", "01035917425", 0, 0]
]
columns = ["이름", "전화번호", "생일", "기록"]
df = pd.DataFrame(data, columns=columns)
print(df)

# print(df.values.tolist())

# dd = df["전화번호"]
# print(dd)

# dd = df["전화번호"][1]
# print(dd)

df['전화번호길이'] = df['전화번호'].str.len()
print(df)

df.to_excel('test_pandas.xlsx', engine='openpyxl')

