from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

html = requests.get('https://search.naver.com/search.naver?query=날씨')
soup = bs(html.text,'html.parser')

# find('tag', {dic형속성})
data1 = soup.find('ul', {'class':'today_chart_list'})
# pprint(data1)

data2 = data1.findAll('li')
# pprint(data2[0])

find_dust = data2[0].find('span', {'class':'txt'}).text
print(find_dust)

