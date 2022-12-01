import requests, json

res = requests.get("https://jsonplaceholder.typicode.com/users/1")

# # binary를 얻음
# print('# res.content')
# print(res.content)

# # string을 얻음
# print('# res.text')
# print(res.text)

# # dict를 얻음
# print('# res.json')
# print(res.json())

# print('# res.headers')
# print(res.headers)
# print(res.headers['Content-Type'])

url = "https://api.monpass.im/api/crm/users/phone/01074901170"
params={
    'Remote Address': '15.164.202.173:443',
    'Referrer Policy': 'strict-origin-when-cross-origin'
}
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Access-Control-Request-Headers': 'token',
    'Access-Control-Request-Method': 'GET',
    'Connection': 'keep-alive',
    'Host': 'api.monpass.im',
    'Origin': 'https://partner.monpass.im',
    'Referer': 'https://partner.monpass.im/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.3'
}
res = requests.request('options', url=url, headers=headers, params=params)
print(res.status_code)
print(res.headers)
print(res.cookies)
print(res.text)