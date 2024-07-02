import streamlit as st
import pandas as pd


# 사이드 바에 극성이 뚜렷한 문장 셀렉트할 수 있게
sent_dic = pd.read_csv("hw_do/data/min_sent_fin.csv")
# 셀렉트한 문장이 챗봇에 입력되게
# 입력된 문장이 어떤 ngram들이 나오고 극성 점수가 몇인지

neg_dic = pd.read_csv("hw_do/data/total_dov_dic.csv")
pos_dic = pd.read_csv("hw_do/data/total_haw_dic.csv")
pos_dic = pos_dic.rename(columns={'Unnamed: 0': 'H_Key'})
neg_dic = neg_dic.rename(columns={'Unnamed: 0': 'D_Key'})


sent_dic = pd.read_csv("hw_do/data/min_sent_fin.csv")
sent = pd.read_csv("hw_do/data/sent_tone.csv")
sent_dic['sentence'] = sent['sentence']



with st.sidebar:
    sent_options = sent_dic['sentence'].unique()
    sentence = st.selectbox('문장을 선택하세요:', sent_options)


st.subheader('의사록 문장 톤분석 챗봇')


def judge_tone(sentence):
    
        rows = sent_dic[sent_dic['sentence'] == sentence].index
        if len(rows) > 0: 
            for row in rows:
                i = row
            
            tone = sent_dic['sent_tone'][i]
            dohw = sent_dic['sentiment'][i]
            word = sent_dic[dohw][i]
            
            return tone, dohw, word
        
        else:
            return None, None, None


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.charts = []
        
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

for chart in st.session_state.charts:
    st.plotly_chart(chart)



# 챗봇에 문장 입력
st.chat_message('user').write(sentence)
# judge_tone 함수의 결과 출력
tone, dohw, word = judge_tone(sentence)

st.chat_message('assistant').markdown(f"선택하신 문장의 톤은 **{tone}**이며, 극성은 **{dohw}**, 해당하는 단어로는 **{word}**가 있습니다.")

#write(f"선택하신 문장의 톤은 {tone}이며, 극성은 {dohw}, 해당하는 단어로는 {word}가 있습니다.")
st.session_state.messages.append({"role": "user", "content": sentence})
st.session_state.messages.append({"role": "assistant", "content": f"선택하신 문장의 톤은 **{tone}**이며, 극성은 **{dohw}**, 해당하는 단어로는 **{word}**가 있습니다."})



import plotly.graph_objects as go

def create_gauge_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [-1, 1]}}
    ))
    return fig

# Streamlit에서 표시
import streamlit as st
fig = create_gauge_chart(tone, "Sent_TONE")
st.plotly_chart(fig)

# Save the chart to the session state
st.session_state.charts.append(fig)