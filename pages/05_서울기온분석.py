import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="서울 기온 분석 앱", layout="centered")
st.title("🌡️ 서울 연도별 특정 날짜 기온 분석")
st.write("1907년부터 2018년까지의 데이터를 바탕으로 선택한 날짜의 기온 변화 추이를 확인합니다.")

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # [수정] UnicodeDecodeError 방지를 위해 encoding="cp949" 추가
    df = pd.read_csv("seoul.csv", encoding="cp949")
    
    # 열 이름의 양끝 공백 제거 (예: ' 날짜 ' -> '날짜')
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 양끝 공백 및 따옴표, 탭 문자(\t) 완벽히 제거
    df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t"\']', '', regex=True).str.strip()
    
    # 날짜 데이터 타입을 datetime으로 변환 (에러 발생 행은 NaT 처리)
    df['날짜_dt'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거 (날짜 변환 실패 및 기온 데이터 누락 행 제거)
    df = df.dropna(subset=['날짜_dt', '최고기온(℃)', '최저기온(℃)'])
    
    # 연도, 월, 일 추출
    df['연도'] = df['날짜_dt'].dt.year
    df['월'] = df['날짜_dt'].dt.month
    df['일'] = df['날짜_dt'].dt.day
    
    return df

# 데이터 로딩 애니메이션 효과
with st.spinner("데이터를 불러오는 중입니다..."):
    try:
        df = load_data()
    except UnicodeDecodeError:
        # cp949로도 안 될 경우를 대비한 예외 처리 예비용 (euc-kr 사용)
        df = pd.read_csv("seoul.csv", encoding="euc-kr")
        df.columns = df.columns.str.strip()
        df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t"\']', '', regex=True
