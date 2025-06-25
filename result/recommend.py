import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../webtoon.csv')

genre_recommendations = {}

for genre in df['장르'].unique():
    if pd.isna(genre) or genre == '':
        continue
    
    genre_webtoons = df[df['장르'] == genre]
    
    if len(genre_webtoons) == 0:
        continue
    
    # 추천 점수 계산
    recommendations = []
    for _, webtoon in genre_webtoons.iterrows():
        # 기본 점수: 해당 웹툰의 평점 × 10
        score = float(webtoon['평점']) * 10
        
        # 해당 작가의 모든 웹툰 찾기
        author = webtoon['작가']
        author_works = df[df['작가'].str.contains(author, na=False)]
        author_count = len(author_works)
        
        # 최대 20점까지 (작품 수 × 2, 최대 3개 작품까지)
        if author_count > 1:
            score += min(author_count * 2, 6)
        
        # 작가가 여러 장르를 다룬다면 가중치
        author_genres = set()
        for _, work in author_works.iterrows():
            if pd.notna(work['장르']):
                author_genres.update(work['장르'].split(', '))
        
        # 작가가 2개 이상의 장르를 다룬다면 가중치
        if len(author_genres) > 1:
            score += 10
        
        recommendations.append({
            '제목': webtoon['제목'],
            '작가': webtoon['작가'],
            '평점': webtoon['평점'],
            '요일': webtoon['요일'],
            '추천점수': round(score, 2)
        })
    
    recommendations.sort(key=lambda x: x['추천점수'], reverse=True)
    
    if recommendations:
        genre_recommendations[genre] = recommendations[0]

all_recommendations = []
for genre, rec in genre_recommendations.items():
    rec['장르'] = genre
    all_recommendations.append(rec)

all_recommendations.sort(key=lambda x: x['추천점수'], reverse=True)

plt.figure(figsize=(16, 10))

top = all_recommendations[:10]
genres = [rec['장르'] for rec in top]
titles = [rec['제목'] for rec in top]
scores = [rec['추천점수'] for rec in top]

bars = plt.bar(range(len(genres)), scores, color='lightcoral', alpha=0.7)

colors = ['lightcoral', 'lightblue', 'lightgreen', 'lightyellow', 'lightpink', 
          'lightgray', 'lightcyan', 'lightsteelblue', 'lightseagreen', 'lightsalmon']

for i, (bar, genre) in enumerate(zip(bars, genres)):
    color_idx = i % len(colors)
    bar.set_color(colors[color_idx])

for i, (bar, score, title) in enumerate(zip(bars, scores, titles)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{score:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, 
             title, ha='center', va='center', fontsize=8, 
             rotation=90, color='black', fontweight='bold')

plt.xlabel('장르')
plt.ylabel('추천점수')
plt.title('장르별 추천 웹툰')
plt.xticks(range(len(genres)), genres, rotation=45, ha='right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()