import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. 한글 폰트 설정 (Streamlit Cloud 환경 자동 대응)
# 리눅스 서버 환경인 Streamlit Cloud에서 한글 깨짐을 방지하기 위해 나눔 폰트를 다운로드 및 적용합니다.
@st.cache_data
def load_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic-Regular.ttf"
    if not os.path.exists(font_path):
        import urllib.request
        urllib.request.urlretrieve(font_url, font_path)
    return font_path

try:
    font_path = load_font()
    fe = fm.FontEntry(fontpath=font_path, name='NanumGothic')
    fm.fontManager.ttflist.insert(0, fe)
    plt.rcParams['font.family'] = 'NanumGothic'
except Exception as e:
    st.warning(f"한글 폰트 로드 중 오류가 발생했습니다: {e}. 기본 폰트를 사용합니다.")

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

st.title("서울시 구별 연령대별 인구 분포 현황")

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    # 제공해주신 population.csv 파일이 소스코드와 같은 경로에 있다고 가정합니다.
    df = pd.read_csv("population.csv")
    
    # 정규식을 이용해 행정구역 명칭에서 '구 이름'만 깔끔하게 추출 (예: "서울특별시 종로구 (1111000000)" -> "종로구")
    df['구이름'] = df['행정구역'].str.extract(r'서울특별시\s+([^\s(]+)')
    
    # '서울특별시' 전체 총계 행은 구이름이 NaN이 되므로 '서울시 전체'로 변경합니다.
    df['구이름'] = df['구이름'].fillna('서울시 전체')
    
    return df

try:
    df = load_data()

    # 3. 셀렉트박스를 통한 행정구 선택
    gu_list = df['구이름'].unique().tolist()
    selected_gu = st.selectbox("조회할 행정구를 선택하세요", gu_list)

    # 선택한 구의 데이터 추출
    selected_data = df[df['구이름'] == selected_gu].iloc[0]

    # 제공된 파일의 정확한 연령대 컬럼명 지정 (중간에 '60에서~69세' 특이 패턴 반영)
    age_columns = ['0~9세', '10~19세', '20~29세', '30~39세', '40~49세', '50~59세', '60에서~69세', '70~79세', '80~89세', '90~99세', '100세 이상']
    
    # 쉼표(,)가 포함된 인구수 데이터를 정수로 변환
    population_values = []
    for col in age_columns:
        val = selected_data[col]
        if isinstance(val, str):
            val = int(val.replace(',', ''))
        else:
            val = int(val)
        population_values.append(val)

    # 4. 시각화 (Matplotlib)
    fig, ax = plt.subplots(figsize=(10, 6))

    # 그래프 바탕색 설정 (연한 보라색 계열)
    ax.set_facecolor('#F0E6FF')      # 그래프 내부 플롯 안쪽 배경색
    fig.patch.set_facecolor('#F5F0FF') # 외부 피겨 테두리 배경색

    # 꺾은선 그래프 플롯 (지정 조건: 빨간색)
    ax.plot(age_columns, population_values, marker='o', color='red', linestyle='-', linewidth=2, markersize=6)

    # 그래프 디자인 구성
    ax.set_title(f"서울시의 인구통계 ({selected_gu})", fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel("연령대", fontsize=12, labelpad=10)
    ax.set_ylabel("인구수 (명)", fontsize=12, labelpad=10)

    # 점선 그리드 추가
    ax.grid(True, linestyle='--', alpha=0.5, color='#999999')

    # 세로축 인구수에 천 단위 콤마(,) 표시 포맷 적용
    import matplotlib.ticker as ticker
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # X축 글자 기울임 (연령대 텍스트 겹침 방지)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 스트림릿 웹 화면에 그래프 렌더링
    st.pyplot(fig)

    # 5. 하단 데이터프레임 보조 표 출력
    st.subheader("상세 데이터")
    df_show = pd.DataFrame({'연령대': age_columns, '인구수(명)': population_values})
    df_show['인구수(명)'] = df_show['인구수(명)'].apply(lambda x: format(x, ','))
    st.dataframe(df_show.set_index('연령대').T)

except FileNotFoundError:
    st.error("`population.csv` 파일을 찾을 수 없습니다. 대시보드 파일(`app.py`)과 동일한 폴더(GitHub 리포지토리)에 배치해 주세요.")
