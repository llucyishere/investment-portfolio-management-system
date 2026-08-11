import requests  # URL 요청 처리
from dotenv import load_dotenv  # .env 파일 불러오기
import os  # 운영체제와 소통
import re  # 정규표현식
import html  # 특수문자 제거
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# .env 파일 불러오기
load_dotenv()

# 네이버 API 인증 정보
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

url = "https://openapi.naver.com/v1/search/news.json"

headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}


# 뉴스 제목에 있는 HTML 태그와 특수문자 제거를 위한 함수 
def clean_text(text):
    text = html.unescape(re.sub('<[^>]+>', "", text))
    return text


# 형태소 분석기
okt = Okt()

# TF-IDF 계산기
vectorizer = TfidfVectorizer()


# 공통 투자 관련 키워드
investment_keywords = [
    "주가","급등","급락","상승","하락","투자",
    "실적","매출","영업이익","순이익","전망",
    "목표주가","증권사","수주","계약","배당","자사주",
    "외국인","기관",
    "거래량","상장","유상증자","무상증자"
]

def get_recommended_news(stock):
    # 네이버 뉴스 검색 조건
    params = {
            "query": stock,
            "display": 20,
            "start": 1,
            "sort": "date"
    }

    # url에 네이버 뉴스 API 요청
    response = requests.get(
            url,
            headers=headers,
            params=params
        )

    # 받아온 결과를 JSON 데이터로 변환
    data = response.json()


    # 뉴스 제목 전처리
    title_nouns = []

    for item in data["items"]:

        title = clean_text(item["title"])

        # 뉴스 제목에서 명사들을 추출해 하나로 합침 
        get_nouns = " ".join(okt.nouns(title))
        # 뉴스 제목별로 하나의 명사 구절을 리스트에 저장 
        title_nouns.append(get_nouns)


    # 검색어에서 명사 추출 
    query_nouns = " ".join(okt.nouns(stock))


    # 검색어 + 뉴스 제목
    corpus = [query_nouns] + title_nouns

    # TF-IDF 계산
    tfidf_matrix = vectorizer.fit_transform(corpus)
    # 검색어 명사와 뉴스 제목 명사들 간의 점수 계산 
    scores = cosine_similarity(
            tfidf_matrix[0],
            tfidf_matrix[1:]
        )
    # 결과가 2차원 배열이기 때문 
    scores = scores[0]

    # 관련 뉴스 기준
    threshold = 0.4

    # 최종 결과를 저장할 리스트
    results = []

    # 최종 점수 계산
    for item, score in zip(data["items"], scores):

        title = clean_text(item["title"])
        link = item["link"]

        # 투자 관련 키워드 점수
        keyword_score = 0

        for keyword in investment_keywords:
            if keyword in title:
                keyword_score += 0.05

        # 최종 점수
        final_score = score + keyword_score

        # threshold 이상인 뉴스만 저장
        if final_score > threshold:
            results.append(
                (title,link,final_score,keyword_score)
            )

    # 최종 점수가 높은 순서대로 정렬
    # 최종 점수가 같으면 키워드 점수가 높은 것부터 
    results.sort(
        key=lambda x: (x[2],x[3]),
        reverse=True
    )

    return results