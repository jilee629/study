import pandas as pd 

data = [
    ["이름1", "01035917425", 0, 0],
    ["이름2", "1035917425", 0, 0],
    ["이름3", "01035917425", 0, 0]
]
columns = ["이름", "전화번호", "생일", "기록"]
df = pd.DataFrame(data, columns=columns)

# dataframe을 list로 변환
df_list = df.values.tolist()
# print(df_list)
"""
[['이름1', '01035917425', 0, 0], ['이름2', '1035917425', 0, 0], ['이름3', '01035917425', 0, 0]]
"""

# dataframe에서 '전화번호'열 출력
dd = df["전화번호"]
# print(dd)
"""
0    01035917425
1     1035917425
2    01035917425
"""

# dataframe에서 '전화번호'열의 2번째 행 값
dd = df["전화번호"][1]
# print(dd)
"""
1035917425
"""

# dataframe에 "전화번호길이" 열 추가
df['전화번호길이'] = df['전화번호'].str.len()
# print(df)
"""
    이름         전화번호  생일  기록  전화번호길이
0  이름1  01035917425   0   0      11
1  이름2   1035917425   0   0      10
2  이름3  01035917425   0   0      11
"""

# dataframe을 excel file로 출력
df.to_excel('test_pandas.xlsx', engine='openpyxl')

