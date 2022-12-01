# 변수를 증가해서 index 추가
i = 0
for letter in ['A', 'B', 'C']:
    print(i, letter)
    i += 1
'''
0 A
1 B
2 C
'''

# enumrate 이용해서 index 추가
for i, letter in enumerate(['A', 'B', 'C']):
    print(i, letter)
'''
0 A
1 B
2 C
'''

# enumrate 이용해서 index 추가
# 기본적으로 tuple로 반환
for entry in enumerate(['A', 'B', 'C']):
    print(entry)
'''
(0, 'A')
(1, 'B')
(2, 'C')
'''

