import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. 한글 폰트 설정 (Streamlit Cloud 환경 자동 대응)
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

# 2. 데이터 로드 및 인코딩 해결
@st.cache_data
def load_data():
    # 파일 인코딩 문제를 해결하기 위해 여러 방식을 순차적으로 시도합니다.
    encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv("population.csv", encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
            
    if df is None:
        st.error("population.csv 파일을 읽을 수 없습니다. 인코딩 형식을 확인해주세요.")
        st.stop()
    
    # 행정구역 명칭에서 '구 이름'만 깔끔하게 추출
    df['구이름'] = df['행정구역'].str.extract(r'서울특별시\s+([^\s(]+)')
    df['구이름'] = df['구이름'].fillna('서울시 전체')
    
    return df

try:
    df = load_data()

    # 3. 셀렉트박스를 통한 행정구 선택
    gu_list = df['구이름'].unique().tolist()
    selected_gu = st.selectbox("조회할 행정구를 선택하세요", gu_list)

    # 선택한 구의 데이터 추출
    selected_data = df[df['구이름'] == selected_gu].iloc[0]

    # 연령대 컬럼명 지정 (60에서~69세 반영)
    age_columns = ['0~9세', '10~19세', '20~29세', '30~39세', '40~49세', '50~59세', '60에서~69세', '70~79세', '80~89세', '90~99세', '100세 이상']
    
    # 쉼표(,) 제거 후 숫자로 변환
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

    # 그래프 바탕색 설정 (연한 보라색)
    ax.set_facecolor('#F0E6FF')      
    fig.patch.set_facecolor('#F5F0FF') 

    # 꺾은선 그래프 플롯 (빨간색)
    ax.plot(age_columns, population_values, marker='o', color='red', linestyle='-', linewidth=2, markersize=6)

    # 그래프 타이틀 및 축 설정
    ax.set_title(f"서울시의 인구통계 ({selected_gu})", fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel("연령대", fontsize=12, labelpad=10)
    ax.set_ylabel("인구수 (명)", fontsize=12, labelpad=10)

    ax.grid(True, linestyle='--', alpha=0.5, color='#999999')

    # y축 천 단위 쉼표 포맷
    import matplotlib.ticker as ticker
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.xticks(rotation=45)
    plt.tight_layout()

    # 스트림릿에 그래프 출력
    st.pyplot(fig)

    # 5. 하단 데이터 표 출력
    st.subheader("상세 데이터")
    df_show = pd.DataFrame({'연령대': age_columns, '인구수(명)': population_values})
    df_show['인구수(명)'] = df_show['인구수(명)'].apply(lambda x: format(x, ','))
    st.dataframe(df_show.set_index('연령대').T)

except FileNotFoundError:
    st.error("`population.csv` 파일을 찾을 수 없습니다. 대시보드 파일과 동일한 경로에 업로드해 주세요.")
