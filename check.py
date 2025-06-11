import pandas as pd
from datetime import datetime

def check_duplicate_titles(input_file):
    try:
        # CSV 파일 읽기
        print(f"{input_file} 파일을 읽는 중...")
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        total_webtoons = len(df)
        
        # 중복된 제목 확인
        print("\n중복된 제목 확인 중...")
        duplicates = df[df.duplicated(subset=['제목'], keep=False)]
        duplicate_count = len(duplicates)
        
        if duplicate_count > 0:
            print(f"\n=== 중복된 제목 발견 ({duplicate_count}개) ===")
            # 중복된 제목 그룹별로 출력
            for title in duplicates['제목'].unique():
                duplicate_group = duplicates[duplicates['제목'] == title]
                print(f"\n제목: {title}")
                for _, row in duplicate_group.iterrows():
                    print(f"  - 평점: {row['평점']}, 장르: {row['장르']}")
            
            # 중복 제거
            print("\n중복 제거 중...")
            df_no_duplicates = df.drop_duplicates(subset=['제목'], keep='first')
            removed_count = total_webtoons - len(df_no_duplicates)
            
            # 결과 저장
            output_file = input_file.replace('.csv', '_no_duplicates.csv')
            df_no_duplicates.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            # 결과 보고서 생성
            report_file = f"result/duplicate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("=== 웹툰 제목 중복 검사 결과 보고서 ===\n\n")
                f.write(f"처리 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"전체 웹툰 수: {total_webtoons}개\n")
                f.write(f"중복된 제목 수: {duplicate_count}개\n")
                f.write(f"제거된 중복 수: {removed_count}개\n")
                f.write(f"남은 웹툰 수: {len(df_no_duplicates)}개\n\n")
                
                f.write("=== 중복된 제목 목록 ===\n")
                for title in duplicates['제목'].unique():
                    duplicate_group = duplicates[duplicates['제목'] == title]
                    f.write(f"\n제목: {title}\n")
                    for _, row in duplicate_group.iterrows():
                        f.write(f"  - 평점: {row['평점']}, 장르: {row['장르']}\n")
            
            print(f"\n중복 제거 결과:")
            print(f"- 전체 웹툰 수: {total_webtoons}개")
            print(f"- 중복된 제목 수: {duplicate_count}개")
            print(f"- 제거된 중복 수: {removed_count}개")
            print(f"- 남은 웹툰 수: {len(df_no_duplicates)}개")
            print(f"\n중복이 제거된 데이터가 {output_file}에 저장되었습니다.")
            print(f"중복 검사 보고서가 {report_file}에 저장되었습니다.")
            
        else:
            print("\n중복된 제목이 없습니다.")
        
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    input_file = "result/webtoon_genres_20250611_133703trance_preprocessed.csv"  # 입력 파일명
    check_duplicate_titles(input_file) 