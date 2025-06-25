import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../webtoon.csv')

print("=" * 60)
print("👨‍🎨 작가별 가중 평점 분석")
print("=" * 60)

all_authors = []
for authors_str in df['작가']:
    if pd.notna(authors_str):
        authors = [author.strip() for author in authors_str.split('/')]
        all_authors.extend(authors)

# 작가별 작품 수 계산
author_counts = pd.Series(all_authors).value_counts()

author_stats = []
for author in author_counts.index:
    # 해당 작가가 정확히 포함된 모든 웹툰 찾기
    author_works = df[df['작가'].apply(lambda x: author in [a.strip() for a in x.split('/')] if pd.notna(x) else False)]
    
    avg_rating = author_works['평점'].mean()
    work_count = len(author_works)
    genres = author_works['장르'].unique()
    
    # 가중치 계산
    weight = 0
    
    # 1. 평균 평점 가중치
    weight += avg_rating * 5
    
    # 2. 작품 수 가중치
    weight += work_count * 5
    
    # 3. 평점 오차 가중치 (평점 표준편차가 작을수록 높은 순위)
    if work_count > 1:
        rating_std = author_works['평점'].std()
        weight += max(0, 10 - rating_std * 2) * (work_count) * 0.05
    
    # 4. 장르 다양성 가중치 (장르가 다를수록 높은 순위)
    if len(genres) > 1:
        weight += 5 * len(genres)
    
    # 5. 감성 장르 제외 가중치 (감성이 아닌 장르가 있으면 높은 순위)
    if '감성' not in genres:
        weight += 5  # 감성이 없으면 5점 추가
    
    author_stats.append({
        '작가': author,
        '작품수': work_count,
        '평균평점': round(avg_rating, 2),
        '장르': ', '.join(genres),
        '가중점수': round(weight, 2)
    })

author_df = pd.DataFrame(author_stats)
author_df = author_df.sort_values('가중점수', ascending=False)

plt.figure(figsize=(12, 8))

top_10 = author_df.head(10)
plt.bar(range(len(top_10)), top_10['가중점수'], color='skyblue', alpha=0.7)
plt.xlabel('작가')
plt.ylabel('가중점수')
plt.title('작가별 가중점수 상위 10명')
plt.xticks(range(len(top_10)), top_10['작가'], rotation=45, ha='right')

# 가중점수 값 표시
for i, v in enumerate(top_10['가중점수']):
    plt.text(i, v + 1, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()