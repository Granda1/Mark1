import requests
from bs4 import BeautifulSoup
hdr = {'user-agent' : ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')}
address = 'http://it.chosun.com/svc/list_in/search.html?sort=regdate&query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4'

# '0. it조선 홈페이지에서 "메타버스"검색 결과 페이지로 이동하는 코드'
it_chosun = 'http://it.chosun.com/'
it_chosun_metaverse = it_chosun + '/svc/list_in/search.html?sort=regdate&query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4'

# '1. 모든 메타버스 페이지의 주소 개수를 구하는 코드이다.'
# for_article_number = BeautifulSoup(requests.get(address).text, 'html.parser')
# all_article_number = int(for_article_number.find('div','head_top').find('h2').find('span').get_text()[0:4])
# print(all_article_number) #현 시각으로는 1043개이다.

'2. 이 아래의 과정은 모든 메타버스 페이지의 주소를 가져다 준다.'
URL = it_chosun_metaverse + '&sort=regdate&pn='
# URL = 'https://it.chosun.com/svc/list_in/search.html?query=%EB%A9%94%ED%83%80%EB%B2%84%EC%8A%A4&sort=regdate&pn='
page_lists = []
for i in range(1,10):    #일단 all_article_number+1 대신에 10을 넣었다.
    page_lists.append(URL+str(i))
# print(page_lists)
# 이로써 모든 page를 담고 있는 리스트를 얻었다.


'html1은 1페이지 안에 있는 모든 기사들의 url을 담고 있는 html을 반환한다.'
# html1 = BeautifulSoup(requests.get(page_lists[0]).text,'html.parser')
# print(html1)  # html1에는 1페이지에 있는 모든 기사들의 url을 담고 있는 html을 반환해준다.

ales = [] # ales에는 모든 페이지의 html이 들어가 있다.
for j in range(len(page_lists)):
    ales.append(BeautifulSoup(requests.get(page_lists[j],headers=hdr).text,'html.parser'))

#ales_html에는 html중에서 tag가 div, class가 txt_wrap인 것들이 있다.
ales_html = [ales[x].find_all('div','txt_wrap') for x in range(len(ales))]
ales_html = sum(ales_html,[]) #find_all을 하면 자동으로 리스트가 또 생성된다. 고로 flatten 시킬 필요가 있다.
# print(ales_html)

#ales_url #이로써 9개의 페이지로부터 90개의 url을 구했다.
ales_url = [y.find('a')['href'] for y in ales_html]
# print(ales_url)

'4. 이제 각 기사 URL에서 제목, 본문, 날짜를 가져오는 코드를 짜보자.'
#이건 1페이지 첫 번째 기사의 주소이다.
# article1_address = all_html[0]
# article1 = BeautifulSoup(requests.get(article1_address).text,'html.parser')
# print(article1_address)
#article1이란 1페이지 첫번째 기사의 html이다.

#일단 각 기사의 html을 구했다.
articles_html = [BeautifulSoup(requests.get(i3).text,'html.parser') for i3 in ales_url]
# print(title_html)

title = [i1.find('div','news_title_text').find('h1').get_text() for i1 in articles_html]
# print(title) #이로서 9개 페이지의 기사 제목들을 전부 긁어왔다.

#이번에는 날짜. 다만 연월일만 뽑는 법은 무식한 slicing으로 했다.
date = [i2.find('div','news_date').get_text()[3:13] for i2 in articles_html]
# print(date) #이로서 9개 페이지의 기사 날짜들을 전부 긁어왔다.


# #마지막으로 본문을 뽑아냈다. 이중리스트를 한 이유는 zip을 하면 첫번재 par만 zip되기 때문이다.
# body = article1.find_all('div','par')
body = [i4.find_all('div','par') for i4 in articles_html]
# print(body)
# #body[0]을 print하면 기사 본문 하나의 리스트가 나온다. 허나, 리스트 안에 있을뿐이지, type을 치면 class 'bs4.element.ResultSet'가 나온다.

# only_text_body = [[only_text.get_text() for only_text in body]]
# only_body = [i5.get_text() for i5 in body]
# print(only_body[0])

# #이제 제목, 날짜, 본문을 모두 가져왔다.
article_final = list(zip(title,date,body))
# print(article_final)


#마지막으로 할 과제는 body에서 깔끔하게 문자만 get_text()로 구하는 것