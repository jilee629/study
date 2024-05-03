import tomllib

credit = '''
        [site1]
        username = "user"
        password = "passwd"
        '''
data = tomllib.load(credit)
username = data['site1']['username']
print(username)

# with open("python/credit.toml", "rb") as f:
#     data = tomllib.load(f)
#     print(data["monpass"]["username"])