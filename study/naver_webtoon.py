from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

html = requests.get('https://comic.naver.com/webtoon/weekday')
soup = bs(html.text,'html.parser')

data1_list = soup.findAll('div', {'class':'col_inner'})
# pprint(data1[0])

# 전체 웹툰 리스트
week_title_list = []

for data1 in data1_list:
    # 제목 포함영역 추출하기
    data2 = data1.findAll('a', {'class':'title'})
    # pprint(data2)

    # 텍스만 추출
    title_list = [t.text for t in data2]
    # print(title_list)
    week_title_list.append(title_list)

print(week_title_list)