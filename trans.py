import pandas as pd

# 장르 코드를 한국어로 변환하는 딕셔너리
GENRE_MAPPING = {
    'ACTION': '액션',
    'DAILY': '일상',
    'DRAMA': '드라마',
    'FANTASY': '판타지',
    'HISTORICAL': '무협',
    'PURE': '순정',
    'SENSIBILITY': '감성',
    'SPORTS': '스포츠',
    'THRILL': '스릴러'
}

def convert_genre_to_korean(genre_code):
    """영문 장르 코드를 한국어로 변환"""
    # COMIC은 건너뛰기
    if genre_code == 'COMIC':
        return ''
    return GENRE_MAPPING.get(genre_code, genre_code)

def convert_genres_in_file(input_file):
    try:
        # CSV 파일 읽기
        print(f"{input_file} 파일을 읽는 중...")
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        
        # 장르 컬럼이 있는지 확인
        if '장르' not in df.columns:
            print("장르 컬럼을 찾을 수 없습니다.")
            return
        
        # 평점이 8.5 이하인 웹툰 제외
        print("평점이 8.5 이하인 웹툰을 제외하는 중...")
        df = df[df['평점'].astype(float) > 8.5]
        print(f"남은 웹툰 수: {len(df)}개")
        
        # 장르 변환
        print("장르를 한국어로 변환하는 중...")
        df['장르'] = df['장르'].apply(lambda x: ', '.join([convert_genre_to_korean(genre.strip()) 
                                                    for genre in str(x).split(',') 
                                                    if convert_genre_to_korean(genre.strip())]) if pd.notna(x) else '')
        
        # 결과 저장
        output_file = input_file.replace('.csv', 'trance.csv')
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"변환된 데이터가 {output_file}에 저장되었습니다.")
        
        # 변환 결과 미리보기
        print("\n=== 변환 결과 미리보기 ===")
        print(df[['제목', '장르', '평점']].head())
        
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    input_file = "webtoon_genres_20250611_133703.csv"  # 입력 파일명
    convert_genres_in_file(input_file) 