import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정 (중앙 집중형 구조로 깔끔하게 배치)
st.set_page_config(
    page_title="서울 인기 관광지 TOP 10",
    page_icon="🗼",
    layout="wide"
)

# 커스텀 폰트 및 스타일링 정의
st.markdown("""
    <style>
    .title-text {
        text-align: center;
        color: #1E3A8A;
        font-weight: bold;
    }
    .subtitle-text {
        text-align: center;
        color: #4B5563;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🇰🇷 외국인이 좋아하는 서울 주요 관광지 TOP 10</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>지도를 통해 위치를 확인하고, 아래 상세 정보 창에서 명소별 지하철역과 알찬 놀거리를 확인해 보세요!</p>", unsafe_allow_html=True)

# 2. 데이터 정의 (상세 정보 포함)
tourist_spots = [
    {
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "한국의 전통미를 느낄 수 있는 대표 고궁",
        "subway": "3호선 경복궁역 5번 출구 (도보 1분 거리)",
        "details": "경복궁 인근 한복 대여점에서 이색적인 고전 한복을 차려입고 입궁해 예쁜 사진을 찍으며 조선시대로 시간 여행을 떠나보세요.\n오전 10시와 오후 2시 광화문 앞에서 열리는 웅장한 수문장 교대식을 관람하며 한국 고유의 전통 군례 문화를 가까이서 경험할 수 있습니다.\n웅장한 경회루 연못가를 산책한 뒤, 뒤편에 위치한 국립민속박물관과 아름다운 옛 유물이 가득한 국립고궁박물관까지 무료로 연계 관람하는 코스를 추천합니다."
    },
    {
        "name": "N서울타워",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울 시내를 한눈에 내려다보는 전망대",
        "subway": "4호선 명동역 3번 출구에서 남산케이블카까지 도보 10분 후 케이블카 이용",
        "details": "전망대에 올라 360도로 드넓게 펼쳐지는 아름다운 서울 도심의 환상적인 낮 전경과 로맨틱한 밤 야경을 온몸으로 한껏 만끽해 보세요.\n광장 철조망 난간에 사랑하는 사람과 소망을 담은 메시지를 적어 굳게 걸어 잠그는 '사랑의 자물쇠' 체험을 즐기며 뜻깊은 순간을 약속해 보세요.\n다채로운 실내 미디어 아트 전시를 체험하고, 하산할 때는 남산 둘레길 산책로를 가볍게 도보로 내려오며 도심 속 고요한 자연을 즐기기 좋습니다."
    },
    {
        "name": "명동 쇼핑거리",
        "lat": 37.5634,
        "lon": 126.9846,
        "desc": "쇼핑과 길거리 음식의 천국",
        "subway": "4호선 명동역 6번 출구 (출구 나오면 바로 연결)",
        "details": "전 세계에서 모인 트렌디한 K-뷰티 브랜드와 유명 패션 로드숍이 한데 모인 쇼핑거리에서 자유로운 로드숍 쇼핑을 활기차게 즐겨보세요.\n매일 늦은 오후부터 열리는 야시장의 길거리 음식 포차에서 치즈 랍스터 구이, 누텔라 크레페, 회오리 감자 등 이색 미식 투어를 경험해 보세요.\n도심 속 고즈넉한 붉은 벽돌이 아름다운 고딕 양식의 명동성당을 한 바퀴 둘러보며 도심 한가운데서 평화로운 치유와 안식을 느낄 수 있습니다."
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.5829,
        "lon": 126.9835,
        "desc": "실제 주민들이 거주하는 전통 한옥 밀집 지역",
        "subway": "3호선 안국역 2번 출구 (도보 10분 거리)",
        "details": "오랜 역사를 품고 실제로 사람들이 살아가는 기와집 가득한 골목길을 걸으며, 고즈넉한 옛 풍경과 멀리 보이는 현대적 빌딩의 놀라운 조화를 감상하세요.\n마을 내 위치한 아기자기한 한옥 공방에 방문해 직접 고풍스러운 천연 염색, 가죽 공예 또는 다도 원데이 클래스를 수강하며 한국의 예절을 배울 수 있습니다.\n조용한 한옥 마당을 아늑하게 개조한 감성 가득한 한옥 카페에서 창밖의 풍경을 보며 전통 쌍화차나 달콤한 인절미 디저트를 음미해 보세요."
    },
    {
        "name": "인사동",
        "lat": 37.5744,
        "lon": 126.9874,
        "desc": "한국 전통 기념품과 찻집이 가득한 곳",
        "subway": "3호선 안국역 6번 출구 (도보 2분) 또는 1호선 종각역 3번 출구 (도보 5분)",
        "details": "독특한 경사로식 골목길로 이루어진 복합문화공간 '쌈지길'을 걸어 올라가며 디자이너들의 독창적인 공예품과 액세서리들을 찬찬히 구경해 보세요.\n은은한 가야금 연주와 고전 가구들이 어우러진 옛 다원에서 따뜻한 대추차와 가래떡 구이를 꿀에 찍어 먹는 고즈넉한 맛의 여유를 느껴보세요.\n한글 간판으로만 구성된 이색적인 브랜드 거리에서 기념사진을 남기고, 주변 갤러리 골목에서 상시 열리는 다양한 한국화 전시를 감상해 볼 수 있습니다."
    },
    {
        "name": "동대문디자인플라자 (DDP)",
        "lat": 37.5668,
        "lon": 127.0094,
        "desc": "독특한 야경과 디자인 전시가 열리는 곳",
        "subway": "2, 4, 5호선 동대문역사문화공원역 1번 출구 (지하 연결 통로 연결)",
        "details": "세계적인 건축가 자하 하디드가 설계한 우주선 모양의 거대한 세계 최대 규모 3차원 비정형 건축물 외부를 배경으로 미래지향적인 사진을 연출해 보세요.\n연중 상시 다채롭게 개최되는 글로벌 패션 위크 및 예술 디자인 전시를 관람하며 실내에서 쾌적하고 세련된 여가 시간을 즐길 수 있습니다.\n특히 어둠이 내리는 밤이 찾아오면 거대한 곡선 알루미늄 외벽을 스크린 삼아 환상적으로 밤하늘을 수놓는 미디어 파사드 레이저 쇼를 감상해 보세요."
    },
    {
        "name": "홍대거리",
        "lat": 37.5567,
        "lon": 126.9236,
        "desc": "젊음과 버스킹, 트렌디한 카페의 중심지",
        "subway": "2호선, 공항철도, 경의중앙선 홍대입구역 9번 출구 (도보 1분)",
        "details": "주말과 야간에 걷고싶은거리 광장에서 활력 넘치게 펼쳐지는 인디 밴드들의 신나는 라이브 음악과 화려한 댄스 버스킹 공연을 눈앞에서 직접 관람해 보세요.\n감각적으로 꾸며진 네컷사진 스튜디오나 레트로 오락실, VR 게임방 등에 방문해 친구들과 함께 트렌디하고 유쾌한 K-놀이 문화를 체험할 수 있습니다.\n트렌디한 편집숍에서 개성 넘치는 패션 잡화를 쇼핑하고, 늦은 밤에는 힙한 감성의 실내 펍과 라이브 클럽에서 열정 가득한 시간을 즐겨보세요."
    },
    {
        "name": "롯데월드타워 & 몰",
        "lat": 37.5126,
        "lon": 127.1025,
        "desc": "세계에서 5번째로 높은 빌딩과 테마파크",
        "subway": "2호선 및 8호선 잠실역 1, 2번 출구 (지하 광장과 직접 연결)",
        "details": "세계 최고 수준의 초고층 전망대 '서울스카이'로 올라가, 아찔한 투명 유리 바닥 데크 위에 서서 발아래 펼쳐지는 아찔하고 거대한 스카이라인을 구경해 보세요.\n동화 같은 매직아일랜드 성이 있는 롯데월드 어드벤처에서 신나는 놀이기구를 타거나, 아름다운 석촌호수 산책로를 걸으며 낭만적인 밤공기를 쐬어보세요.\n복합쇼핑몰인 롯데월드몰 내부에서 초대형 아쿠아리움 수조 감상, 면세점 브랜드 쇼핑, 테마 식당가 한식 맛집 투어까지 날씨 걱정 없이 쾌적하게 즐길 수 있습니다."
    },
    {
        "name": "이태원 관광특구",
        "lat": 37.5345,
        "lon": 126.9942,
        "desc": "다양한 문화와 이국적인 맛집이 모인 곳",
        "subway": "6호선 이태원역 1~4번 출구 (지하철역에서 거리 연결)",
        "details": "그리스, 브라질, 태국, 레바논 등 전 세계 정통 셰프들이 선보이는 다채롭고 특별한 오리지널 글로벌 요리들을 한자리에서 자유롭게 맛보세요.\n남산 서울타워 뷰가 아름답게 정면으로 보이는 트렌디한 해방촌 일대 루프탑 바에 앉아 로맨틱한 노을과 시원한 수제 맥주 한 잔을 여유롭게 나누어 보세요.\n앤티크 가구 거리에서 독특한 빈티지 소품들을 보물찾기하듯 즐겁게 구경하고, 골목 곳곳을 수놓은 스트리트 그래피티 아트를 배경으로 힙한 사진을 남겨보세요."
    },
    {
        "name": "광장시장",
        "lat": 37.5701,
        "lon": 126.9996,
        "desc": "녹두빈대떡, 육회 등 K-푸드를 체험하는 전통시장",
        "subway": "1호선 종로5가역 8번 출구 (도보 1분) 또는 2/5호선 을지로4가역 4번 출구",
        "details": "맷돌로 즉석에서 갈아 바삭하게 부쳐내는 고소한 녹두빈대떡과 마법 소스에 찍어 먹는 원조 '마약김밥'을 북적이는 야외 가판 시장에 앉아 따뜻하게 맛보세요.\n정갈하고 차갑게 준비되는 신선한 한우 육회 골목에서 달콤한 국산 배와 노른자를 버무린 진한 오리지널 K-푸드를 시원한 주류와 환상적으로 매칭해 드세요.\n한국 시장 특유의 따뜻하고 정이 넘치는 에너지 속에서 길거리 만두, 호떡, 빈대떡을 맛보며 한국 로컬 야시장의 진정한 문화를 온몸으로 느낄 수 있습니다."
    }
]

# 3. 지도 및 선택 상태를 동기화하기 위한 세션 상태 관리
if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0

# 4. 지도 영역 (화면 폭의 60% 크기로 줄여 레이아웃 구성)
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

with col2:
    st.subheader("🗺️ 서울 관광지도 (지하철 및 지명 한글 최적화)")
    
    # 선택된 관광지의 좌표를 지도의 중심좌표로 자동 이동시켜 사용자 경험 극대화
    current_spot = tourist_spots[st.session_state.selected_index]
    m = folium.Map(location=[current_spot["lat"], current_spot["lon"]], zoom_start=13, tiles="OpenStreetMap")
    
    # 지도에 마커 표시 (고대비 선명한 파란색 숫자 디자인 커스텀 적용)
    for idx, spot in enumerate(tourist_spots, 0):
        popup_html = f"<b>{idx+1}. {spot['name']}</b><br>{spot['desc']}"
        
        # 선명한 파란색(Vibrant Royal Blue) 및 고대비 흰색 링 테두리 디자인
        icon_html = f"""
        <div style="
            background-color: #1E40AF; 
            border: 3px solid #60A5FA; 
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 13px;
            font-weight: bold;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.4);
        ">
            {idx+1}
        </div>
        """
        icon = folium.DivIcon(
            html=icon_html,
            icon_size=(32, 32),
            icon_anchor=(16, 16)
        )
        
        folium.Marker(
            location=[spot['lat'], spot['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{idx+1}. {spot['name']}",
            icon=icon
        ).add_to(m)
    
    # 스트림릿에 가로 폭을 이 상자에 맞춰 60% 크기로 단독 렌더링
    st_folium(m, use_container_width=True, height=450, returned_objects=[])

st.write("")
st.write("---")

# 5. 지도 밑 상세 정보 탐색 (관광지 선택 및 지하철역, 상세 놀거리 출력)
st.subheader("🔍 서울 명소 상세 탐방 가이드")
st.markdown("알아보고 싶은 관광지를 아래 목록에서 선택하세요. 가장 가까운 역 정보와 아주 세부적인 즐길거리를 한눈에 볼 수 있습니다.")

# 관광지 이름을 선택박스로 나열
selected_spot_name = st.selectbox(
    "📍 상세 정보를 보실 관광지를 선택하세요:",
    options=[spot["name"] for spot in tourist_spots],
    index=st.session_state.selected_index,
    key="spot_selectbox"
)

# 선택박스가 변경될 때마다 세션 인덱스 상태 변경
selected_spot_index = next(i for i, spot in enumerate(tourist_spots) if spot["name"] == selected_spot_name)
if selected_spot_index != st.session_state.selected_index:
    st.session_state.selected_index = selected_spot_index
    st.rerun()

selected_spot = tourist_spots[st.session_state.selected_index]

# 세련된 커스텀 카드 레이아웃으로 상세 정보 표시
st.markdown(f"""
<div style="
    background-color: #F8FAFC; 
    padding: 30px; 
    border-radius: 16px; 
    border-left: 8px solid #1E40AF;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
    margin-top: 15px;
">
    <h3 style="margin-top: 0; color: #1E3A8A; font-size: 24px; font-weight: bold;"> ⭐ {selected_spot['name']}</h3>
    <p style="font-size: 16px; color: #6B7280; margin-bottom: 20px; font-style: italic;">"{selected_spot['desc']}"</p>
    
    <div style="background-color: #EFF6FF; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <span style="font-size: 18px; font-weight: bold; color: #1E40AF;">🚇 가장 가까운 전철역</span><br>
        <span style="font-size: 16px; color: #1F2937;">{selected_spot['subway']}</span>
    </div>
    
    <div style="background-color: #F1F5F9; padding: 20px; border-radius: 8px;">
        <span style="font-size: 18px; font-weight: bold; color: #334155;">🎡 추천 놀거리 & 구체적인 코스 (3~4줄 가이드)</span><br>
        <p style="font-size: 15px; line-height: 1.8; color: #374151; margin-top: 10px; white-space: pre-line;">
{selected_spot['details']}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

