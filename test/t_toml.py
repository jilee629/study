import tomllib
import os

credit = '''
[site1]
username = "user1"
password = "passwd1"
'''

# loads()는 문자열을 인수로 받는다.
data = tomllib.loads(credit)
id1 = data['site1']['username']
# print(id1)
# user1

# load()는 파일을 인수로 받는다.
with open(os.path.join(os.path.dirname(__file__), 'test.toml'), "rb") as f:
    data = tomllib.load(f)
    id2 = data['site2']['username']
    # print(id2)
# user2
