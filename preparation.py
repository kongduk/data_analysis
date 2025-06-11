import pandas as pd
from datetime import datetime

def preprocess_webtoon_data(input_file):
    try:
        # CSV 파일 읽기
        print(f"{input_file} 파일을 읽는 중...")
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        total_webtoons = len(df)
        
        # 평점이 8.5 이하인 웹툰 제외
        print("평점이 8.5 이하인 웹툰을 제외하는 중...")
        removed_df = df[df['평점'].astype(float) <= 8.5]  # 제외된 웹툰
        df = df[df['평점'].astype(float) > 8.5]  # 남은 웹툰
        remaining_webtoons = len(df)
        removed_webtoons = len(removed_df)
        
        # 결과 저장
        output_file = input_file.replace('.csv', '_preprocessed.csv')
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        # 결과 보고서 생성
        report_file = f"result/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=== 웹툰 데이터 전처리 결과 보고서 ===\n\n")
            f.write(f"처리 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"전체 웹툰 수: {total_webtoons}개\n")
            f.write(f"제외된 웹툰 수: {removed_webtoons}개\n")
            f.write(f"남은 웹툰 수: {remaining_webtoons}개\n\n")
            
            f.write("=== 기본 통계 정보 ===\n")
            f.write(f"평균 평점: {df['평점'].astype(float).mean():.2f}\n")
            f.write(f"최고 평점: {df['평점'].astype(float).max():.2f}\n")
            f.write(f"최저 평점: {df['평점'].astype(float).min():.2f}\n\n")
            
            f.write("=== 제외된 웹툰 목록 ===\n")
            for _, row in removed_df.sort_values('평점', ascending=False).iterrows():
                f.write(f"제목: {row['제목']}, 평점: {row['평점']}, 장르: {row['장르']}\n")
            f.write("\n")
            
            f.write("=== 지원진 목록 ===\n")
            f.write("1. 데이터 수집: [이름]\n")
            f.write("2. 데이터 전처리: [이름]\n")
            f.write("3. 데이터 분석: [이름]\n")
            f.write("4. 보고서 작성: [이름]\n")
        
        print(f"\n전체 웹툰 수: {total_webtoons}개")
        print(f"제외된 웹툰 수: {removed_webtoons}개")
        print(f"남은 웹툰 수: {remaining_webtoons}개")
        print(f"\n전처리된 데이터가 {output_file}에 저장되었습니다.")
        print(f"결과 보고서가 {report_file}에 저장되었습니다.")
        
        # 제외된 웹툰 목록 출력
        print("\n=== 제외된 웹툰 목록 (평점 순) ===")
        for _, row in removed_df.sort_values('평점', ascending=False).iterrows():
            print(f"제목: {row['제목']}, 평점: {row['평점']}, 장르: {row['장르']}")
        
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    input_file = "result/webtoon_genres_20250611_133703trance.csv"  # 입력 파일명
    preprocess_webtoon_data(input_file)
