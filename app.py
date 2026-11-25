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

    df = df.set_index(df.columns[0])

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 업로드된 방문객 수 데이터")
        st.dataframe(df, use_container_width=True)

    with col2:
        st.subheader("📌 분석 요약")
        st.write(f"- 총 **{len(df)}개** 기간의 데이터가 로드되었습니다.")
        st.write(f"- 분석 대상 항목: **{', '.join(df.columns)}**")

    st.subheader("📈 연도별 방문객 수 추이 그래프")
    st.line_chart(df)
else:
    st.info("👆 위 상자를 눌러 분석할 CSV 파일을 먼저 선택해 주세요.")
