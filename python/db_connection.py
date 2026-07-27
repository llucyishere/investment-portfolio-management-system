import mysql.connector # mysql과 python을 연결하는 클래스 
from dotenv import load_dotenv
import os # 환경변수 불러오기 위함 

# .env 파일의 환경변수 불러오기 
load_dotenv()

# MySQL 연결 설정
def get_connection():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'), # mysql 서버 주소
        user=os.getenv('DB_USER'), # mysql 계정
        password=os.getenv('DB_PASSWORD'), # mysql 계정 비밀번호
        database=os.getenv('DB_NAME') # 연결할 데이터베이스 이름
    )
    return conn
