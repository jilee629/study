import tomllib

credit = '''
        [monpass]
        username = "user"
        password = "passwd"
        '''

data = tomllib.load(credit)
print(data["monpass"]["username"])
    
# with open("python/credit.toml", "rb") as f:
#     data = tomllib.load(f)
#     print(data["monpass"]["username"])