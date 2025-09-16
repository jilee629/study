import tomllib
import os

credit = '''
[site1]
username = "user1"
password = "passwd1"
'''

# loads()는 문자열을 인수로 받는다.
data = tomllib.loads(credit)
print(f"loads() : {data['site1']['username']}")

# load()는 파일을 인수로 받는다.
with open(os.path.join(os.path.dirname(__file__), 'credit.toml'), "rb") as f:
    data = tomllib.load(f)
    print(f"load() : {data['site2']['username']}")

