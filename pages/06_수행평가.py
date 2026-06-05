import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 저녁 풀코스 추천기", page_icon="🔮", layout="centered")

# 제목 및 설명
st.title("🔮 MBTI 맞춤형 저녁 풀코스 추천기")
st.write("당신의 MBTI를 선택하고 오늘 저녁에 딱 맞는 메인 메뉴, 디저트, 음료 코스를 추천받으세요!")

# 16가지 MBTI 리스트 정의
mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 💡 텍스트 입력 대신 '드롭다운 선택창'으로 변경!
selected_mbti = st.selectbox(
    "당신의 MBTI는 무엇인가요?",
    mbti_list,
    index=None,  # 처음에 아무것도 선택 안 된 상태로 시작
    placeholder="여기를 눌러 MBTI를 선택하세요..."
)

# 데이터베이스
course_db = {
    "NT": {
        "concept": "⚙️ 깔끔함과 고효율을 추구하는 어른의 맛 코스",
        "main": "🥩 고급 스테이크와 구운 채소",
        "dessert": "🍫 진하고 달지 않은 다크 초콜릿 무스",
        "drink": "☕ 깔끔하게 입안을 정돈해 줄 에스프레소",
        "desc": "영양 성분이 확실한 메인 식사 후, 두뇌 회전에 도움을 주는 다크 초콜릿과 깔끔한 커피로 완벽한 마무리를 해보세요."
    },
    "NF": {
        "concept": "✨ 감성과 로맨틱함을 채워줄 힐링 코스",
        "main": "🍝 감성 가득한 로제 파스타",
        "dessert": "🍰 비주얼 끝판왕 딸기 생크림 케이크",
        "drink": "🫖 향긋하고 따뜻한 얼그레이 밀크티",
        "desc": "눈과 입이 모두 즐거운 예쁜 플레이팅은 필수! 감수성이 풍부한 당신의 마음을 몽글몽글하게 채워줄 조합입니다."
    },
    "SJ": {
        "concept": "🏡 실패 없는 클래식, 안정이 최고야 코스",
        "main": "🍲 든든하고 깊은 맛의 돼지고기 김치찌개",
        "dessert": "🍡 쫀득하고 달콤한 찹쌀떡 (또는 약과)",
        "drink": "🌾 살얼음 동동 띄운 시원한 식혜",
        "desc": "한국인이라면 참을 수 없는 완벽한 소울푸드 조합! 얼큰한 찌개 뒤에 오는 전통 디저트의 '단짠' 조화가 완벽합니다."
    },
    "SP": {
        "concept": "🎉 오늘 밤 주인공은 나! 트렌디 짜릿 코스",
        "main": "🔥 스트레스 풀리는 매콤한 마라탕",
        "dessert": "🍓 바삭하고 달콤한 딸기 탕후루 (또는 크루키)",
        "drink": "🍹 톡 쏘는 청량함, 청포도 에이드",
        "desc": "지루한 일상은 가라! 화끈한 매운맛으로 시작해, 요즘 가장 핫한 디저트의 식감과 청량한 탄산으로 오감을 자극해 보세요."
    }
}

# 추천 버튼 (MBTI를 선택했을 때만 활성화)
if st.button("오늘의 저녁 메뉴 추천받기 🍽️"):
    if selected_mbti:
        # 2번째, 3번째 글자로 그룹 판단 (예: INFP -> NF)
        group = selected_mbti[1:3]
        course = course_db[group]
        
        st.success(f"🎉 {selected_mbti} 성향을 위한 맞춤 코스가 준비되었습니다!")
        st.write("---")
        
        # 결과 출력 UI
        st.subheader(course["concept"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="🍽️ 메인 메뉴", value=course["main"].split()[0], delta=" ".join(course["main"].split()[1:]), delta_color="off")
        with col2:
            st.metric(label="🍰 디저트", value=course["dessert"].split()[0], delta=" ".join(course["dessert"].split()[1:]), delta_color="off")
        with col3:
            st.metric(label="🍹 음료", value=course["drink"].split()[0], delta=" ".join(course["drink"].split()[1:]), delta_color="off")
            
        st.write("---")
        st.info(f"💡 **코스 가이드:** {course['desc']}")
    else:
        st.warning("⚠️ 목록에서 MBTI를 먼저 선택해 주세요!")
