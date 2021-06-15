from pytrends.request import TrendReq # 트랜드 모듈 로드
import pandas as pd     #dataframe화
import matplotlib.pyplot as plt #시각화

def trend_overtime(kw_list,time,nation):  # 키워드 - 리스트 형식이어야됨
    # 언어, 타임존 설정
    pytrends = TrendReq(hl='en-US', tz=360)

    # build the payload(키워드,시작일 끝일,나라) 가져오기
    pytrends.build_payload(kw_list, timeframe=time, geo=nation)

    #데이터 프레임화
    df = pytrends.interest_over_time()  

    #시각화
    df.plot()
    plt.show()

#입력
kw_list = ['BTS','PSY']     # 알고 싶은 keywords
start_date = input('ex) 2020-01-01, 시작일 : ')
end_date = input('ex) 2020-12-31, 끝일 : ')
time = start_date + ' ' + end_date
nation = input('ex) US, 나라 : ')

trend_overtime(kw_list,time,nation)
