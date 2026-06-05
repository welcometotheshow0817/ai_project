import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 캐릭터 & 디너 추천", page_icon="🎬", layout="centered")

# 배경 및 폰트 스타일링
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stSelectbox label { color: #10b981 !important; font-size: 1.2rem; font-weight: bold; }
    .result-box {
        background: #1e293b;
        padding: 30px;
        border-radius: 20px;
        border-left: 8px solid #10b981;
        margin-top: 25px;
    }
    .char-name { color: #10b981; font-size: 2rem; font-weight: bold; margin-bottom: 5px; }
    .menu-item { font-size: 1.1rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🎬 MBTI 캐릭터 & 디너 풀코스")
st.write("당신과 닮은 **유명 캐릭터**를 확인하고, 그 캐릭터가 즐길 법한 **최고의 메뉴**를 추천받으세요!")

# 16가지 MBTI 및 캐릭터 데이터
mbti_data = {
    "INTJ": {"char": "배트맨 (다크 나이트)", "trait": "치밀한 계획가", "group": "NT"},
    "INTP": {"char": "셜록 홈즈 (BBC 셜록)", "trait": "천재적인 분석가", "group": "NT"},
    "ENTJ": {"char": "볼드모트 (해리 포터)", "trait": "강력한 지도자", "group": "NT"},
    "ENTP": {"char": "토니 스타크 (아이언맨)", "trait": "재기발랄한 발명가", "group": "NT"},
    "INFJ": {"char": "알버스 덤블도어 (해리 포터)", "trait": "통찰력 있는 선구자", "group": "NF"},
    "INFP": {"char": "프로도 배긴스 (반지의 제왕)", "trait": "낭만적인 중재자", "group": "NF"},
    "ENFJ": {"char": "카마도 탄지로 (귀멸의 칼날)", "trait": "정의로운 주인공", "group": "NF"},
    "ENFP": {"char": "스파이더맨 (피터 파커)", "trait": "재기발랄한 활동가", "group": "NF"},
    "ISTJ": {"char": "헤르미온느 그레인저 (해리 포터)", "trait": "철저한 관리자", "group": "SJ"},
    "ISFJ": {"char": "캡틴 아메리카 (마블)", "trait": "헌신적인 수호자", "group": "SJ"},
    "ESTJ": {"char": "드와이트 슈루트 (더 오피스)", "trait": "엄격한 감독관", "group": "SJ"},
    "ESFJ": {"char": "모니카 겔러 (프렌즈)", "trait": "친절한 사교가", "group": "SJ"},
    "ISTP": {"char": "아리아 스타크 (왕좌의 게임)", "trait": "냉철한 기술자", "group": "SP"},
    "ISFP": {"char": "해리 포터 (해리 포터)", "trait": "예술가적 영혼", "group": "SP"},
    "ESTP": {"char": "잭 스패로우 (해적)", "trait": "모험을 즐기는 사업가", "group": "SP"},
    "ESFP": {"char": "손오공 (드래곤볼)", "trait": "자유로운 영혼의 연예인", "group": "SP"}
}

# 메뉴 데이터
menus = {
    "NT": {"main": "🥩 프라임 립아이 스테이크", "dessert": "🍫 다크 초콜릿 무스", "drink": "☕ 에스프레소", "guide": "최고의 효율과 퀄리티를 중시하는 당신을 위한 선택입니다."},
    "NF": {"main": "🍝 로제 파스타", "dessert": "🍰 딸기 생크림 케이크", "drink": "🫖 얼그레이 밀크티", "guide": "감성과 의미를 소중히 여기는 당신의 마음을 채워줍니다."},
    "SJ": {"main": "🍲 돼지고기 김치찌개", "dessert": "🍡 쫀득한 찹쌀떡", "drink": "🌾 시원한 식혜", "guide": "안정감과 신뢰를 주는 든든한 한국인의 정석입니다."},
    "SP": {"main": "🔥 화끈한 마라탕", "dessert": "🍓 딸기 탕후루", "drink": "🍹 과일 에이드", "guide": "오감을 자극하는 모험적인 맛의 조화입니다."}
}

# 선택창
mbti_choice = st.selectbox("당신의 MBTI는?", list(mbti_data.keys()), index=None, placeholder="목록에서 선택하세요")

if st.button("오늘의 페르소나 & 메뉴 확인 🔍"):
    if mbti_choice:
        char_info = mbti_data[mbti_choice]
        menu_info = menus[char_info["group"]]
        
        st.balloons()
        st.markdown(f"""
            <div class="result-box">
                <div style='color:#94a3b8; font-size:1rem;'>당신의 페르소나 캐릭터</div>
                <div class="char-name">{char_info['char']}</div>
                <p style='font-size:1.2rem; font-style:italic;'>"{char_info['trait']}"</p>
                <hr style='border-color:rgba(255,255,255,0.1)'>
                <div class="menu-item">🍽️ <b>메인:</b> {menu_info['main']}</div>
                <div class="menu-item">🍰 <b>디저트:</b> {menu_info['dessert']}</div>
                <div class="menu-item">🍹 <b>음료:</b> {menu_info['drink']}</div>
                <div style='margin-top:20px; color:#10b981; font-weight:bold;'>💡 가이드: {menu_info['guide']}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("MBTI를 먼저 선택해 주세요!")

### 💡 달라진 점
1. **16가지 모든 유형 대응
