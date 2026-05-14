import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 취향 저격소", page_icon="📚")

# 제목 부분
st.title("✨ MBTI별 인생 책 & 영화 추천 ✨")
st.write("너의 MBTI를 선택해봐! 딱 맞는 추천 아이템을 보여줄게. 😎")

# MBTI 데이터베이스 (청소년 취향 저격 버전!)
mbti_data = {
    "ISTJ": {"book": "데미안", "movie": "인턴", "reason": "성실하고 책임감 있는 너에겐 따뜻한 조언과 성장이 담긴 이야기가 딱이야! 💼"},
    "ISFJ": {"book": "나미야 잡화점의 기적", "movie": "어바웃 타임", "reason": "배려심 깊은 너의 마음을 몽글몽글하게 만들어줄 다정한 이야기들이야. ❤️"},
    "INFJ": {"book": "어린 왕자", "movie": "인셉션", "reason": "생각이 깊고 통찰력 있는 너를 위한 철학적이고 신비로운 세계관이야. 🌌"},
    "INTJ": {"book": "사피엔스", "movie": "테넷", "reason": "지적 호기심이 넘치고 전략적인 너에겐 거대한 스케일의 지식과 논리가 필요해! 🧠"},
    "ISTP": {"book": "파친코", "movie": "탑건: 매버릭", "reason": "냉철한 분석력과 스릴을 즐기는 너에게 몰입감 넘치는 경험을 줄 거야. ✈️"},
    "ISFP": {"book": "달러구트 꿈 백화점", "movie": "리틀 포레스트", "reason": "예술적 감수성이 풍부하고 자유로운 너를 위한 힐링 세트! 🌿"},
    "INFP": {"book": "호밀밭의 파수꾼", "movie": "월플라워", "reason": "섬세하고 이상적인 너의 마음을 위로해줄 진솔한 성장 드라마야. 🌙"},
    "INTP": {"book": "코스모스", "movie": "매트릭스", "reason": "세상의 원리에 관심이 많은 너를 위한 끝없는 탐구와 상상력의 끝판왕! 🪐"},
    "ESTP": {"book": "돈의 속성", "movie": "분노의 질주", "reason": "에너지 넘치고 현실적인 감각이 뛰어난 너를 위한 화끈한 액션과 꿀팁! 🏎️"},
    "ESFP": {"book": "미드나잇 라이브러리", "movie": "위대한 쇼맨", "reason": "인생의 즐거움을 아는 너에게 화려한 쇼와 희망찬 에너지를 선물할게! 🎪"},
    "ENFP": {"book": "모모", "movie": "라라랜드", "reason": "상상력 대장인 너의 가슴을 뛰게 할 낭만적이고 창의적인 이야기들이야. 🌈"},
    "ENTP": {"book": "부의 추월차선", "movie": "아이언맨", "reason": "고정관념을 깨는 걸 좋아하는 너에게 영감을 줄 혁신적인 캐릭터와 메시지! 🚀"},
    "ESTJ": {"book": "그릿(GRIT)", "movie": "머니볼", "reason": "목표를 향해 달려가는 너의 열정에 불을 지필 체계적이고 효율적인 성공담! 📈"},
    "ESFJ": {"book": "아몬드", "movie": "인사이드 아웃", "reason": "사람 사이의 관계와 감정을 중요하게 생각하는 너에게 깊은 공감을 줄 거야. 😊"},
    "ENFJ": {"book": "연금술사", "movie": "죽은 시인의 사회", "reason": "모두를 이끄는 따뜻한 리더인 너에게 꿈과 희망의 가치를 알려주는 작품이야. 🕯️"},
    "ENTJ": {"book": "생각에 관한 생각", "movie": "더 울프 오브 월 스트리트", "reason": "야망 있고 카리스마 넘치는 너의 실행력을 자극할 강렬한 이야기들! 💎"},
}

# 선택창 만들기
mbti_list = sorted(list(mbti_data.keys()))
choice = st.selectbox("너의 MBTI는 뭐야? 👇", mbti_list)

# 결과 출력
if choice:
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📖 추천 도서")
        st.info(f"**{mbti_data[choice]['book']}**")
        
    with col2:
        st.subheader("🎬 추천 영화")
        st.success(f"**{mbti_data[choice]['movie']}**")
        
    st.write(f"### 🧐 왜 추천하냐면...")
    st.write(mbti_data[choice]['reason'])
    
    st.balloons() # 축하 효과!

# 푸터
st.caption("제작: 너의 AI 친구 🤖 | 오늘 하루도 즐겁게 보내!")








