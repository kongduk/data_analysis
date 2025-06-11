import requests
import pandas as pd
from datetime import datetime
import time
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# 장르 코드를 한국어로 변환하는 딕셔너리
GENRE_MAPPING = {
    'COMIC': '개그',
    'FANTASY': '판타지',
    'ACTION': '액션',
    'DRAMA': '드라마',
    'PURE': '순정',
    'SENSIBILITY': '감성',
    'THRILL': '스릴러',
    'HISTORICAL': '시대극',
    'SPORTS': '스포츠',
    'HUMOR': '유머',
    'ROMANCE': '로맨스',
    'DAILY': '일상',
    'SF': 'SF',
    'HORROR': '공포',
    'MYSTERY': '미스터리',
    'ADULT': '성인',
    'MARTIAL_ARTS': '무협',
    'SCHOOL': '학원',
    'ADVENTURE': '모험',
    'MUSIC': '음악',
    'COOKING': '요리',
    'MEDICAL': '의학',
    'MILITARY': '군사',
    'POLICE': '경찰',
    'POLITICS': '정치',
    'RELIGION': '종교',
    'SCIENCE': '과학',
    'TECHNOLOGY': '기술',
    'TRAVEL': '여행',
    'WAR': '전쟁',
    'WESTERN': '서부극',
    'ZOMBIE': '좀비'
}

def convert_genre_to_korean(genre_code):
    """영문 장르 코드를 한국어로 변환"""
    return GENRE_MAPPING.get(genre_code, genre_code)

def get_webtoon_info(webtoon, day, headers):
    try:
        # 웹툰 상세 정보 API URL
        title_id = webtoon.get('titleId', '')
        detail_api_url = f"https://comic.naver.com/api/article/list/info?titleId={title_id}"
        
        # API에서 상세 정보 가져오기
        detail_response = requests.get(detail_api_url, headers=headers)
        detail_response.raise_for_status()
        detail_data = detail_response.json()
        
        # 장르 정보 추출
        genres = []
        
        # 1. curationTagList에서 GENRE_COMIC 타입 찾기
        for tag in detail_data.get('curationTagList', []):
            if tag.get('curationType') == 'GENRE_COMIC':
                genres.append(tag.get('tagName', ''))
        
        # 2. gfpAdCustomParam에서 genreTypes 가져오기
        if 'gfpAdCustomParam' in detail_data:
            genre_types = detail_data['gfpAdCustomParam'].get('genreTypes', [])
            # 영문 장르 코드를 한국어로 변환
            korean_genres = [convert_genre_to_korean(genre) for genre in genre_types]
            genres.extend(korean_genres)
        
        # 중복 제거 및 정리
        genres = list(set(genres))
        genre_str = ', '.join(genres) if genres else ''
        
        webtoon_info = {
            '요일': day,
            '제목': webtoon.get('titleName', ''),
            '작가': webtoon.get('author', ''),
            '장르': genre_str,
            '평점': webtoon.get('starScore', '0.0'),
            '연령등급': detail_data.get('age', {}).get('description', ''),
            '태그': [tag['tagName'] for tag in detail_data.get('curationTagList', [])]
        }
        
        print(f"수집 완료: {webtoon_info['제목']} (장르: {webtoon_info['장르']})")
        return webtoon_info
        
    except Exception as e:
        print(f"웹툰 정보 처리 중 오류 발생: {e}")
        return None

def get_webtoon_list():
    print("크롤링을 시작합니다...")
    start_time = time.time()
    
    url = "https://comic.naver.com/api/webtoon/titlelist/weekday"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://comic.naver.com/webtoon/weekday",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        print("네이버 웹툰 API에 접속하는 중...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("API 접속 완료!")
        
        data = response.json()
        
        # 첫 번째 웹툰의 상세 정보 확인
        first_webtoon = next(iter(data.get('titleListMap', {}).values()))[0]
        title_id = first_webtoon.get('titleId', '')
        detail_api_url = f"https://comic.naver.com/api/article/list/info?titleId={title_id}"
        
        print(f"\n첫 번째 웹툰 상세 정보 확인 중: {detail_api_url}")
        detail_response = requests.get(detail_api_url, headers=headers)
        detail_response.raise_for_status()
        detail_data = detail_response.json()
        
        print("\n=== 웹툰 상세 정보 ===")
        print(json.dumps(detail_data, indent=2, ensure_ascii=False))
        
        # 모든 웹툰 정보 수집
        all_webtoons = []
        for day, webtoons in data.get('titleListMap', {}).items():
            for webtoon in webtoons:
                webtoon_info = get_webtoon_info(webtoon, day, headers)
                if webtoon_info:
                    all_webtoons.append(webtoon_info)
        
        # DataFrame 생성 및 저장
        df = pd.DataFrame(all_webtoons)
        filename = f"webtoon_genres_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n데이터가 {filename}에 저장되었습니다.")
        
        return df
        
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

if __name__ == "__main__":
    get_webtoon_list()