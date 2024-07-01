import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import matplotlib.font_manager as fm

st.title('📈논문 구현 : 금리 예측')


#사이드 바 기능 추가
with st.sidebar:
    sdt = st.date_input('조회 시작일을 선택해주세요',pd.to_datetime('2005-06-01'))
    edt = st.date_input('조회 종료일을 선택해주세요',pd.to_datetime('2020-01-01'))


# 콜금리,문서톤 데이터 불러오기
final_data = pd.read_csv("./streamlit_BOK/hw_do/data/doc_tone_base_rate.csv")
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



import seaborn as sns
# seaborn 설치 필요!
graph1 = plt.figure()
sns.regplot(x = "doc_tone", y = "baserate", data = date_df)
plt.xlabel("어조")
plt.ylabel("기준금리")
plt.title("의사록 어조에 따른 기준금리 분포")
st.pyplot(graph1)

