import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 페이지 설정 및 제목 (이 설정이 브라우저 탭 및 상단에 한글로 표시되게 합니다)
st.set_page_config(page_title="서울 기온 분석 앱", layout="centered")
st.title("🌡️ 서울 연도별 특정 날짜 기온 분석")
st.write("1907년부터 2018년까지의 데이터를 바탕으로 선택한 날짜의 기온 변화 추이를 확인합니다.")

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 인코딩 설정 추가하여 파일 읽기
    df = pd.read_csv("seoul.csv", encoding="cp949")
    
    # 열 이름 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 정제
    df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t"\']', '', regex=True).str.strip()
    df['날짜_dt'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거
    df = df.dropna(subset=['날짜_dt', '최고기온(℃)', '최저기온(℃)'])
    
    # 연도, 월, 일 추출
    df['연도'] = df['날짜_dt'].dt.year
    df['월'] = df['날짜_dt'].dt.month
    df['일'] = df['날짜_dt'].dt.day
    
    return df

# 데이터 로드
with st.spinner("데이터를 불러오는 중입니다..."):
    df = load_data()

# 3. 사이드바 - 사용자 날짜 선택
st.sidebar.header("🗓️ 날짜 선택")
selected_month = st.sidebar.selectbox("월을 선택하세요", list(range(1, 13)), index=7)

if selected_month in [4, 6, 9, 11]:
    max_day = 30
elif selected_month == 2:
    max_day = 29
else:
    max_day = 31

selected_day = st.sidebar.selectbox("일을 선택하세요", list(range(1, max_day + 1)), index=14)

# 4. 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

# 5. 시각화 및 정보 출력
if not filtered_df.empty:
    st.subheader(f"📊 {selected_month}월 {selected_day}일의 기온 변화 그래프")
    
    # 리눅스 서버용 기본 폰트 설정 및 마이너스 깨짐 방지
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 최고기온 (핫핑크)
    ax.plot(filtered_df['연度' if '연度' in filtered_df.columns else '연도'], filtered_df['최고기온(℃)'], 
            color='#FF69B4', marker='o', markersize=3, linestyle='-', label='최고기온')
    
    # 최저기온 (연한 파란색)
    ax.plot(filtered_df['연度' if '연度' in filtered_df.columns else '연도'], filtered_df['최저기온(℃)'], 
            color='#ADD8E6', marker='o', markersize=3, linestyle='-', label='최저기온')
    
    # 그래프 스타일 설정
    ax.set_title("날짜별 기온분석", fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel("연도", fontsize=12)
    ax.set_ylabel("온도 (℃)", fontsize=12)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    st.pyplot(fig)
    
    # 카드형 미니 통계 정보
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
    st.warning("선택한
