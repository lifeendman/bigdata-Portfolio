import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] =  'Malgun Gothic'
import plotly.express as px

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

st.header("서울시 공공자전거 이용정보 분석")
bic = pd.read_csv("bic.csv", encoding="cp949")
bic['성별'] = bic['성별'].str.upper()



st.sidebar.image("서울시.jpg")
selected = st.sidebar.selectbox("메뉴 선택", 
                     ["메인", "대여소별 데이터 보기", "대여소별 이용건수 TOP10", "이용시간이 긴 대여소", "데이터 선택 및 통계"]) 


def main():

    st.subheader("메인페이지")

    st.image("따릉이.png")

    st.info('이번 프로젝트는 서울시 공공자전거 **따릉이** 이용 데이터를 분석하는 빅데이터 실습입니다.')
    st.dataframe(bic)
    st.info("데이터 양이 많기 때문에 일부만 표시됩니다.")
    st.success("지금부터 서울시 공공자전거 데이터를 하나씩 분석해보겠습니다!")

def data():

    st.subheader("대여소별 데이터 보기")
    selected_company = st.selectbox("확인할 대여소를 선택하세요.",
                                    bic['대여소명'].unique().tolist() )    
    result3 = bic.query("대여소명 == @selected_company ")
    st.dataframe(result3)
    st.info("선택한 대여소의 상세 이용 데이터를 확인할 수 있습니다.")

def rental():
    st.subheader("대여소별 이용건수 TOP10")
    st.dataframe(bic)
    st.text("서울시에서 이용건수가 많은 대여소 상위 10곳을 확인해보겠습니다.")

    result1 = bic.groupby("대여소명", as_index=False)\
                .agg(이용건수 = ('이용건수', 'sum'))\
                .sort_values("이용건수", ascending=False)\
                .head(10)
    st.dataframe(result1)

    b1 = px.bar(data_frame= result1, 
                x='대여소명', 
                y = "이용건수")
    st.plotly_chart(b1)

    st.info('분석 결과, **마곡나루역 2번 출구**가 가장 많이 이용된 대여소로 나타났습니다.')

def time():
    st.subheader("이용시간이 긴 대여소")
    st.dataframe(bic)
    st.text("대여소별 총 이용시간을 기준으로 가장 오래 이용된 상위 10곳을 살펴봅니다.")

    result1 = bic.groupby("대여소명", as_index=False)\
                .agg(분당이용시간 = ('이용시간(분)', 'sum'))\
                .sort_values("분당이용시간", ascending=False)\
                .head(10)
    st.dataframe(result1)

    b1 = px.bar(data_frame= result1, 
                x='대여소명', 
                y = "분당이용시간")
    st.plotly_chart(b1)

    st.info('한강공원 인근 대여소에서 이용시간이 특히 긴 것으로 나타났습니다.')

def show_menu2():
    st.subheader("데이터 선택 및 통계")

    input1 = st.selectbox("그룹 기준 선택", 
                          ["대여소명","연령대코드","성별"])
    input2 = st.selectbox("분석할 항목 선택",["이용건수","이동거리(M)","이용시간(분)"])
    input3 = st.selectbox("통계 방법 선택", ['sum','mean','max','min','count'])
    
    result4 = bic.groupby(input1, as_index=False)\
                .agg(value = (input2, input3))\
                .sort_values("value", ascending=False)\
                .head(10)
    st.dataframe(result4)

    b2=px.bar(data_frame=result4, x=input1, y ='value' )
    st.plotly_chart(b2)

    st.info(f"선택한 기준({input1})별로 {input2}의 {input3} 값을 계산한 결과입니다.")


if selected == "메인":
    main()
elif selected == "대여소별 데이터 보기":
    data()
elif selected =="대여소별 이용건수 TOP10":
    rental()
elif selected == "이용시간이 긴 대여소":
    time()
elif selected == "데이터 선택 및 통계":
    show_menu2()
else:
    st.error("Error")
