# -*- coding: utf-8 -*-
# [정보 수행평가] 발로란트 V26 ACT III 최신 티어 분포 분석 프로그램

# 1. 이미지(1000005804.jpg) 그래프를 바탕으로 입력한 최신 통계 데이터
# (I1=아이언1, B1=브론즈1, S1=실버1, G1=골드1, P1=플래티넘1, D1=다이아1, A1=초월자1, I1=불멸1, R=레디언트)
valorant_stats = [
    {"tier": "레디언트 (R)", "ratio": 0.1, "top": 0.1},
    {"tier": "불멸 (Immortal)", "ratio": 1.0, "top": 1.1},
    {"tier": "초월자 (Ascendant)", "ratio": 4.5, "top": 5.6},
    {"tier": "다이아몬드 (Diamond)", "ratio": 9.5, "top": 15.1},
    {"tier": "플래티넘 (Platinum)", "ratio": 16.5, "top": 31.6},
    {"tier": "골드 (Gold)", "ratio": 23.0, "top": 54.6},  # 그래프에서 가장 높음
    {"tier": "실버 (Silver)", "ratio": 22.0, "top": 76.6},
    {"tier": "브론즈 (Bronze)", "ratio": 17.0, "top": 93.6},
    {"tier": "아이언 (Iron)", "ratio": 6.4, "top": 100.0}
]

print("================================================================")
print("     VALORANT KOREA COMPETITIVE RANK DISTRIBUTION (V26)")
print("================================================================")
print("  티어 구간\t\t│  유저 비율\t│  상위 누적 백분위")
print("----------------------------------------------------------------")

# 데이터를 표 형태로 출력하는 반복문
for data in valorant_stats:
    print(f"  {data['tier']:<18}\t│  {data['ratio']:.1f}%\t│  상위 {data['top']:.1f}%")

print("================================================================")

# 사용자 입력 및 분석 구간
user_input = input("\n자신의 티어를 입력하세요 (예: 골드, 플래, 다이아): ").strip()

is_found = False
for data in valorant_stats:
    if user_input in data['tier'] or data['tier'].lower().startswith(user_input.lower()):
        print("\n" + "*" * 64)
        print(f" [분석 결과] 입력하신 티어는 전체 유저 중 [{data['top']:.1f}%] 이내입니다.")
        print(f" 현재 한국 서버에서 해당 티어의 비율은 약 {data['ratio']:.1f}% 입니다.")
        print("*" * 64)
        is_found = True
        break

if not is_found:
    print("\n[알림] 티어 이름을 확인하고 다시 입력해주세요. (예: 골드, 실버)")
