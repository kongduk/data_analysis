import requests
import pandas as pd
from datetime import datetime
import time
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def get_webtoon_info(webtoon, day, headers):
    try:
        # 웹툰 상세 페이지 URL
        title_id = webtoon.get('titleId', '')
        detail_url = f"https://comic.naver.com/webtoon/list?titleId={title_id}"
        
        # 상세 페이지에서 장르 정보 가져오기
        detail_response = requests.get(detail_url, headers=headers)
        detail_response.raise_for_status()
        soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        # 장르 태그 찾기 (span.genre 클래스 사용)
        genre_span = soup.find('span', {'class': 'genre'})
        genre = genre_span.text.strip() if genre_span else ''
        
        webtoon_info = {
            '요일': day,
            '제목': webtoon.get('titleName', ''),
            '작가': webtoon.get('author', ''),
            '장르': genre,
            '평점': webtoon.get('starScore', '0.0')
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
        
        # 첫 번째 웹툰의 상세 페이지 확인
        first_webtoon = next(iter(data.get('titleListMap', {}).values()))[0]
        title_id = first_webtoon.get('titleId', '')
        detail_url = f"https://comic.naver.com/webtoon/list?titleId={title_id}"
        
        print(f"\n첫 번째 웹툰 상세 페이지 확인 중: {detail_url}")
        detail_response = requests.get(detail_url, headers=headers)
        detail_response.raise_for_status()
        
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        # 장르 관련 태그 찾기
        print("\n=== 장르 관련 태그 찾기 ===")
        
        # 1. span.genre 태그 찾기
        genre_span = soup.find('span', {'class': 'genre'})
        print("\n1. span.genre 태그:")
        print(genre_span)
        
        # 2. div.detail 태그 찾기
        detail_div = soup.find('div', {'class': 'detail'})
        print("\n2. div.detail 태그:")
        print(detail_div)
        
        # 3. 모든 span 태그 찾기
        print("\n3. 모든 span 태그:")
        for span in soup.find_all('span'):
            print(f"클래스: {span.get('class', '')}, 텍스트: {span.text.strip()}")
        
        # 4. 모든 div 태그 찾기
        print("\n4. 모든 div 태그:")
        for div in soup.find_all('div'):
            print(f"클래스: {div.get('class', '')}, ID: {div.get('id', '')}")
        
        return None
        
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

if __name__ == "__main__":
    get_webtoon_list()