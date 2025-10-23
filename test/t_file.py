import os

data1 = ['aa', '00']
file_path = os.path.join(os.path.dirname(__file__), "file.txt")

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
    f.write('\n' + ' '.join(data2))
"""
aa 00
bb 11
"""
