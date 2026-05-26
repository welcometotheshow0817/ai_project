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
    # 데이터 불러오기
    df = pd.read_csv("seoul.csv")
    
    # 열 이름 공백 제거 및 날짜 열의 '\t' 문자 정제
    df.columns = df.columns.str.strip()
    df['날짜'] = df['날짜'].astype(str).str.replace('\t', '').str.strip()
    
    # 날짜 데이터 타입을 datetime으로 변환 (에러 발생 시 내버려둠)
    df['날짜_dt'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거 (날짜 변환 실패 및 기온 데이터 누락 행 제거)
    df = df.dropna(subset=['날짜_dt', '최고기온(℃)', '최저기온(℃)'])
    
    # 월(Month)과 일(Day), 연도(Year) 추출
    df['연도'] = df['날짜_dt'].dt.year
    df['월'] = df['날짜_dt'].dt.month
    df['일'] = df['날짜_dt'].dt.day
    
    return df

# 데이터 로딩 애니메이션 효과
with st.spinner("데이터를 불러오는 중입니다..."):
    df = load_data()

# 3. 사이드바 - 사용자 입력 인터페이스
st.sidebar.header("🗓️ 날짜 선택")
selected_month = st.sidebar.selectbox("월을 선택하세요", list(range(1, 13)), index=7) # 기본값 8월

# 선택한 월에 따른 일수 제한 (간단하게 처리)
if selected_month in [4, 6, 9, 11]:
    max_day = 30
elif selected_month == 2:
    max_day = 29
else:
    max_day = 31

selected_day = st.sidebar.selectbox("일을 선택하세요", list(range(1, max_day + 1)), index=14) # 기본값 15일

# 4. 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

# 5. 메인 화면 시각화 및 정보 제공
if not filtered_df.empty:
    st.subheader(f"📊 {selected_month}월 {selected_day}일의 기온 변화 그래프")
    
    # 스트림릿 클라우드(리눅스 환경) 한글 깨짐 방지를 위한 폰트 설정
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 최고기온 (핫핑크: #FF69B4)
    ax.plot(filtered_df['연도'], filtered_df['최고기온(℃)'], 
            color='#FF69B4', marker='o', markersize=4, linestyle='-', label='최고기온')
    
    # 최저기온 (연한 파란색: #ADD8E6)
    ax.plot(filtered_df['연도'], filtered_df['최저기온(℃)'], 
            color='#ADD8E6', marker='o', markersize=4, linestyle='-', label='최저기온')
    
    # 그래프 속성 설정
    ax.set_title("날짜별 기온분석", fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel("연도", fontsize=12)
    ax.set_ylabel("온도 (℃)", fontsize=12)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 스트림릿에 그래프 출력
    st.pyplot(fig)
    
    # 요약 정보 제공 테이블
    st.write(f"ℹ️ **{selected_month}월 {selected_day}일**의 역사적 기록:")
    col1, col2 = st.columns(2)
    
    max_temp_row = filtered_df.loc[filtered_df['최고기온(℃)'].idxmax()]
    min_temp_row = filtered_df.loc[filtered_df['최저기온(℃)'].idxmin()]
    
    with col1:
        st.metric(label="역대 최고 기온", 
                  value=f"{max_temp_row['최고기온(℃)']} ℃", 
                  delta=f"{int(max_temp_row['연도'])}년")
    with col2:
        st.metric(label="역대 최저 기온", 
                  value=f"{min_temp_row['최저기온(℃)']} ℃", 
                  delta=f"{int(min_temp_row['연도'])}년", 
                  delta_color="inverse")
else:
    st.warning("선택한 날짜에 해당하는 데이터가 존재하지 않습니다.")
