import streamlit as st
import pandas as pd

st.set_page_config(page_title="부산 해수욕장 방문객", page_icon="🌊", layout="wide")

st.title("🌊 부산 주요 해수욕장 연도별 방문객 수 변화")
st.write("해운대, 광안리, 송정 등 부산 주요 해수욕장의 최근 5년간 방문객 수 추이를 분석한 대시보드입니다.")

data = {
    '연도': ['2019', '2020', '2021', '2022', '2023'],
    '해운대': [1100, 750, 850, 950, 1050],
    '광안리': [850, 600, 700, 800, 900],
    '송정': [400, 300, 350, 420, 480],
    '다대포': [350, 250, 300, 350, 400],
    '송도': [300, 200, 250, 280, 320]
}

df = pd.DataFrame(data).set_index('연도')

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 방문객 수 데이터 (단위: 만 명)")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📌 분석 요약")
    st.write("- 2020년 팬데믹 영향으로 방문객이 크게 감소했습니다.")
    st.write("- 2021년 이후 지속적인 회복세를 보이고 있습니다.")
    st.write("- 해운대와 광안리가 여전히 가장 높은 방문객 비중을 차지합니다.")

st.subheader("📈 연도별 방문객 수 추이 그래프")
st.line_chart(df)

st.caption("※ 본 웹사이트의 데이터는 차트 시각화 예시를 위해 임의로 생성된 가상 데이터입니다.")