#지지도(support) : P(A교B)/전체
#신뢰도(confidence) : P(A교B)/P(A)
#향상도(lift) : A가 주어지지 않을 때의 품목 B의 확률에 비해 A가 주어졌을 때 품목 B의 증가 비율
#         향상도가 1이면 독립

#장바구니 분석
import pandas as pd #행열로 이루어진 데이터 객체 만듦
from mlxtend.preprocessing import TransactionEncoder #데이터 사이언스 작업도구
from mlxtend.frequent_patterns import apriori, association_rules

dataset = [['Milk', 'Onion', 'Nutmeg', 'Eggs', 'Yogurt'],  #장바구니 데이터
           ['Onion', 'Nutmeg', 'Eggs', 'Yogurt'],
           ['Milk', 'Apple', 'Eggs'],
           ['Milk', 'Unicorn', 'Corn', 'Yogurt'],
           ['Corn', 'Onion', 'Onion', 'Ice cream', 'Eggs']]

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset) #dataset 교유라벨 갖게함
df = pd.DataFrame(te_ary, columns=te.columns_) #리스트를 배열로 변환
#print(df)

frequent_itemsets = apriori(df, min_support=0.5, use_colnames=True) #지지도 0.5이상인 것들만
#print(frequent_itemsets)

result = association_rules(frequent_itemsets, metric="lift", min_threshold=1) #지지도 0.5이상, 향상도 1이상인 것들만
print(result)
