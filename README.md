# Investment Portfolio Management System

개인 투자 포트폴리오를 관리할 수 있는 웹 서비스입니다.

회원은 거래 내역과 관심 종목을 관리할 수 있으며,
관리자는 종목 등록 요청을 승인하여 종목을 추가할 수 있습니다.

또한 관심 종목과 사용자가 검색한 종목을 기반으로 관련 뉴스를 검색하고 추천하는 기능을 추가하여
포트폴리오 관리와 투자 정보 확인을 하나의 서비스에서 이용할 수 있도록 구성했습니다.

Python, MySQL, Streamlit을 활용하여 CLI 버전으로 기능을 먼저 구현한 뒤
웹 서비스 형태로 확장했습니다.

## 주요 기능

### 회원

- 회원가입
- 로그인 / 로그아웃

### 거래 내역

- 거래 내역 조회
- 거래 내역 등록
- 거래 내역 삭제

### 관심 종목

- 관심 종목 조회
- 관심 종목 등록
- 관심 종목 삭제

### 종목 관리

- 등록된 종목 조회
- 종목 등록 요청
- 관리자 승인 후 종목 등록

### 통계

- 연령대별 인기 종목 조회

### 뉴스

- 종목 관련 실시간 뉴스 검색
- 관심 종목 기반 뉴스 검색
- TF-IDF 기반 뉴스 관련도 계산
- 투자 관련 키워드 가산점을 활용한 뉴스 추천

## Tech Stack

### Backend
- Python
- MySQL
- mysql-connector-python

### Frontend
- Streamlit

### Data Processing

- pandas
- scikit-learn
- KoNLPy

### External API

- Naver News Search API

### Version Control
- Git
- GitHub

## Database

### Tables

- MEMBER
- STOCK
- TRANSACTION_HISTORY
- WATCHLIST
- STOCK_REQUEST

### ERD
![ERD](images/ERD.png)

## Project Structure

```text
investment-portfolio-management-system/
│
├── python/
│   ├── app.py
│   ├── db_connection.py
│   ├── main.py
│   ├── news.py
│   ├── queries.py
│   └── query_test.py
│
├── sql/
│   ├── create_tables.sql
│   ├── insert_data1.sql
│   └── select_queries.sql
│
└── README.md
```

## 실행 방법 
- 저장소 clone 

```bash
gh repo clone llucyishere/investment-portfolio-management-system
```

- 가상환경 생성 및 활성화 (선택)

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

macOS / Linux

```bash
source .venv/bin/activate
```

- 필요한 라이브러리 설치 

```bash
pip install -r requirements.txt
```
- Streamlit 실행 

```bash
streamlit run python/app.py
```

## 화면 예시 
- 기본 홈 화면 
![HOME](images/HOME.png)
- 로그인 후 홈 화면 
![HOME_LOGIN](images/HOME_LOGIN.png)

- 회원 가입 화면 
![REGISTER](images/REGISTER.png)
- 로그인 화면 
![LOGIN](images/LOGIN.png)

- 거래 내역 관련 화면(조회, 등록, 삭제) 
![VIEW_TRANSACTION](images/VIEW_TRANSACTION.png)
![ADD_TRANSACTION](images/ADD_TRANSACTION.png)
![DELETE_TRANSACTION](images/DELETE_TRANSACTION.png)

- 관심 종목 관련 화면(조회, 등록, 삭제) 
![VIEW_WATCHLIST](images/VIEW_WATCHLIST.png)
![ADD_WATCHLIST](images/ADD_WATCHLIST.png)
![DELETE_WATCHLIST](images/DELETE_WATCHLIST.png)

- 등록 요청 화면 
![REQUEST](images/REQUEST.png)
- 요청 관리 및 처리 화면 
![VIEW_REQUEST](images/VIEW_REQUEST.png)

## 프로젝트 특징

- Session State 활용 로그인 상태 관리
- 회원별 데이터 조회
- 관리자 권한 분리
- 종목 등록 요청 승인 프로세스
- SQL Window 함수 사용 연령대별 인기 종목 통계
- CLI 버전으로 기능을 먼저 구현한 후 Streamlit을 활용해 웹 UI로 확장
- Foreign Key 및 UNIQUE 제약조건을 활용한 데이터 무결성 관리
- 기존 뉴스 추천 프로젝트의 기능을 모듈화하여 현재 프로젝트에 재사용
- Naver News Search API를 활용한 실시간 종목 뉴스 검색
- Okt 형태소 분석과 TF-IDF를 활용한 뉴스 관련도 계산
- 투자 관련 키워드 가산점을 적용한 뉴스 추천

## 추후 개선 사항

- 비밀번호 암호화 적용
- 거래 내역 수정 기능 추가
- 종목 및 거래 내역 검색 기능 추가
- 주가 API 연동
- 투자 수익률 및 자산 통계 기능 추가
- 뉴스 본문을 활용한 뉴스 관련도 분석
- TF-IDF 기반 뉴스 추천을 임베딩 기반 의미 분석으로 고도화

## License

This project was created for educational purposes.

## 프로젝트 회고

데이터베이스 설계부터 SQL 구현, Python 연동, Streamlit을 활용한 웹 서비스 개발까지
하나의 프로젝트를 직접 구현하며 CRUD 기능과 사용자 인증,
관리자 권한 분리, 데이터 무결성 관리 과정을 경험할 수 있었습니다.

프로젝트를 진행하면서 기존에 별도로 개발했던 뉴스 추천 프로젝트의 기능을
현재 프로젝트에 통합하여 새로운 기능으로 확장하는 경험도 할 수 있었습니다.

향후에는 현재의 TF-IDF 기반 뉴스 추천 방식을 발전시켜
뉴스 본문과 임베딩 기반 의미 분석을 활용하고,
주가 데이터와 결합하여 실제 투자 판단에 도움이 될 수 있는
포트폴리오 관리 서비스로 확장해보고자 합니다.

## 프로젝트 발전 과정

### 1. CLI 기반 데이터베이스 기능 구현
- MySQL 데이터베이스 설계
- 회원, 종목, 거래 내역, 관심 종목 CRUD 구현
- Python과 MySQL 연동

### 2. Streamlit 기반 웹 서비스 확장
- 로그인 / 회원가입 구현
- Session State를 활용한 로그인 상태 관리
- 거래 내역 및 관심 종목 관리 UI 구현
- 관리자 종목 등록 요청 승인 기능 구현

### 3. 뉴스 추천 기능 통합
- 기존 뉴스 추천 프로젝트의 기능 재사용
- Naver News Search API 연동
- Okt 형태소 분석
- TF-IDF 기반 뉴스 관련도 계산
- 투자 관련 키워드 가산점 적용
- 홈 화면 및 관심 종목 조회 화면에 뉴스 검색 기능 추가
