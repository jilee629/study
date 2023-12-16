import tomllib

with open("python/credit.toml", "rb") as f:
    data = tomllib.load(f)
    print(data["monpass"]["username"])