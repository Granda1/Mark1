import requests
from bs4 import BeautifulSoup
address = 'http://it.chosun.com/svc/list_in/search.html?sort=regdate&query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4'
test1 = BeautifulSoup(requests.get(address).text, 'html.parser')
# print(test1)

# '1. 모든 메타버스 페이지의 주소 개수를 구하는 코드이다.'
all_article_number = int(test1.find('div','head_top').find('h2').find('span').get_text()[0:4])
# print(all_article_number) #현 시각으로는 1044개이다.

'2. 이 아래의 과정은 모든 메타버스 페이지의 주소를 가져다 준다.'
# URL = 'https://it.chosun.com/svc/list_in/search.html?query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4&sort=regdate&pn='
# page_lists = []
# for i in range(1,all_article_number+1):
#     page_lists.append(URL+str(i))
# print(page_lists)

'3. 각 페이지에서 각 기사 URL을 가져오는 코드이다.'
bodies = test1.find('div','txt_wrap').find('a')['href'] #기사 하나의 URL을 얻었다.
# print(bodies)
#일단 검사 내의 모든 정보들을 가져온다.
all_bodies = test1.find_all('div','txt_wrap')
# print(all_bodies[0]) #이미 find_all 함수를 쓰면 리스트 안에 값들이 저장된다.
#그리고 한 페이지 안에 있는 모든 기사들의 주소들을 가져왔다.
all_html = [html.find('a')['href'] for html in all_bodies]
# print(all_html)


'4. 이제 각 기사 URL에서 제목, 본문, 날짜를 가져오는 코드를 짜보자.'
#이건 1페이지 첫 번째 기사의 주소이다.
article1_address = all_html[0]
article1 = BeautifulSoup(requests.get(article1_address).text,'html.parser')
# print(article1_address)

#기사의 제목을 가져왔다.
title = [article1.find('div','news_title_text').find('h1').get_text()]
# print(title)

#이번에는 날짜. 다만 연월일만 뽑는 법은 무식한 slicing으로 했다.
date = [article1.find('div','news_date').get_text()[3:13]]
# print(date)

#마지막으로 본문을 뽑아냈다. 이중리스트를 한 이유는 zip을 하면 첫번재 par만 zip되기 때문이다.
body = article1.find_all('div','par')
only_text_body = [[only_text.get_text() for only_text in body]]
print(only_text_body)

#이제 제목, 날짜, 본문을 모두 가져왔다.
article1_final = list(zip(title,date,only_text_body))
# print(article1_final)


