import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="부산 주요 해수욕장 방문객 추이 대시보드",
    page_icon="🏖️",
    layout="wide"
)

st.title("🏖️ 부산 주요 해수욕장 연도별 방문객 수 변화 대시보드")
st.markdown("부산광역시 해수욕장 방문객 현황 CSV 파일을 업로드하면 연도별 추이를 분석해 드립니다.")

# 2. 파일 업로더 (초기 화면에는 이 버튼만 표시됨)
uploaded_file = st.file_uploader("📂 부산 해수욕장 CSV 파일을 업로드하세요 (2015~2025년)", type=["csv"])

# CSV 인코딩 자동 판별 읽기 함수 (UTF-8 및 CP949/EUC-KR 대응)
def load_csv_safely(file):
    for encoding in ["utf-8", "cp949", "euc-kr"]:
        try:
            file.seek(0)
            return pd.read_csv(file, encoding=encoding)
        except UnicodeDecodeError:
            continue
    return None

# 3. 파일이 업로드된 경우에만 아래 내용 실행
if uploaded_file is not None:
    df = load_csv_safely(uploaded_file)

    if df is None:
        st.error("❌ 파일 인코딩을 읽을 수 없습니다. UTF-8 또는 CP949 형식의 CSV 파일인지 확인해 주세요.")
        st.stop()

    # 열 이름 앞뒤 공백 제거 (공공데이터 오류 방지)
    df.columns = df.columns.str.strip()

    # 필수 열 존재 여부 확인
    required_cols = ["연도별", "해수욕장명", "방문자수(천명)"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"❌ CSV 파일에 필수 열이 누락되었습니다: {', '.join(missing_cols)}")
        st.info(f"현재 파일의 열 목록: {', '.join(df.columns)}")
        st.stop()

    # 데이터 전처리 (StreamlitAPIException 및 차트 렌더링 오류 원천 차단)
    clean_df = df.copy()

    # '연도별' 열에서 숫자(연도)만 추출하여 문자열로 변환 (X축 쉼표 표기 예: 2,020 방지)
    clean_df["연도별"] = (
        clean_df["연도별"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )
    clean_df = clean_df.dropna(subset=["연도별"])

    # '방문자수(천명)' 열의 쉼표(,) 제거 후 숫자형(float/int)으로 강제 변환
    clean_df["방문자수(천명)"] = (
        clean_df["방문자수(천명)"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    clean_df["방문자수(천명)"] = pd.to_numeric(clean_df["방문자수(천명)"], errors="coerce").fillna(0)

    # '해수욕장명' 공백 제거
    clean_df["해수욕장명"] = clean_df["해수욕장명"].astype(str).str.strip()

    # --- 화면 출력 1: 업로드한 데이터 표 ---
    st.divider()
    st.subheader("1. 📋 업로드한 원본 데이터 표")
    st.dataframe(df, use_container_width=True)

    # 피벗 테이블 생성 (X축: 연도별, 범례/열: 해수욕장명, 값: 방문자수(천명))
    pivot_df = clean_df.pivot_table(
        index="연도별",
        columns="해수욕장명",
        values="방문자수(천명)",
        aggfunc="sum"
    ).sort_index()

    # --- 화면 출력 2: 분석 요약 내용 ---
    st.divider()
    st.subheader("2. 📊 데이터 분석 요약")

    years = sorted(clean_df["연도별"].unique())
    start_year, end_year = years[0], years[-1]
    total_visitors = clean_df["방문자수(천명)"].sum()

    # 최다 방문 해수욕장 및 최다 방문 연도 계산
    beach_totals = clean_df.groupby("해수욕장명")["방문자수(천명)"].sum()
    top_beach = beach_totals.idxmax()
    top_beach_val = beach_totals.max()

    year_totals = clean_df.groupby("연도별")["방문자수(천명)"].sum()
    top_year = year_totals.idxmax()
    top_year_val = year_totals.max()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("분석 기간", f"{start_year}년 ~ {end_year}년")
    col2.metric("누적 총 방문객 수", f"{total_visitors:,.0f} 천명")
    col3.metric("최다 방문 해수욕장", f"{top_beach}", f"{top_beach_val:,.0f} 천명")
    col4.metric("최다 방문 연도", f"{top_year}년", f"{top_year_val:,.0f} 천명")

    st.info(
        f"💡 **요약 코멘트:** **{start_year}년부터 {end_year}년까지** 부산 주요 해수욕장({len(beach_totals)}곳)의 "
        f"누적 방문객은 총 **{total_visitors:,.0f}천 명**입니다. "
        f"전체 기간 중 가장 많은 인파가 몰린 곳은 **{top_beach}**({top_beach_val:,.0f}천 명)이며, "
        f"방문객이 가장 많았던 해는 **{top_year}년**({top_year_val:,.0f}천 명)입니다."
    )

    # --- 화면 출력 3: 연도별 해수욕장별 방문객 수 추이 라인 차트 ---
    st.divider()
    st.subheader("3. 📈 연도별·해수욕장별 방문객 수 추이 (단위: 천명)")

    # 해수욕장 선택 필터 (원하는 곳만 골라볼 수 있도록 기본 전체 선택 제공)
    selected_beaches = st.multiselect(
        "차트에 표시할 해수욕장을 선택하세요:",
        options=list(pivot_df.columns),
        default=list(pivot_df.columns)
    )

    if selected_beaches:
        st.line_chart(pivot_df[selected_beaches], use_container_width=True)
    else:
        st.warning("최소 1개 이상의 해수욕장을 선택해 주세요.")
    st.info("👆 위 상자를 눌러 분석할 CSV 파일을 먼저 선택해 주세요.")
