import requests, json

res = requests.get("https://jsonplaceholder.typicode.com/users/1")

# # # binary를 얻음
# print(type(res.content))
# print(res.content)

# # # string을 얻음
# print(type(res.text))
# print(res.text)

# # dict를 얻음
# print(type(res.json()))
# print(res.json())

print(res.headers)
print('\nContent-Type: ', res.headers['Content-Type'])

