from bs4 import BeautifulSoup as bs
import requests, re, os
from pprint import pprint
from urllib.request import urlretrieve

# 저장 폴더 추가
try:
    if not (os.path.isdir('image')):
        os.makedirs(os.path.join('image'))
except OSError as e:
    if e.errno != errno.EEXIST:
        print('폴더생성실패')
        exit()

html = requests.get('https://comic.naver.com/webtoon/weekday')
soup = bs(html.text,'html.parser')

data1_list = soup.findAll('div', {'class':'col_inner'})
# pprint(data1_list)

li_list = []
for data1 in data1_list:
    li_list.extend(data1.findAll('li'))

# pprint(li_list)
'''
<li>
<div class="thumb">
<a href="/webtoon/list?titleId=799213&amp;weekday=sun" onclick="nclk_v2(event,'thm*S.img','','79')">
<img alt="어떤소란" height="107" onerror="this.src='https://ssl.pstatic.net/static/comic/images/migration/common/blank.gif'" src="https://shared-comic.pstatic.net/thumb/webtoon/799213/thumbnail/thumbnail_IMAG21_3d88ad40-2cca-4255-a00c-a5d9dab3c29f.jpg" title="어떤소란" width="83"/><span class="mask"></span>
</a>
</div>
<a class="title" href="/webtoon/list?titleId=799213&amp;weekday=sun" onclick="nclk_v2(event,'thm*S.tit','','79')" title="어떤소란">어떤소란</a>
</li>
'''

# 각각의 썸네일과 제목 추출하기
for li in li_list:
    img = li.find('img')
    title = img['title']
    img_src = img['src']
    print(title, img_src)
    title = re.sub('[^0-9a-zA-Zㄱ-힗]', '', title)
    urlretrieve(img_src, './image/' + title + '.jpg')