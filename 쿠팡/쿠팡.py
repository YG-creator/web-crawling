import requests
import re
from bs4 import BeautifulSoup
import numpy as np  # numpy 패키지 가져오기
import pandas as pd # pandas 패키지 가져오기
import matplotlib.pyplot as plt # 시각화 패키지 가져오기

## 데이터 전처리
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud

## 건강 측정용품 : 114644
# 배란 측정용 : 114675
# 체온계 : 159431
# 임신테스트기 : 114676
# 당뇨관리용품 : 114677
# 혈압계 : 114678
# 체중계 : 174690
# 신장계 : 174691
category_num = input('카테고리를 입력해주세요 (1 :건강 측정용품, 2: 배란 측정용, 3 : 체온계, 4 : 임신테스트기, 5 : 당뇨관리용품, 6 : 혈압계, 7 : 체중계, 8 : 신장계)')

if category_num == '1' : category = '114644'
elif category_num == '2' : category = '114675'
elif category_num == '3' : category = '159431'
elif category_num == '4' : category = '114676'
elif category_num == '5' : category = '114677'
elif category_num == '6' : category = '114678'
elif category_num == '7' : category = '174690'
elif category_num == '8' : category = '174691'
    
title_list=[]

def word_cloud(category):
    url = 'https://www.coupang.com/np/categories/' + category + '?listSize=120&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=sale&filter=&component=120500&rating=0'
    headers = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    html = res.text
    title_list=[]
     
    #뷰티풀소프의 인자값 지정
    soup = BeautifulSoup(html, 'html.parser')
     
    #<a>태그에서 제목과 링크주소 추출
    atags = soup.select('.name')

    for atag in atags:
        title = atag.text.strip()
        title_list.append(title)     #제목
    #print(title_list)

    #3.3 형태소 분리
    sentences_tag = []
    twitter = Okt()
    for sentence in title_list:
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
    tags = counts.most_common(10)

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

word_cloud(category)
