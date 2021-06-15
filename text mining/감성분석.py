import os #경로 설정
import rhinoMorph #형태소 분석
from sklearn.model_selection import GridSearchCV #그리드 서치
#로지스틱 회귀분석 적용
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer #행렬로 변환
from collections import Counter #Counter 클래스를 이용해 각 분류가 같은 비율로 들어갔는지 확인해 본다
from sklearn.model_selection import train_test_split #훈련데이터와 테스트데이터로 분리

os.chdir("C:/Users/YG/Desktop/test")                  # 경로 설정
'''
##데이터 로딩

# 파일 읽기 함수 정의 
def read_data(filename):
    with open(filename, 'rt',encoding='UTF8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]                    # 파일의 헤더(컬럼명) 제외
    return data

# 파일 쓰기 함수 정의
def write_data(data, filename):
    with open(filename, 'w') as f:
        f.write(data)

data = read_data('ratings.txt')

##형태소 분석기 기동
rn = rhinoMorph.startRhino()  

# 20만 건 전체 문장 형태소 분석. 시간이 많이 소요됨 
morphed_data = ''
for data_each in data:
    morphed_data_each = rhinoMorph.onlyMorph_list(rn, data_each[1], pos=['NNG', 'NNP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'])
    joined_data_each = ' '.join(morphed_data_each)
    if joined_data_each:                                                                                                      # 내용이 있는 경우만 저장함
        morphed_data += data_each[0]+"\t"+joined_data_each+"\t"+data_each[2]+"\n"   # 원본과 같은 양식으로 만듦

# 형태소 분석된 파일 저장
write_data(morphed_data, 'ratings_morphed.txt')
'''
rn = rhinoMorph.startRhino()  
#형태소 분석된 파일 다시 불러들이기

def read_data(filename):
    with open(filename, 'r', encoding="cp949") as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]                                       # 파일의 헤더(컬럼명) 제외
    return data

data = read_data('ratings_morphed.txt')    # 1은 긍정, 0은 부정

#훈련데이터와 테스트데이터로 분리
data_text = [line[1] for line in data]             # 훈련데이터 본문
data_senti = [line[2] for line in data]           # 훈련데이터 긍부정 부분
train_data_text, test_data_text, train_data_senti, test_data_senti = train_test_split(data_text, data_senti, stratify=data_senti)
# Counter 클래스를 이용해 각 분류가 같은 비율로 들어갔는지 확인해 본다
train_data_senti_freq = Counter(train_data_senti)
#print('train_data_senti_freq:', train_data_senti_freq)
test_data_senti_freq = Counter(test_data_senti)
#print('test_data_senti_freq:', test_data_senti_freq)

#행렬로 변환
vect = CountVectorizer(min_df=5).fit(train_data_text)
X_train = vect.transform(train_data_text)
#print("X_train:\n", repr(X_train))
feature_names = vect.get_feature_names()
#print("특성 개수:", len(feature_names))
#print("처음 20개 특성:\m", feature_names[:20])
#print("3000~5000까지의 특성:\n", feature_names[3000:5000])

#로지스틱 회귀분석 적용
y_train = pd.Series(train_data_senti)
scores = cross_val_score(LogisticRegression(solver="liblinear"), X_train, y_train, cv=5)
#print('교차 검증 점수:', scores)
#print('교차 검증 점수 평균:', scores.mean())

#그리드 서치
param_grid = {'C': [0.01, 0.1, 1, 3, 5]}
grid = GridSearchCV(LogisticRegression(solver="liblinear"), param_grid, cv=5)
grid.fit(X_train, y_train)
#print("최고 교차 검증 점수:", round(grid.best_score_, 3))
#print("최적의 매개변수:", grid.best_params_)

#테스트 데이터에 적용하기
X_test = vect.transform(test_data_text)
y_test = pd.Series(test_data_senti)
#print("테스트 데이터 점수:", grid.score(X_test, y_test))


# 파일을 새로 열었으므로 형태소분석기도 다시 기동한다. 
# 만약 한 페이지로 연결되어 있으면 아래의 두 줄은 삭제한다 
new_input = '오늘은 정말 실망 스러운 하루구나!'
# 입력 데이터 형태소 분석하기 
inputdata = []
morphed_input = rhinoMorph.onlyMorph_list(rn, new_input, pos=['NNG', 'NNP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'])
morphed_input = ' '.join(morphed_input)                     # 한 개의 문자열로 만들기
inputdata.append(morphed_input)                               # 분석 결과를 리스트로 만들기
X_input = vect.transform(inputdata)
result = grid.predict(X_input) # 0은 부정,1은 긍정
if result == 0:
    print(f"'{new_input}'은 부정적인 글입니다")
else:
    print(f"'{new_input}'은 긍정적인 글입니다")


