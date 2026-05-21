import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 기본 설정
st.set_page_config(page_title="글로벌 MBTI 데이터 대시보드", layout="centered")

st.title("🌏 글로벌 MBTI 데이터 대시보드")
st.markdown("공개된 csv 데이터를 바탕으로 국가별, MBTI 유형별 비율을 다각도로 분석합니다.")

# 2. 데이터 불러오기 함수
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()
    
    # 3. 스트림릿 탭(Tab)을 이용해 두 가지 기능 분리
    tab1, tab2 = st.tabs(["📊 국가별 MBTI 비율", "🧩 MBTI별 상위 10개국"])

    # ----------------------------------------------------
    # [탭 1] 국가별 MBTI 비율 분석 (처음에 만든 기능)
    # ----------------------------------------------------
    with tab1:
        st.subheader("국가별 MBTI 분포 분석")
        st.write("국가를 선택하면 해당 국가의 16가지 MBTI 유형 비율을 확인합니다.")
        
        country_list = df["Country"].unique()
        selected_country = st.selectbox("분석할 국가를 선택하세요:", country_list, key="tab1_country")

        # 선택한 국가의 데이터 추출 및 정렬
        country_data = df[df["Country"] == selected_country].iloc[0, 1:]
        country_df = pd.DataFrame({
            "MBTI": country_data.index,
            "Percentage": country_data.values * 100
        }).sort_values(by="Percentage", ascending=False).reset_index(drop=True)

        # 1등은 빨강, 나머지는 비율별 파란색 그라데이션 색상 정의
        colors_t1 = []
        max_val_t1 = country_df["Percentage"].max()
        min_val_t1 = country_df["Percentage"].min()

        for idx, row in country_df.iterrows():
            if idx == 0:
                colors_t1.append("rgb(230, 57, 70)")
            else:
                norm = (row["Percentage"] - min_val_t1) / (max_val_t1 - min_val_t1) if max_val_t1 != min_val_t1 else 1
                r = int(29 + (168 - 29) * (1 - norm))
                g = int(53 + (218 - 53) * (1 - norm))
                b = int(87 + (220 - 87) * (1 - norm))
                colors_t1.append(f"rgb({r}, {g}, {b})")

        # Plotly 그래프 생성
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=country_df["MBTI"],
            y=country_df["Percentage"],
            marker_color=colors_t1,
            text=country_df["Percentage"].round(2).astype(str) + "%",
            textposition='auto',
            hovertemplate="<b>%{x}</b>: %{y:.2f}%<extra></extra>"
        ))

        fig1.update_layout(
            title=f"📊 {selected_country}의 MBTI 유형별 비율 (1위 강조)",
            xaxis_title="MBTI 유형",
            yaxis_title="비율 (%)",
            template="plotly_white",
            margin=dict(l=20, r=20, t=60, b=20),
            height=500
        )
        st.plotly_chart(fig1, use_container_width=True, key="fig1_chart")

        # 요약 문구
        top_mbti_t1 = country_df.iloc[0]["MBTI"]
        top_pct_t1 = country_df.iloc[0]["Percentage"]
        st.info(f"💡 **{selected_country}**에서 가장 많은 MBTI 유형은 **{top_mbti_t1}**이며, 전체의 **{top_pct_t1:.2f}%**를 차지합니다.")


    # ----------------------------------------------------
    # [탭 2] MBTI별 상위 10개국 분석 (새로 추가한 기능)
    # ----------------------------------------------------
    with tab2:
        st.subheader("MBTI 기준 비율 상위 10개국")
        st.write("MBTI 유형을 선택하면 전 세계에서 해당 비율이 가장 높은 10개국을 확인합니다.")
        
        mbti_list = df.columns[1:].tolist()
        selected_mbti = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_list, key="tab2_mbti")

        # 선택한 MBTI 기준 상위 10개국 추출
        top10_df = pd.DataFrame({
            "Country": df["Country"],
            "Percentage": df[selected_mbti] * 100
        }).sort_values(by="Percentage", ascending=False).head(10).reset_index(drop=True)

        # 1등 국가는 빨강, 2~10등은 파란색 그라데이션
        colors_t2 = []
        max_val_t2 = top10_df["Percentage"].max()
        min_val_t2 = top10_df["Percentage"].min()

        for idx, row in top10_df.iterrows():
            if idx == 0:
                colors_t2.append("rgb(230, 57, 70)")
            else:
                norm = (row["Percentage"] - min_val_t2) / (max_val_t2 - min_val_t2) if max_val_t2 != min_val_t2 else 1
                r = int(29 + (168 - 29) * (1 - norm))
                g = int(53 + (218 - 53) * (1 - norm))
                b = int(87 + (220 - 87) * (1 - norm))
                colors_t2.append(f"rgb({r}, {g}, {b})")

        # Plotly 그래프 생성
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=top10_df["Country"],
            y=top10_df["Percentage"],
            marker_color=colors_t2,
            text=top10_df["Percentage"].round(2).astype(str) + "%",
            textposition='auto',
            hovertemplate="<b>%{x}</b>: %{y:.2f}%<extra></extra>"
        ))

        fig2.update_layout(
            title=f"📊 {selected_mbti} 비율이 가장 높은 국가 Top 10",
            xaxis_title="국가 (Country)",
            yaxis_title="비율 (%)",
            template="plotly_white",
            margin=dict(l=20, r=20, t=60, b=40),
            height=500
        )
        st.plotly_chart(fig2, use_container_width=True, key="fig2_chart")

        # 요약 문구
        top_country_t2 = top10_df.iloc[0]["Country"]
        top_pct_t2 = top10_df.iloc[0]["Percentage"]
        st.success(f"👑 전 세계에서 **{selected_mbti}** 비율이 가장 높은 나라는 **{top_country_t2}**이며, 무려 **{top_pct_t2:.2f}%**에 달합니다!")

except FileNotFoundError:
    st.error("⚠️ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 파일명을 확인하고 대시보드 파일과 같은 경로에 배치해 주세요.")
