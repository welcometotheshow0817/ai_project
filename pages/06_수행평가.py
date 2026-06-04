# -*- coding: utf-8 -*-
# [정보 수행평가] 발로란트 티어별 통계 및 모스트 요원 분석 프로그램
import sys
from tabulate import tabulate

# 2026년 최신 기준 티어별 분포 및 주력 요원 데이터
valorant_data = [
    ["레디언트", "0.1%", "상위 0.1%", "제트, 소바"],
    ["불멸", "1.0%", "상위 1.1%", "제트, 레이즈"],
    ["초월자", "3.9%", "상위 5.0%", "레이나, 제트"],
    ["다이아몬드", "8.5%", "상위 13.5%", "레이나, 제트"],
    ["플래티넘", "15.8%", "상위 29.3%", "레이나, 킬조이"],
    ["골드", "22.6%", "상위 51.9%", "레이나, 세이지"],
    ["실버", "23.4%", "상위 75.3%", "세이지, 레이나"],
    ["브론즈", "18.2%", "상위 93.5%", "세이지, 페이드"],
    ["아이언", "6.5%", "상위 100.0%", "세이지, 피닉스"]
]

# 표의 헤더(제목) 설정
headers = ["티어 이름", "유저 비율", "상위 누적 백분위", "많이 쓰는 요원 (Most)"]

def run_program():
    print("\n" + "="*65)
    print("      VALORANT TIER & AGENT METRICS REPORT (2026)")
    print("="*65)
    
    # tabulate 라이브러리를 사용해 깔끔한 Grid 모양의 표 출력
    print(tabulate(valorant_data, headers=headers, tablefmt="grid"))
    print("="*65)
    
    # 사용자 입력 받기
    user_input = input("\n자신의 티어를 입력하세요 (예: 골드, 플래티넘): ").strip()
    
    # 데이터 검색 및 결과 분석
    is_found = False
    for row in valorant_data:
        if row[0] in user_input or user_input in row[0]:
            print("\n" + "*" * 65)
            print(f" [분석 결과] 당신은 발로란트 유저 중 [{row[2]}] 구간입니다.")
            print(f" 현재 해당 티어의 인기 요원은 [{row[3]}] 입니다.")
            print("*" * 65)
            is_found = True
            break
            
    if not is_found:
        print("\n[알림] 올바른 티어 이름을 입력해주세요. (예: 골드, 실버)")

if __name__ == "__main__":
    run_program()
