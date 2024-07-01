import streamlit as st
from datetime import datetime
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

st.set_page_config(page_title="naver news", page_icon=":이빨을_보이며_웃고_있는_얼굴:")
def get_news_item(url) :
    res = req.get(url)
    soup = bs(res.text, "html.parser")
    date = soup.select_one("span.media_end_head_info_datestamp_time")["data-date-time"]
    title = soup.select_one("h2#title_area").text
    media = soup.select_one("a.media_end_head_top_logo > img")["title"]
    content = soup.select_one("div.newsct_article").text.replace("\n", "")
    return (date, title, media, content)

def get_news(ds, de) :
    page = 1
    result = []
    search = "금리"
    while True :
        if page == 6 :
            break
        start = (page - 1) * 10 + 1
        url = f"https://s.search.naver.com/p/newssearch/search.naver?de={de}&ds={ds}&eid=&field=0&force_original=&is_dts=0&is_sug_officeid=0&mynews=0&news_office_checked=&nlu_query=&nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22finance%22%7D%7D%7D&nso=%26nso%3Dso%3Add%2Cp%3Afrom{ds.replace('.', '')}to{de.replace('.', '')}%2Ca%3Aall&nx_and_query=&nx_search_hlquery=&nx_search_query=&nx_sub_query=&office_category=0&office_section_code=0&office_type=0&pd=3&photo=0&query={search}&query_original=&service_area=0&sort=0&spq=0&start={start}&where=news_tab_api&nso=so:dd,p:from{ds.replace('.', '')}to{de.replace('.', '')},a:all"
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
st.title("네이버 뉴스")
slider_date = st.slider(
        "금리 예측 기간 선택",
        min_value = datetime(2005, 6, 6),
        max_value = datetime(2017, 1, 13),
        value = (datetime(2017, 1, 10), datetime(2017, 1, 13)),
        format= "YYYY/MM/DD")
st.write(f'{str(slider_date[0])[:10]}부터 {str(slider_date[1])[:10]}까지의 "금리" 네이버 뉴스 결과입니다.')
ds = slider_date[0]
de = slider_date[1]
if ds and de:
    df = get_news(ds.strftime("%Y%m%d"), de.strftime("%Y%m%d"))
    st.dataframe(df)