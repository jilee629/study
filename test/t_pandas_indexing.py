import pandas as pd

df = pd.DataFrame({
    'phone' : ['1111', '2222', '3333'],
    'name' : ['lee', 'kim', 'park'],
    'color' : ['yellow', 'green', 'red'],
    })

## iloc는 정수 기반의 인덱싱을 사용한다.

# iloc, 2행 출력
# print(df.iloc[1])
"""
phone     2222
name       kim
color    green
Name: 1, dtype: object
"""

# iloc, 2열 출력
# print(df.iloc[:, 1])
"""
0     lee
1     kim
2    park
Name: name, dtype: object
"""


## loc는 라벨 기반의 인덱싱을 사용한다.

# loc, 2행 출력
# print(df.loc[1])
"""
phone     2222
name       kim
color    green
Name: 1, dtype: object
"""

# loc, 2행에서 3열 출력
# print(df.iloc[1, 2])
"""
green
"""

# loc, 'name'열 출력
# print(df.loc[:, 'name'])
"""
0     lee
1     kim
2    park
Name: name, dtype: object
"""

# loc, 2행에서 'color'열 출력
# print(df.loc[1, 'color'])
"""
green
"""

# 'name'열에서 값이 'kim'인 행 출력
# print(df.loc[df['name'] == 'kim'])
"""
  phone name  color
1  2222  kim  green
"""

# # 값이 일치하는 행의 열값
# 'name'에서 'kim'인 행의 'color' 열 춮력")
print(df.loc[df['name'] == 'kim', 'color'])
"""
1    green
Name: color, dtype: object
"""
