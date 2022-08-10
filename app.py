import pandas as pd
import numpy as np
import streamlit as st

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

url = 'https://movie.naver.com/movie/point/af/list.naver'
webpage = urlopen(url).read().decode()

naver = bs(webpage, 'html.parser')
trs = naver.select('#old_content > table  tr')[1:]

df = pd.DataFrame(columns = {'col1', 'col2', 'col3', 'col4', 'col5', 'col6'})

for item in trs :
    lt = []

    tds = item.find_all('td')
    
    no = tds[0].text
    writer = tds[1].find('a').text
    em = tds[1].find('em').text
    netizen = tds[1].text.split('\n')[5:-2]
    netizen = ' '.join(netizen).strip()
    author = tds[2].text

    lt.append(no)
    lt.append(writer)
    lt.append(em)
    lt.append(netizen)
    lt.append(author[:-8])
    lt.append(author[-8:])

    idx = df.index.max()
    if np.isnan(idx) : idx = 0
    else : idx += 1

    df.loc[idx] = lt

df.columns = ['번호', '영화명', '평점', '리뷰', '작성자아이디', '작성일']
df

st.title('네이버 영화평')
st.dataframe(df)

df['평점'] = df['평점'].astype(int)
dfg = df.groupby('영화명').mean()
dfg.sort_values('평점').plot(kind = 'barh')
plt.show()