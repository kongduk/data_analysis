import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../webtoon.csv')

# 요일별 평균 평점 계산
day_avg_rating = df.groupby('요일')['평점'].mean().reindex([
    'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'
])

# 요일별 작품 수 계산
day_counts = df['요일'].value_counts().reindex([
    'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'
])
plt.figure(figsize=(10, 6))

# 요일별 평균 평점
plt.plot(day_avg_rating.index, day_avg_rating.values, marker='o', color='b', label='평균 평점')
plt.ylabel('평균 평점')
plt.xlabel('요일')
plt.title('요일별 평균 평점 및 작품 수')

# 요일별 작품 수
plt.twinx()
plt.bar(day_counts.index, day_counts.values, alpha=0.3, color='orange', label='작품 수')
plt.ylabel('작품 수')

plt.tight_layout()
plt.show() 