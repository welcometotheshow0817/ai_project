import streamlit as np
import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 인기 관광지 TOP 10",
    page_icon="🗼",
    layout="wide"
)

st.title("외국인이 좋아하는 서울 주요 관광지 TOP 10")
st.markdown("스트림릿과 폴리움을 활용하여 서울의 명소를 소개합니다.")

# 2. 데이터 정의 (명소 이름, 위도, 경도, 설명)
tourist_spots = [
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770, "desc": "한국의 전통미를 느낄 수 있는 대표 고궁"},
    {"name": "N서울타워", "lat": 37.5512, "lon": 126.9882, "desc": "서울 시내를 한눈에 내려다보는 전망대"},
    {"name": "명동 쇼핑거리", "lat": 37.5634, "lon": 126.9846, "desc": "쇼핑과 길거리 음식의 천국"},
    {"name": "북촌한옥마을", "lat": 37.5829, "lon": 126.9835, "desc": "실제 주민들이 거주하는 전통 한옥 밀집 지역"},
    {"name": "인사동", "lat": 37.5744, "lon": 126.9874, "desc": "한국 전통 기념품과 찻집이 가득한 곳"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.5668, "lon": 127.0094, "desc": "독특한 야경과 디자인 전시가 열리는 곳"},
    {"name": "홍대거리", "lat": 37.5567, "lon": 126.9236, "desc": "젊음과 버스킹, 트렌디한 카페의 중심지"},
    {"name": "롯데월드타워 & 몰", "lat": 37.5126, "lon": 127.1025, "desc": "세계에서 5번째로 높은 빌딩과 테마파크"},
    {"name": "이태원 관광특구", "lat": 37.5345, "lon": 126.9942, "desc": "다양한 문화와 이국적인 맛집이 모인 곳"},
    {"name": "광장시장", "lat": 37.5701, "lon": 126.9996, "desc": "녹두빈대떡, 육회 등 K-푸드를 체험하는 전통시장"}
]

# 3. 화면 레이아웃 분할 (좌측: 지도, 우측: 상세 정보)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ 서울 관광지도")
    
    # 서울 중심부 좌표로 지도 초기화
    m = folium.Map(location=[37.555, 126.990], zoom_start=12)
    
    # 마커 추가
    for idx, spot in enumerate(tourist_spots, 1):
        popup_html = f"<b>{idx}. {spot['name']}</b><br>{spot['desc']}"
        folium.Marker(
            location=[spot['lat'], spot['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{idx}. {spot['name']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
    
    # 스트림릿에 지도 렌더링
    st_folium(m, width="100%", height=500, returned_objects=[])

with col2:
    st.subheader("📌 명소 리스트")
    for idx, spot in enumerate(tourist_spots, 1):
        with st.expander(f"{idx}. {spot['name']}"):
            st.write(spot['desc'])


