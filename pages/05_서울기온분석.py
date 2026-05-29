import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="서울 기온 분석 앱", layout="centered")
st.title("🌡️ 서울 연도별 기온 분석 및 미래 예측")
st.write("1907년부터 2018년까지의 데이터를 바탕으로 특정 날짜의 기온 추이를 확인하고 미래 기온을 예측합니다.")

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
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

# 3. 사이드바 - 사용자 날짜 및 예측 연도 선택
st.sidebar.header("🗓️ 날짜 및 예측 설정")
selected_month = st.sidebar.selectbox("월을 선택하세요", list(range(1, 13)), index=7)

# 월별 말일 예외 처리
if selected_month in [4, 6, 9, 11]:
    max_day = 30
elif selected_month == 2:
    max_day = 29
else:
    max_day = 31

selected_day = st.sidebar.selectbox("일을 선택하세요", list(range(1, max_day + 1)), index=14)

# 미래 예측 연도 선택 (기존 데이터 이후인 2019년부터 2100년까지 선택 가능)
predict_year = st.sidebar.slider("예측할 미래 연도를 선택하세요", min_value=2019, max_value=2100, value=2030)

# 4. 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

# 5. 시각화 및 정보 출력
if not filtered_df.empty:
    st.subheader(f"📊 {selected_month}월 {selected_day}일의 기온 변화 및 예측 그래프")
    st.caption("💡 그래프 위에 마우스를 올리면 해당 연도의 정확한 기온이 표시됩니다.")
    
    # --- 머신러닝 기반 미래 기온 예측 로직 (선형 회귀) ---
    X = filtered_df[['연도']].values 
    y_max = filtered_df['최고기온(℃)'].values 
    y_min = filtered_df['최저기온(℃)'].values 
    
    # 최고기온 예측 모델 학습
    model_max = LinearRegression()
    model_max.fit(X, y_max)
    pred_max_temp = model_max.predict([[predict_year]])[0]
    
    # 최저기온 예측 모델 학습
    model_min = LinearRegression()
    model_min.fit(X, y_min)
    pred_min_temp = model_min.predict([[predict_year]])[0]
    
    # --- Plotly 대화형 그래프 생성 ---
    fig = go.Figure()
    
    # 과거 최고기온 선그래프
    fig.add_trace(go.Scatter(
        x=filtered_df['연도'], y=filtered_df['최고기온(℃)'],
        mode='lines+markers', name='과거 최고기온',
        line=dict(color='#FF69B4', width=2),
        marker=dict(size=4),
        hovertemplate='<b>%{x}년 최고기온</b><br>온도: %{y}°C<extra></extra>'
    ))
    
    # 과거 최저기온 선그래프
    fig.add_trace(go.Scatter(
        x=filtered_df['연도'], y=filtered_df['최저기온(℃)'],
        mode='lines+markers', name='과거 최저기온',
        line=dict(color='#ADD8E6', width=2),
        marker=dict(size=4),
        hovertemplate='<b>%{x}년 최저기온</b><br>온도: %{y}°C<extra></extra>'
    ))
    
    # 미래 예측 최고기온 다이아몬드 점
    fig.add_trace(go.Scatter(
        x=[predict_year], y=[pred_max_temp],
        mode='markers', name='예측 최고기온',
        marker=dict(color='#FF0000', size=10, symbol='diamond'),
        hovertemplate=f'<b>{predict_year}년 최고 예측</b><br>온도: %{{y}}:.2f°C<extra></extra>'
    ))
    
    # 미래 예측 최저기온 다이아몬드 점
    fig.add_trace(go.Scatter(
        x=[predict_year], y=[pred_min_temp],
        mode='markers', name='예측 최저기온',
        marker=dict(color='#0000FF', size=10, symbol='diamond'),
        hovertemplate=f'<b>{predict_year}년 최저 예측</b><br>온도: %{{y}}:.2f°C<extra></extra>'
    ))
    
    # 레이아웃 스타일 가다듬기
    fig.update_layout(
        title=dict(text=f"{selected_month}월 {selected_day}일 기온 추이 및 예측 ({predict_year}년)", font=dict(size=16)),
        xaxis_title="연도",
        yaxis_title="온도 (℃)",
        hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40),
        plot_bgcolor='rgba(255,255,255,0.9)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # --- 정보 출력 섹션 ---
    st.write(f"🔮 **{predict_year}년 {selected_month}월 {selected_day}일** 기온 예측 결과:")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.metric(label=f"{predict_year}년 예상 최고 기온", value=f"{pred_max_temp:.2f} ℃")
    with p_col2:
        st.metric(label=f"{predict_year}년 예상 최저 기온", value=f"{pred_min_temp:.2f} ℃")
        
    st.markdown("---")
    
    st.write(f"ℹ️ **{selected_month}월 {selected_day}일**의 역사적 기록 (1907~2018):")
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
    st.warning(f"선택한 {selected_month}월 {selected_day}일에 해당하는 데이터가 없습니다.")
