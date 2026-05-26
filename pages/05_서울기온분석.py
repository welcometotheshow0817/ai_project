import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="서울 기온 분석 앱", layout="centered")
st.title("🌡️ 서울 연도별 특정 날짜 기온 분석")
st.write("1907년부터 2018년까지의 데이터를 바탕으로 선택한 날짜의 기온 변화 추이를 확인합니다.")

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 파일 인코딩(cp949) 명시하여 UnicodeDecodeError 방지
    df = pd.read_csv("seoul.csv", encoding="cp949")
    
    # 열 이름의 양끝 공백 및 보이지 않는 문자 제거 ('날짜', '지점', '평균기온(℃)' 등)
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터의 앞뒤 공백 및 탭 문자(\t), 따옴표 제거 후 문자열로 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t"\']', '', regex=True).str.strip()
    
    # 날짜 데이터 타입을 datetime 객체로 변환 (변환 안 되는 행은 NaT 처리)
    df['날짜_dt'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 필수 데이터(날짜, 최고기온, 최저기온)에 결측치가 있는 행 제거
    df = df.dropna(subset=['날짜_dt', '최고기온(℃)', '최저기온(℃)'])
    
    # 날짜에서 연도, 월, 일 정수형 데이터로 추출
    df['연도'] = df['날짜_dt'].dt.year
    df['월'] = df['날짜_dt'].dt.month
    df['일'] = df['날짜_dt'].dt.day
    
    return df

# 데이터 불러오기 수행
with st.spinner("데이터를 불러오는 중입니다..."):
    df = load_data()

# 3. 사이드바 - 사용자 날짜 입력 인터페이스
st.sidebar.header("🗓️ 날짜 선택")
selected_month = st.sidebar.selectbox("월을 선택하세요", list(range(1, 13)), index=7)  # 기본값 8월

# 선택한 월에 맞게 선택 가능한 일수 제한
if selected_month in [4, 6, 9, 11]:
    max_day = 30
elif selected_month == 2:
    max_day = 29
else:
    max_day = 31

selected_day = st.sidebar.selectbox("일을 선택하세요", list(range(1, max_day + 1)), index=14)  # 기본값 15일

# 4. 사용자가 선택한 월/일에 맞춰 데이터 필터링 후 연도순 정렬
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

# 5. 메인 화면 시각화 및 정보 표시
if not filtered_df.empty:
    st.subheader(f"📊 {selected_month}월 {selected_day}
