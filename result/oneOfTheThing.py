import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../webtoon.csv')

lico_works = df[df['작가'].str.contains('LICO', na=False)]

plt.figure(figsize=(14, 8))

titles = lico_works['제목'].tolist()
ratings = lico_works['평점'].tolist()

bars = plt.bar(range(len(titles)), ratings, color='skyblue', alpha=0.7)

avg_rating = lico_works['평점'].mean()
plt.axhline(y=avg_rating, color='red', linestyle='--', alpha=0.8, label=f'평균 평점: {avg_rating:.3f}')

for i, (bar, rating) in enumerate(zip(bars, ratings)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, 
             f'{rating:.3f}', ha='center', va='bottom', fontsize=9)

plt.xlabel('작품')
plt.ylabel('평점')
plt.title('LICO 작가 작품별 평점')
plt.xticks(range(len(titles)), titles, rotation=45, ha='right', fontsize=10)
plt.ylim(9.7, 10.0)  # 평점 범위 조정
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n" + "=" * 60) 