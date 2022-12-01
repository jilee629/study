import requests

res = requests.get('http://naver.com')
res.raise_for_status()

print(res.text)

with open("mynaver.html", "w", encoding="utf8") as f:
    f.write(res.text)