import tomllib



data = tomllib.load(credit)
print(data["monpass"]["username"])

credit = '''
        [monpass]
        username = "user"
        password = "passwd"
        '''
            
# with open("python/credit.toml", "rb") as f:
#     data = tomllib.load(f)
#     print(data["monpass"]["username"])