#read document
from nltk.corpus import gutenberg   # Docs from project gutenberg.org
files_en = gutenberg.fileids()      # Get file ids
doc_en = gutenberg.open('austen-emma.txt').read()

#문서를 토큰으로 나눔
from nltk import regexp_tokenize :
pattern = r'''(?x) ([A-Z]\.)+ | \w+(-\w+)* | \$?\d+(\.\d+)?%? | \.\.\. | [][.,;"'?():-_`]'''
tokens_en = regexp_tokenize(title_list, pattern)

#Load tokens
import nltk
en = nltk.Text(tokens_en)

#tokens
en.vocab()                  # returns frequency distribution

# Plot sorted frequency of top 50 tokens
en.plot(10)

#Plot 저장
from matplotlib import pylab
pylab.show = lambda: pylab.savefig('some_filename.png')

#For those who see rectangles instead of letters in the saved plot file, include the following configurations before drawing the plot:
from matplotlib import font_manager, rc
font_fname = 'c:/windows/fonts/gulim.ttc'     # A font of your choice
font_name = font_manager.FontProperties(fname=font_fname).get_name()
rc('font', family=font_name)

#count
en.count('Emma')        # Counts occurrences

#Dispersion plot
en.dispersion_plot(['Emma', 'Frank', 'Jane']) #원하는 단어

#concordance
en.concordance('Emma', lines=5)

#find similar words
en.similar('Emma')

#collocations
en.collocations()

#품사 구분
tokens = "The little yellow dog barked at the Persian cat".split()
tags_en = nltk.pos_tag(tokens)

#chunking
parser_en = nltk.RegexpParser("NP: {<DT>?<JJ>?<NN.*>*}")
chunks_en = parser_en.parse(tags_en)
chunks_en.draw()

#빈도분포표
data = en.vocab().items()
print(data)


#빈도분포표 저장
import csv
with open('words.csv', 'w', encoding='utf-8') as f:
    f.write('word,freq\n')
    writer = csv.writer(f)
    writer.writerows(data)

#웹에 올리기
python -m http.server 8888

#주소창에 http://localhost:8888 치면 확인가능
