# 기존 load_data() 함수를 아래 코드로 수정하세요.
@st.cache_data
def load_data():
    # 파일 인코딩 문제를 해결하기 위해 여러 인코딩 방식을 순차적으로 시도합니다.
    encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv("population.csv", encoding=encoding)
            # 성공적으로 읽어왔다면 루프 탈출
            break
        except UnicodeDecodeError:
            continue
            
    if df is None:
        raise ValueError("파일을 읽을 수 없습니다. 인코딩 형식을 확인해주세요.")
    
    # 정규식을 이용해 행정구역 명칭에서 '구 이름'만 깔끔하게 추출 (예: "서울특별시 종로구 (1111000000)" -> "종로구")
    df['구이름'] = df['행정구역'].str.extract(r'서울특별시\s+([^\s(]+)')
    
    # '서울특별시' 전체 총계 행은 구이름이 NaN이 되므로 '서울시 전체'로 변경합니다.
    df['구이름'] = df['구이름'].fillna('서울시 전체')
    
    return df
