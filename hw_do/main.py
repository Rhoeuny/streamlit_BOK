import streamlit as st

st.title('텍스트 마이닝을 통한 금리 예측 ')

st.caption('한국은행 <Deciphering Monetary Policy Board Minutes through Text Mining Approach> 논문의 일부를 구현')

st.write("-------------------------------------------------------------------")
st.subheader("🗂️페이지 구성")
st.write("")

st.subheader("1. 문서톤과 기준금리의 상관관계")
st.write("논문 구현의 최종 결과로 동일 기간동안에 의사록 문서의 톤과 기준금리의 상관관계를 나타내는 페이지로 해당기간의 '금리' 키워드로 검색된 네이버 뉴스의 데이터 프레임까지 출력")
st.write("")

st.subheader("2. 데이터를 기반으로 제작한 극성사전")
st.write("뉴스, 채권보고서, 의사록을 통해 제작한 Dovish,Hawkish 사전 별 상위 10개 단어와 그 단어가 포함된 의사록 문장을 보여주는 페이지")
st.write("")

st.subheader("3. 의사록 문장톤을 확인하는 챗봇")
st.write("의사록 문장을 셀렉트 박스에서 선택하면 그 문장의 문장톤, 극성, 어떠한 극성 단어가 포함되어있는지를 챗봇형식으로 알려주는 페이지")
