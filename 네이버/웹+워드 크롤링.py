import numpy as np  # numpy 패키지 가져오기
import pandas as pd # pandas 패키지 가져오기
import matplotlib.pyplot as plt # 시각화 패키지 가져오기

## 데이터 전처리
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud

from bs4 import BeautifulSoup
import requests

info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")  
query = input("검색어 입력: ")  
sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")
s_date = input("시작날짜 입력(2021.01.01):")
e_date = input("끝날짜 입력(2021.03.26):")
title_list = []

def crawler(maxpage,query,sort,s_date,e_date):
    s_from = s_date.replace(".","")
    e_to = e_date.replace(".","")
    page = 1  
    maxpage_t =(int(maxpage)-1)*10+1   # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지
    
    while page <=maxpage_t:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
        req = requests.get(url)
 
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.select('div.news_wrap.api_ani_send > div > a')

        for title in titles:
            title_list.append(title['title'])
        page += 10

crawler(maxpage,query,sort,s_date,e_date)

#3.2 단어 리스트 만들기
word_list = title_list

#3.3 형태소 분리
sentences_tag = []
twitter = Okt()
for sentence in word_list:
    morph = twitter.pos(sentence)
    sentences_tag.append(morph)

#3.4. 명사만 추출
noun_list = []
for sentence in sentences_tag:
    for word, tag in sentence:
        if tag in ['Noun']:
            noun_list.append(word)


#3.6 단어 카운트
counts = Counter(noun_list)
tags = counts.most_common(30)
tags

#4.WordCloud생성
wordcloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf',  #글씨체
                      background_color='white', #배경 색
                      width=800,    #폭
                      height=600)   #높이

print(dict(tags))

cloud = wordcloud.generate_from_frequencies(dict(tags))
plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.show()

