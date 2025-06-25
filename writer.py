import pandas as pd
import numpy as np

# CSV 파일 로딩
df = pd.read_csv('webtoon.csv')

print("=" * 60)
print("👨‍🎨 작가별 가중 평점 분석")
print("=" * 60)

# 작가별 통계 계산
authors = df['작가'].str.split('/').explode()
author_counts = authors.value_counts()

author_stats = []
for author in author_counts.index:
    author_works = df[df['작가'].str.contains(author, na=False)]
    
    # 기본 통계
    avg_rating = author_works['평점'].mean()
    work_count = len(author_works)
    genres = author_works['장르'].unique()
    
    # 가중치 계산
    weight = 0
    
    # 1. 작품 수 가중치 (작품 수가 많을수록 높은 순위)
    weight += work_count * 10
    
    # 2. 평점 오차 가중치 (평점 표준편차가 작을수록 높은 순위)
    if work_count > 1:
        rating_std = author_works['평점'].std()
        # 표준편차가 작을수록 높은 점수 (최대 10점)
        weight += max(0, 10 - rating_std * 2)
    
    # 3. 장르 다양성 가중치 (장르가 다를수록 높은 순위)
    if len(genres) > 1:
        weight += 20  # 장르가 2개 이상이면 20점 추가
    
    # 4. 감성 장르 제외 가중치 (감성이 아닌 장르가 있으면 높은 순위)
    if '감성' not in genres:
        weight += 15  # 감성이 없으면 15점 추가
    
    author_stats.append({
        '작가': author,
        '작품수': work_count,
        '평균평점': round(avg_rating, 2),
        '장르': ', '.join(genres),
        '가중점수': round(weight, 2)
    })

# DataFrame으로 변환하고 가중점수로 정렬
author_df = pd.DataFrame(author_stats)
author_df = author_df.sort_values('가중점수', ascending=False)

print(f"\n📊 전체 통계:")
print(f"   • 총 작가 수: {len(author_df)}명")
print(f"   • 평균 작품 수: {author_df['작품수'].mean():.1f}개")
print(f"   • 평균 평점: {author_df['평균평점'].mean():.2f}")

print(f"\n🏆 가중점수 상위 20명:")
print(author_df.head(20).to_string(index=False))

print(f"\n📈 가중점수 계산 기준:")
print(f"   • 작품 수 × 10점")
print(f"   • 평점 일관성: 최대 10점 (표준편차가 작을수록 높음)")
print(f"   • 장르 다양성: 20점 (2개 이상 장르)")
print(f"   • 감성 장르 제외: 15점")

print("\n" + "=" * 60) 