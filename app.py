import streamlit as st
import pandas as pd

st.set_page_config(page_title="부산 해수욕장 방문객", page_icon="🌊", layout="wide")

st.title("🌊 부산 주요 해수욕장 연도별 방문객 수 변화")
st.write("CSV 파일을 업로드하면 해수욕장별 방문객 수 표와 추이 그래프를 분석해 줍니다.")

uploaded_file = st.file_uploader("방문객 데이터 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding="cp949")

    df.columns = df.columns.str.strip()

    if {'연도별', '해수욕장명', '방문자수(천명)'}.issubset(df.columns):
        df['해수욕장명'] = df['해수욕장명'].str.strip()
        chart_df = df.pivot(index='연도별', columns='해수욕장명', values='방문자수(천명)')
    else:
        chart_df = df.set_index(df.columns[0])

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 업로드된 방문객 수 데이터")
        st.dataframe(df, use_container_width=True)

    with col2:
        st.subheader("📌 분석 요약")
        st.write(f"- 총 **{len(chart_df)}개** 연도(2015~2025)의 데이터가 로드되었습니다.")
        st.write(f"- 분석 대상 해수욕장: **{', '.join(chart_df.columns)}**")

    st.subheader("📈 연도별 방문객 수 추이 그래프 (단위: 천 명)")
    st.line_chart(chart_df)
else:
    st.info("👆 위 상자를 눌러 분석할 CSV 파일을 먼저 선택해 주세요.")
