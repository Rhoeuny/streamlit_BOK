import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import requests as req
from bs4 import BeautifulSoup as bs
import matplotlib.font_manager as fm

st.title('📈논문 구현 : 금리 예측')
st.write("")

#사이드 바 기능 추가
with st.sidebar:
    sdt = st.date_input('조회 시작일을 선택해주세요',pd.to_datetime('2005-06-01'))
    edt = st.date_input('조회 종료일을 선택해주세요',pd.to_datetime('2020-01-01'))


# 콜금리,문서톤 데이터 불러오기
final_data = pd.read_csv("hw_do/data/doc_tone_base_rate.csv")
# 데이터 프레임 변환
df = pd.DataFrame(final_data)
df['date'] = pd.to_datetime(df['date'])
date_df = df[(df['date']>= pd.Timestamp(sdt)) & (df['date']<=pd.Timestamp(edt))]

# 차트
test = plt.figure(figsize=(10,7))
plt.rcParams["axes.unicode_minus"] = False
ax1 = date_df.doc_tone.plot(color='blue', grid=True, label='금통위 의사록 어조')
ax2 = date_df.baserate.plot(color='red', grid=True, secondary_y=True, label='기준금리')
# 왼쪽 y축 범위 설정
ax1.set_ylim(-1, 0)
plt.show()



st.subheader('기준금리와 문서톤의 상관관계')
# 그래프 출력
st.pyplot(test)
# 데이터 프레임 출력(정렬 기능 제공)
st.dataframe(date_df, use_container_width = True)

st.write("-------------------------------------------------------------------")


st.subheader('산점도 및 추세선')
st.write('의사록 어조에 따른 기준금리 분포')


import seaborn as sns
# seaborn 설치 필요!
graph1 = plt.figure()
sns.regplot(x = "doc_tone", y = "baserate", data = date_df)
st.pyplot(graph1)

# st.caption('x축 : 어조  / y축 : 기준금리')


# 선택 날짜 네이버 뉴스 검색
def get_news_item(url) :
    res = req.get(url)
    soup = bs(res.text, "html.parser")
    date = soup.select_one("span.media_end_head_info_datestamp_time")["data-date-time"]
    title = soup.select_one("h2#title_area").text
    media = soup.select_one("a.media_end_head_top_logo > img")["title"]
    content = soup.select_one("div.newsct_article").text.replace("\n", "")
    return (date, title, media, content)

def get_news(sdt, edt) :
    page = 1
    result = []
    search = "금리"
    while True :
        if page == 11 :
            break
        start = (page - 1) * 10 + 1
        url = f"https://s.search.naver.com/p/newssearch/search.naver?de={edt}&ds={sdt}&eid=&field=0&force_original=&is_dts=0&is_sug_officeid=0&mynews=0&news_office_checked=&nlu_query=&nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22finance%22%7D%7D%7D&nso=%26nso%3Dso%3Add%2Cp%3Afrom{sdt.replace('.', '')}to{edt.replace('.', '')}%2Ca%3Aall&nx_and_query=&nx_search_hlquery=&nx_search_query=&nx_sub_query=&office_category=0&office_section_code=0&office_type=0&pd=3&photo=0&query={search}&query_original=&service_area=0&sort=0&spq=0&start={start}&where=news_tab_api&nso=so:dd,p:from{sdt.replace('.', '')}to{edt.replace('.', '')},a:all"
        res = req.get(url)
        doc = eval(res.text.replace("\n", ""))
        for lst in doc["contents"] :
            soup = bs(lst, "html.parser")
            a_tags = soup.select("div.info_group > a")
            if len(a_tags) == 2 :
                try :
                    result.append(get_news_item(a_tags[-1]["href"]))
                except Exception as e :
                    print("오류 : ", e)
        page += 1
    return pd.DataFrame(columns = ["date", "title", "media", "content"], data = result)

st.write("-------------------------------------------------------------------")

st.subheader("네이버 뉴스")
st.write(f"{sdt.strftime('%Y-%m-%d')}부터 {edt.strftime('%Y-%m-%d')}까지의 [금리] 네이버 뉴스 '관련도순' 검색 결과입니다.")

if sdt and edt :
    df_news = get_news(sdt.strftime("%Y%m%d"), edt.strftime("%Y%m%d"))
    st.dataframe(df_news)