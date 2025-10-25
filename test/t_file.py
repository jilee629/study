import os

data1 = ['aa', '00']
file_path = os.path.join(os.path.dirname(__file__), "test_file.txt")

# 리스트의 string을 file에 쓰기
# w(write), a(append)
with open(file_path, "w") as f:
    f.write(' '.join(data1))
"""
aa 00
"""

# 새로운 행으로 출력하기
data2 = ['bb', '11']
with open(file_path, "a") as f:
    f.write('\n' + '\t'.join(data2))
"""
aa 00
bb 11
"""

# join() 함수를 사용하기 위해 map()을 이용해 모두 string으로 변환
data3 = list(map(str, ['cc', 22]))
with open(file_path, "a") as f:
    f.write('\n' + '\t'.join(data3))
"""
aa 00
bb 11
cc 22
"""
