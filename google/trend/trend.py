import matplotlib.pyplot as plt     #시각화        
from matplotlib import rc   #시각화
import pandas as pd     #Data frame
from pytrends.request import TrendReq   #구글 트랜드
rc('font', family = 'DejaVu Sans') #한글깨짐 방지
'''
#시간에 따른 변화 
keywords = ['Corona symptoms','Corona Vaccine']      #리스트 형식이어야됨
pytrends = TrendReq(hl='en-US', tz=360) #언어 타임존
pytrends.build_payload(kw_list = keywords, timeframe = 'today 5-y') #지금으로부터 5개년
df_ot = pytrends.interest_over_time()    
df_ot.plot()
plt.show()    
#df_ot.to_csv('trend.csv', mode='w', index = None) #csv로 저장

'''
#연관어
keyword = 'Corona symtoms' #키워드 입력
pytrends = TrendReq(hl='en-US', tz=360) #언어 타임존
pytrends.build_payload(kw_list=[keyword], timeframe='2020-01-01 2021-05-15', geo='US')
df_rt = pytrends.related_topics()   #관련어
df_rq = pytrends.related_queries()  #관련 질문
df_s = pytrends.suggestions(keyword)    #추천 검색 키워드
print(df_rt[keyword]['rising'].head(5))
print(df_rt[keyword]['top'].head(5))
print(df_rq)
print(df_s)

'''
#인기 검색어
pytrends = TrendReq(hl='en-US', tz=360) #언어 타임존
pytrends.trending_searches(pn='united_states')  
print(pytrends.top_charts(date='2020', hl='en-US', tz=360, geo='US'))
'''

'''
##keyword 전체,나라별 트렌드

import pandas as pd
from pytrends.request import TrendReq
import datetime
from iso3166 import countries

def interest_processing(geo, country_name) :
    pytrend.build_payload(kw_list = keyword, timeframe = timerange, geo = geo, cat = 3)
    dt = pytrend.interest_over_time()
    try:
        # delete unnecessary colmun 
        del dt['isPartial']
        # renmae column name
        dt.rename(columns = {'korea' : country_name}, inplace = True)
        return dt
    except:
        pass

#key word
keyword = ["KOREA"]
pytrend = TrendReq()

# set date
today = datetime.datetime.now()
startdate = '2012-12-01'
enddate = str(today.date())
timerange = startdate + ' ' + enddate

# 전세계 data
result = pd.DataFrame()
pytrend.build_payload(kw_list = keyword, timeframe = timerange)
total = pytrend.interest_over_time()
period = total.index.values
total = total['KOREA'].values
result['period'] = period
result['total'] = total

# 국가별 data
for c in countries:
    geo = c.alpha2
    country_name = c.name
    new = interest_processing(geo, country_name)
    print(country_name)
    try:
        new.reset_index(drop = True, inplace = True)
        result.reset_index(drop = True, inplace = True)
        result = pd.concat([result, new], ignore_index = False, axis = 1)
    except:
        pass

#csv로 저장
print(result)
result.to_csv('google_trend.csv', mode='w', index = None)
'''
