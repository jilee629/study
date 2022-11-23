from bs4 import BeautifulSoup

tag = "<div><strong><p class='example' id='test01'> Hello World! </p></strong></div>" 
soup = BeautifulSoup(tag, 'lxml')

# find

# 태그만  특정
print(soup.find('p'))

# 속성값만 특정
print(soup.find(attrs={'class':'example'}))

# 태그와 속성값을 모두 특정
print(soup.find('p', attrs={'class':'example'}))

# select

# 특정 태그 아래에 있는 태그 찾기
print(soup.select('div p'))

# 특정 태그 바로 아래에 있는 태그 찾기
print(soup.select('div > strong > p'))

# class로 찾기 (class 시작은 '.'으로, class name이 띄어쓰기가 있으면 '.'으로 )
print(soup.select('.example'))

