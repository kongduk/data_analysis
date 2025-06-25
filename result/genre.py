import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../webtoon.csv')

# 평균 평점
genre_avg_rating = df.groupby('장르')['평점'].mean().sort_values(ascending=False)
# 작품 수
genre_counts = df['장르'].value_counts()
plt.figure(figsize=(12, 6))

# 장르별 평균 평점
plt.plot(genre_avg_rating.index, genre_avg_rating.values, marker='o', color='b', label='평균 평점')
plt.ylabel('평균 평점')
plt.xlabel('장르')
plt.title('장르별 평균 평점 및 작품 수')

# 장르별 작품 수 
plt.twinx()
plt.bar(genre_counts.index, genre_counts.values, alpha=0.3, color='orange', label='작품 수')
plt.ylabel('작품 수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

genre_stats = df.groupby('장르').agg({
    '제목': 'count',
    '평점': 'mean'
}).round(2)
genre_stats.columns = ['작품수', '평균평점']
genre_stats = genre_stats.sort_values('평균평점', ascending=False)
print(genre_stats)
