def recommend_dinner(mbti):
    # 대문자 변환 및 공백 제거
    mbti = mbti.upper().strip()
    
    # MBTI 그룹별 메뉴 데이터베이스
    menu_db = {
        "NT": {"menu": "🥩 고급 스테이크와 와인", "desc": "오늘 하루도 스마트하게 보낸 당신! 완벽한 단백질과 영양 가득한 스테이크로 효율적인 에너지를 충전하세요."},
        "NF": {"menu": "🍝 감성 가득한 로제 파스타", "desc": "감수성이 풍부한 당신에게 딱 맞는 메뉴! 예쁜 접시에 담아 분위기 있는 음악과 함께 즐겨보세요."},
        "SJ": {"menu": "🍲 든든한 돼지고기 김치찌개", "desc": "계획대로 완벽한 하루를 보낸 당신에게 드리는 최고의 보상! 역시 클래식하고 든든한 집밥이 최고죠."},
        "SP": {"menu": "🔥 스트레스 풀리는 마라탕이나 닭발", "desc": "지루한 건 못 참지! 오늘 저녁은 짜릿하고 화끈한 매운맛으로 미각을 자극해 보세요."}
    }
    
    # MBTI 4글자 유효성 검사
    if len(mbti) != 4 or any(c not in "INFPESTJ" for c in mbti):
        return "⚠️ 올바른 MBTI 4글자를 입력해주세요. (예: INFJ, ESTP)"
    
    # 2번째, 3번째 글자로 그룹 판단
    group = mbti[1:3]
    
    if group in menu_db:
        result = menu_db[group]
        return f"\n🌟 [{mbti}] 성향을 위한 추천 저녁 메뉴 🌟\n👉 추천 메뉴: {result['menu']}\n💬 한줄 이유: {result['desc']}"
    else:
        # 혹시 모를 예외 처리 (예: 코드 로직상 분류되지 않는 조합 방지)
        return "메뉴를 고르는 데 고민이 깊어지네요. 오늘은 맛있는 치킨 어떠신가요?"

# --- 프로그램 실행부 ---
if __name__ == "__main__":
    print("--- 🔮 MBTI 맞춤형 저녁 메뉴 추천기 🔮 ---")
    user_mbti = input("당신의 MBTI를 입력하세요 (예: ENFP, INTJ): ")
    
    recommendation = recommend_dinner(user_mbti)
    print(recommendation)
