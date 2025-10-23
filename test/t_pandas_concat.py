import pandas as pd

df1 = pd.DataFrame({
    'phone' : ['1111', '2222', '3333'],
    'name' : ['lee', 'kim', 'park'],
    'color' : ['yellow', 'green', 'red'],
    })
df2 = pd.DataFrame({
    'phone' : ['1111', '2222', '3333'],
    'city' : ['seoul', 'incheon', 'seoul']
    })

# axis=0, Dataframe을 세로로 합치기
df_axis_0 = pd.concat([df1, df2], axis=0)
# print(df_axis_0)
"""
  phone  name   color     city
0  1111   lee  yellow      NaN
1  2222   kim   green      NaN
2  3333  park     red      NaN
0  1111   NaN     NaN    seoul
1  2222   NaN     NaN  incheon
2  3333   NaN     NaN    seoul
"""

# axis=1, Dataframe을 가로로 합치기
df_axis_1 = pd.concat([df1, df2], axis=1)
# print(df_axis_1)
"""
  phone  name   color phone     city
0  1111   lee  yellow  1111    seoul
1  2222   kim   green  2222  incheon
2  3333  park     red  3333    seoul
"""
