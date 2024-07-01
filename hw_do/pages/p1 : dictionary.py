import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
# 폰트 프로퍼티를 가져옵니다.
font_prop = fm.FontProperties(fname=font_path, size=12)
# matplotlib의 rcParams를 통해 전역 폰트 설정을 변경
plt.rcParams['font.family'] = 'AppleGothic'


st.title('극성 사전')

neg_dic = pd.read_csv("hw_do/data/total_dov_dic.csv")
pos_dic = pd.read_csv("hw_do/data/total_haw_dic.csv")
pos_dic = pos_dic.rename(columns={'Unnamed: 0': 'H_Key'})
neg_dic = neg_dic.rename(columns={'Unnamed: 0': 'D_Key'})

neg_sent = pd.read_csv("hw_do/data/do_ngram_minsent.csv")
pos_sent = pd.read_csv("hw_do/data/hw_ngram_minsent.csv")

#----------------------------------------------------------------------------

neg_10 = neg_dic.sort_values('Down', ascending=False).head(10)
neg_10['D_Key'] = neg_10['D_Key'].apply(lambda x: x.split('/')[0])
# 막대 그래프 생성
n_fig, n_ax = plt.subplots()
n_bars = n_ax.bar(neg_10['D_Key'], neg_10['Down'],color = 'orange')
for n_bar in n_bars:
    yval = n_bar.get_height()
    n_ax.text(n_bar.get_x() + n_bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')



st.header('🕊️DOVISH 사전')

dic, n_bar = st.columns(2)
dic.dataframe(neg_dic)
n_bar.pyplot(n_fig)

st.subheader('🕊️n-gram이 포함된 의사록 문장')
neg_11 = neg_dic.sort_values('Down', ascending=False).head(10)
n_options = neg_11['D_Key'].unique()
select_option = st.selectbox('값을 선택하세요:', n_options)

neg_sent = neg_sent.drop('Unnamed: 0',axis=1)
filtered_ndf = neg_sent[neg_sent['Dovish'] == select_option]
st.dataframe(filtered_ndf)
#----------------------------------------------------------------------------

pos_10 = pos_dic.sort_values('Up', ascending=False).head(10)
pos_10['H_Key'] = pos_10['H_Key'].apply(lambda x: x.split('/')[0])
# 막대 그래프 생성
h_fig, h_ax = plt.subplots()
h_bars = h_ax.bar(pos_10['H_Key'], pos_10['Up'],color = 'blue')
for h_bar in h_bars:
    yval = h_bar.get_height()
    h_ax.text(h_bar.get_x() + h_bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')


st.header('🦅HAWKISH 사전')

dic, h_bar = st.columns(2)
dic.dataframe(pos_dic)
h_bar.pyplot(h_fig)

st.subheader('🦅n-gram이 포함된 의사록 문장')
pos_11 = pos_dic.sort_values('Up', ascending=False).head(10)
p_options = pos_11['H_Key'].unique()
select_option = st.selectbox('값을 선택하세요:', p_options)

pos_sent = pos_sent.drop('Unnamed: 0',axis=1)
filtered_pdf = pos_sent[pos_sent['Hawkish'] == select_option]
st.dataframe(filtered_pdf)