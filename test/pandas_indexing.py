import pandas as pd

df = pd.DataFrame({
    'phone' : ['1111', '2222', '3333'],
    'name' : ['lee', 'kim', 'park'],
    'color' : ['yellow', 'green', 'red'],
    })
print(f"데이터 프레임\n{df}")

## iloc는 정수 기반의 인덱싱을 사용한다.
## loc는 라벨 기반의 인덱싱을 사용한다.

print("\n 두번째 행 출력")
print(f"-> iloc\n{df.iloc[1]}")
print(f"-> loc\n{df.loc[1]}\n")

print("\n 두번째 열 출력")
print(f"-> iloc\n{df.iloc[:, 1]}")
print(f"-> loc\n{df.loc[:, 'name']}\n")

print("\n 두번재 행에서 3번재 열 출력")
print(f"-> iloc : {df.iloc[1, 2]}")
print(f"-> loc : {df.loc[1, 'color']}")

# 값이 일치하는 행 출력
print("\n name이 'kim'인 행 출력")
print(df.loc[df['name'] == 'kim'])

# 값이 일치하는 행의 열값
print("\n name이 'kim'인 행의 color 열 춮력")
print(df.loc[df['name'] == 'kim', 'color'])