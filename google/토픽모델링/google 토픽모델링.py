#크롬 드라이버 google.py 안에 있는 파일에 넣어줘야됨

from bs4 import BeautifulSoup
from selenium import webdriver #복잡한 헤더 문제 해결(구글)
import matplotlib.pyplot as plt # 시각화 패키지 가져오기
from collections import Counter #단어수 세기
from wordcloud import WordCloud #시각화
import nltk #단어토큰화, 품사구분
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk import Text

#고급설정
maxpage = 5 
query = 'covid-19 vaccine'
s_date = list('1/1/2020'.split('/'))
e_date = list('4/19/2021'.split('/'))
'''
info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
maxpage = input("최대 크롤링할 페이지 수 입력하시오: ") 
query = input("검색어를 입력해주세요: ")
s_date = input("시작날짜 입력(12/31/2020):")
e_date = input("끝날짜 입력(12/31/2021):")
'''
#tbm = input("검색 분야(전체(없음), 이미지(isch), 뉴스(nws), 동영상(vid), 도서(bks), 쇼핑(shop))")
#hl = input("언어 (한국어(ko), 영어(en))")
title_list = [] #제목
summary_list = []   #요약문


def crawler(maxpage,query,s_date,e_date):
    page = 0  
    maxpage_t =(int(maxpage)-1)*10   # 0= 1페이지 10=2페이지 20=3페이지     
    while page <=maxpage_t:
        url = 'https://www.google.com/search?q=' + query  + "&tbs=cdr%3A1%2Ccd_min%3A" + s_date[0] + "%2F" + s_date[1] + "%2F" + s_date[2] + "%2Ccd_max%3A" + e_date[0] + "%2F" + e_date[1] + "%2F" + e_date[2] + "&start=" + str(page)
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")

        list = soup.select('.g')
        for i in list:
            title_list.append(i.select_one('.LC20lb.DKV0Md').text)
            summary_list.append(i.select_one('.IsZvec').text)
        driver.close()
        page += 10

crawler(maxpage,query,s_date,e_date)

#문장
sentences = ""
for i in title_list:
    sentences += i+'.'

def get_wordnet_pos(pos_tag):
    """
    펜 트리뱅크 품사표기법(pos_tag()의 반환형태)을 받아서 WordNetLemmatizer에서 사용하는 품사표기(v, a, n, r)로 변환하는 함수.
    [매개변수]
        pos_tag: pos_tag()가 반환하는 품사
    [반환값]
        문자열: 동사-"v", 명사-'n', 형용사-'a', 부사-'r', 그외-None
    """
    if pos_tag.startswith('V'):
        return 'v'
    elif pos_tag.startswith('N'):
        return 'n'
    elif pos_tag.startswith('J'):
        return 'a'
    elif pos_tag.startswith('R'):
        return 'r'
    else:
        return None

def tokenize_text2(text):
    """텍스트 전처리 함수"""
    # 소문자로 모두 변환
    text = text.lower()
    # 문장 단위로 토큰화
    sentence_tokens = nltk.sent_tokenize(text) #[문장, 문장, 문장]

    #stopwords 조회
    stop_words = stopwords.words('english')
    stop_words.extend(['although','unless', 'may']) 

    #원형복원을 위해 객체생성
    lemm = WordNetLemmatizer()

    # 반환한 값들을 모아놓을 리스트
    word_token_list = []

    # 문장단위로 처리
    for sentence in sentence_tokens:
        # word 토큰 생성
        word_tokens = nltk.regexp_tokenize(sentence, r'[A-Za-z]+')
        # 불용어(stopword)들 제거
        word_tokens = [word for word in word_tokens if word not in stop_words]

        #Stemming
        stemmer = SnowballStemmer('english')
        word_tokens = [stemmer.stem(word) for word in word_tokens]

        # 원형 복원
        # 1. 품사부착
        word_tokens = pos_tag(word_tokens)
        # 2. lemmatize()용 품사로 변환
        word_tokens = [(word, get_wordnet_pos(tag)) for word, tag  in word_tokens if get_wordnet_pos(tag)!=None]
        # 3. 원형복원
        word_tokens = [ lemm.lemmatize(word, pos=tag) for word, tag in word_tokens]
        word_token_list.append(word_tokens)

    return word_token_list

tokens = tokenize_text2(sentences) 



##Text class


# news_tokens을 1차원 리스트로 변환
words = []
for lst in tokens:
    words = words+lst

#Text객체 생성 - Text객체가 하나의 문서(document)를 분석한다. (document-하나의 주제에대한 text)
text = Text(words, name='뉴스')

#선그래프로 단어 빈도수 출력 
plt.figure(figsize=(10,7))
text.plot(10) # 10 - 빈도수 상위 10개 단어를 선그래프로 그려준다. X축-단어, Y축-개수(빈도수)
plt.show()

#단어의 dispersion 출력
plt.figure(figsize=(10,7))
lst = ['covid', 'vaccine','health', 'new'] #원하는 단어
text.dispersion_plot(lst) # 전체 문서에서 리스트로 전달한 단어들이 출현한 위치를 시각화. X축-문서시작 ~ 문서끝
plt.show()

#wordcloud
wordcloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf',  #글씨체
                      background_color='white', #배경 색
                      width=800,    #폭
                      height=600)   #높이
counts = Counter(text)
tags = counts.most_common(30) #30개 까지
print(dict(tags))

cloud = wordcloud.generate_from_frequencies(dict(tags))
plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.show()


