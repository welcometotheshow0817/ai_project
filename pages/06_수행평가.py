# ====================================================================
# [정보 수행평가] 발로란트 티어 통계 및 백분위 데이터 분석 프로그램
# 기능: 예외 처리 기능이 추가된 티어 분포 표 출력 및 사용자 상위 % 분석
# ====================================================================

# 1. 2026년 기준 발로란트 티어 데이터 (정밀 가공 데이터)
valorant_tiers = [
    {"rank": "레디언트", "ratio": 0.1, "top": 0.1},
    {"rank": "불멸", "ratio": 1.0, "top": 1.1},
    {"rank": "초월자", "ratio": 3.9, "top": 5.0},
    {"rank": "다이아몬드", "ratio": 8.5, "top": 13.5},
    {"rank": "플래티넘", "ratio": 15.8, "top": 29.3},
    {"rank": "골드", "ratio": 22.6, "top": 51.9},
    {"rank": "실버", "ratio": 23.4, "top": 75.3},
    {"rank": "브론즈", "ratio": 18.2, "top": 93.5},
    {"rank": "아이언", "ratio": 6.5, "top": 100.0},
]

def print_tier_table():
    """한글 깨짐 및 밀림 현상을 방지한 격자형 표 출력 함수"""
    print("\n" + "┌" + "─"*16 + "┬" + "─"*16 + "┬" + "─"*16 + "┐")
    print(f"│    티어 이름     │    유저 비율     │  상위 누적 백분위│")
    print("├" + "─"*16 + "┼" + "─"*16 + "┼" + "─"*16 + "┤")
    
    for tier in valorant_tiers:
        # 한글 글자수 정렬 문제를 해결하기 위해 서식을 지정하여 표를 그립니다.
        rank_str = tier['rank'].center(10)
        ratio_str = f"{tier['ratio']}%".center(14)
        top_str = f"상위 {tier['top']}%".center(12)
        print(f"│ {rank_str} │ {ratio_str} │ {top_str} │")
        
    print("└" + "─"*16 + "┴" + "─"*16 + "┴" + "─"*16 + "┘")

def analyze_user_position(user_input):
    """'골드3', '실버 1' 처럼 숫자가 포함되어도 앞 글자만 따서 판정하는 예외처리 기능"""
    # 사용자가 입력한 문자열에서 공백을 제거하고, '골드', '실버' 등 한글 핵심 단어만 추출
    cleaned_input = ""
    for char in user_input:
        if char.isalpha():  # 숫자나 특수문자가 아닌 '글자'만 추출
            cleaned_input += char

    is_found = False
    
    for tier in valorant_tiers:
        # 입력값에 티어 이름이 포함되어 있는지 확인 (예: '골드3' 입력 시 '골드' 검색 성공)
        if tier['rank'] in cleaned_input or cleaned_input in tier['rank']:
            print("\n" + "★" * 50)
            print(f" [분석 완료] 입력하신 티어 기반 판정: [{tier['rank']}] 구간")
            print(f" 당신은 전 세계 발로란트 유저 중 약 '상위 {tier['top']}%'에 해당합니다.")
            
            # 실력 지표 멘트 분기문
            if tier['top'] <= 5.0:
                print(" -> 한 줄 평가: 천상계 유저입니다. 랭커를 노려보세요!")
            elif tier['top'] <= 30.0:
                print(" -> 한 줄 평가: 상위권 숙련자입니다. 팀의 핵심 역할을 합니다.")
            elif tier['top'] <= 60.0:
                print(" -> 평가: 가장 두터운 중간층입니다. 조금만 노력하면 상위권 진입 가능!")
            else:
                print(" -> 평가: 하위 구간을 탈출하기 위해 맵 리딩과 에임 연습이 필요합니다.")
            print("★" * 50)
            is_found = True
            break
            
    if not is_found:
        print("\n[오류] 입력값을 인식하지 못했습니다. '골드', '실버 2' 처럼 정확한 티어를 적어주세요.")

# ==================== 프로그램 실행부 ====================
if __name__ == "__main__":
    print("\n==================================================")
    print("      VALORANT TIER DATA ANALYZER (2026)")
    print("==================================================")
    
    # 1. 표 출력
    print_tier_table()
    
    # 2. 사용자 입력 및 분석
    user_tier = input("\n당신의 발로란트 티어를 입력하세요 (예: 골드 2, 플래): ").strip()
    analyze_user_position(user_tier)
