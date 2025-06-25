import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 로딩
df = pd.read_csv('webtoon.csv')

# 작가 컬럼을 '/' 기준으로 분리하고 각 작가별로 작품 수 계산
authors = df['작가'].str.split('/').explode()
author_counts = authors.value_counts()

# 작가별 평균 평점과 관심도 계산
author_ratings = []
for author in author_counts.index:
    # 해당 작가가 포함된 모든 웹툰의 평점과 관심도 평균 계산
    author_works = df[df['작가'].str.contains(author, na=False)]
    avg_rating = author_works['평점'].mean()
    avg_interest = author_works['관심'].mean()
    author_ratings.append({
        '작가': author,
        '작품수': author_counts[author],
        '평균평점': round(avg_rating, 2),
        '평균관심': round(avg_interest, 2)
    })

# DataFrame으로 변환
author_stats = pd.DataFrame(author_ratings)
author_stats = author_stats.sort_values('평균평점', ascending=False)

# 결과 출력
print("\n작가별 통계:")
print(author_stats)

# 그래프로 시각화 (평점과 관심도)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# 평균 평점 그래프
ax1.bar(author_stats['작가'], author_stats['평균평점'])
ax1.set_title('작가별 평균 평점')
ax1.set_xlabel('작가')
ax1.set_ylabel('평균 평점')
ax1.tick_params(axis='x', rotation=45)

# 평균 관심도 그래프
ax2.bar(author_stats['작가'], author_stats['평균관심'])
ax2.set_title('작가별 평균 관심도')
ax2.set_xlabel('작가')
ax2.set_ylabel('평균 관심도')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
