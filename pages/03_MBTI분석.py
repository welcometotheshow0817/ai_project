import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 기본 설정
st.set_page_config(page_title="국가별 MBTI 분포 분석", layout="centered")

st.title("🌏 국가별 MBTI 비율 분석기")
st.markdown("공개된 csv 데이터를 바탕으로 국가별 MBTI 16가지 유형의 비율을 시각화합니다.")

# 2. 데이터 불러오기
@st.cache_data
def load_data():
    # 데이터셋 로드 (전체 경로 대신 파일명만 지정하여 클라우드 환경 대응)
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()

    # 3. 사이드바 또는 메인 화면에서 국가 선택
    country_list = df["Country"].unique()
    selected_country = st.selectbox("분석할 국가를 선택하세요:", country_list)

    # 4. 선택한 국가의 데이터 추출 및 정렬
    country_data = df[df["Country"] == selected_country].iloc[0, 1:]
    
    # 비율을 백분율(%)로 변환하고 내림차순 정렬
    country_df = pd.DataFrame({
        "MBTI": country_data.index,
        "Percentage": country_data.values * 100
    }).sort_values(by="Percentage", ascending=False).reset_index(drop=True)

    # 5. 조건별 색상 스케일 정의 (1등은 빨강, 나머지는 파란색 그라데이션)
    # 데이터가 이미 내림차순 정렬되어 있으므로 index 0이 무조건 1등입니다.
    colors = []
    max_val = country_df["Percentage"].max()
    min_val = country_df["Percentage"].min()

    for idx, row in country_df.iterrows():
        if idx == 0:
            # 1등은 확실한 빨간색
            colors.append("rgb(230, 57, 70)")
        else:
            # 나머지는 비율에 따라 진한 파란색 -> 연한 파란색 그라데이션 계산
            # 수치가 높을수록 진한 파랑, 낮을수록 연한 파랑
            norm = (row["Percentage"] - min_val) / (max_val - min_val) if max_val != min_val else 1
            # RGB 값 보간 (진한 파랑: rgb(29, 53, 87) ~ 연한 파랑: rgb(168, 218, 220))
            r = int(29 + (168 - 29) * (1 - norm))
            g = int(53 + (218 - 53) * (1 - norm))
            b = int(87 + (220 - 87) * (1 - norm))
            colors.append(f"rgb({r}, {g}, {b})")

    # 6. Plotly 인터랙티브 그래프 생성
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=country_df["MBTI"],
        y=country_df["Percentage"],
        marker_color=colors,
        text=country_df["Percentage"].round(2).astype(str) + "%",
        textposition='auto',
        hovertemplate="<b>%{x}</b>: %{y:.2f}%<extra></extra>"
    ))

    # 그래프 레이아웃 깔끔하게 조정
    fig.update_layout(
        title=f"📊 {selected_country}의 MBTI 유형별 비율 (1위 강조)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (%)",
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        height=500
    )

    # 스트림릿에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 7. 간단한 요약 정보 제공
    top_mbti = country_df.iloc[0]["MBTI"]
    top_pct = country_df.iloc[0]["Percentage"]
    st.info(f"💡 **{selected_country}**에서 가장 많은 MBTI 유형은 **{top_mbti}**이며, 전체의 **{top_pct:.2f}%**를 차지합니다.")

except FileNotFoundError:
    st.error("⚠️ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 대시보드 파일과 같은 경로에 배치해 주세요.")
