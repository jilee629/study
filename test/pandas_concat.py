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

print(f"\n axis=0, Dataframe을 세로로 합치기")
df_axis_0 = pd.concat([df1, df2], axis=0)
print(df_axis_0)

print(f"\n axis=1, Dataframe을 가로로 합치기")
df_axis_1 = pd.concat([df1, df2], axis=1)
print(df_axis_1)