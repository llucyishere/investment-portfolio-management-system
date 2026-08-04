# DB 연결을 설정 
from db_connection import get_connection 
conn = get_connection()

# SQL문 전달하고 결과 받아올 객체 생성 
cursor = conn.cursor()

# 현재 로그인 한 회원의 member_id를 받아서 쿼리에 적용(추후 수정 예정)
member_id=1

# SQL문 작성 및 실행 
# 전체 회원 조회 
cursor.execute("SELECT * FROM MEMBER")
# 결과 가져오기(한 행 내용을 원소로 가지는 배열 형태)
result = cursor.fetchall()
# 반복문으로 배열을 순회하면서 한 줄씩 데이터 출력 
for row in result:
     print(row)

# 특정 회원의 거래 내역 조회 
cursor.execute(""" 
     select TRANSACTION_HISTORY.transaction_id as '거래 ID', 
            TRANSACTION_HISTORY.stock_code as '종목 코드', 
            STOCK.stock_name as '종목 이름', 
            TRANSACTION_HISTORY.transaction_date as '거래 날짜', 
            TRANSACTION_HISTORY.transaction_type as '거래 유형', 
            TRANSACTION_HISTORY.quantity as '수량', 
            TRANSACTION_HISTORY.price as '가격'
     from TRANSACTION_HISTORY inner join STOCK 
     on TRANSACTION_HISTORY.stock_code = STOCK.stock_code
     where member_id = %s
     order by TRANSACTION_HISTORY.transaction_date;
     """,(member_id,))
# 결과 가져오기(한 행 내용을 원소로 가지는 배열 형태)
result = cursor.fetchall()
# 반복문으로 배열을 순회하면서 한 줄씩 데이터 출력 
for row in result:
     print(row)

# 특정 회원의 관심 종목 조회 
cursor.execute("""
 select WATCHLIST.watchlist_id as '관심 목록 ID',
        WATCHLIST.stock_code as '종목 코드',
        STOCK.stock_name as '종목 이름'
 from WATCHLIST inner join STOCK
 on WATCHLIST.stock_code = STOCK.stock_code
 where member_id = %s
 order by WATCHLIST.watchlist_id;
 """,(member_id,))
# 결과 가져오기(한 행 내용을 원소로 가지는 배열 형태)
result = cursor.fetchall()
# 반복문으로 배열을 순회하면서 한 줄씩 데이터 출력 
for row in result:
     print(row)

# 관심 종목 중 현재 투자 중인 종목 조회 
cursor.execute("""
 select t.stock_code as '종목 코드',
        s.stock_name as '종목 이름',
        sum(case when transaction_type = 'buy' then quantity else -quantity end) as '보유 수량'
 from transaction_history t inner join stock s
 on t.stock_code = s.stock_code
 where t.member_id = %s and t.stock_code in (select stock_code from WATCHLIST where member_id = %s)
 group by t.stock_code
 having sum(case when transaction_type = 'buy' then quantity else -quantity end) > 0
 order by t.stock_code;
 """,(member_id,member_id))
# 결과 가져오기(한 행 내용을 원소로 가지는 배열 형태)
result = cursor.fetchall()
# 반복문으로 배열을 순회하면서 한 줄씩 데이터 출력 
for row in result:
     print(row)

# 연령대별 최고 인기 관심 종목 조회 
cursor.execute("""
 SELECT `연령대`, stock_code as '종목 코드', stock_name as '종목 이름', `관심 회원 수`
 FROM
 (SELECT 
     FLOOR(TIMESTAMPDIFF(YEAR, m.birth_date, CURDATE()) / 10) * 10 AS '연령대',
     s.stock_code, 
     s.stock_name, 
     COUNT(w.member_id) AS '관심 회원 수',
     RANK() OVER (PARTITION BY FLOOR(TIMESTAMPDIFF(YEAR, m.birth_date, CURDATE()) / 10) * 10 ORDER BY COUNT(*) DESC) as ranking
 FROM WATCHLIST w
 INNER JOIN STOCK s
     ON w.stock_code = s.stock_code
 INNER JOIN MEMBER m
     ON w.member_id = m.member_id
 GROUP BY 
     FLOOR(TIMESTAMPDIFF(YEAR, m.birth_date, CURDATE()) / 10) * 10,
     s.stock_code) s
 where ranking=1
 order by `연령대`;  
 """)
# 결과 가져오기(한 행 내용을 원소로 가지는 배열 형태)
result = cursor.fetchall()
# 반복문으로 배열을 순회하면서 한 줄씩 데이터 출력 
for row in result:
     print(row)

# 사용자의 입력을 받아 거래 내역 추가 
transaction_id = input("거래 ID를 입력하세요: ")
stock_code = input("종목 코드를 입력하세요: ")
transaction_date = input("거래 날짜를 입력하세요 (YYYY-MM-DD): ")
transaction_type = input("거래 유형을 입력하세요 (buy/sell): ")
quantity = int(input("거래 수량을 입력하세요: "))
price = float(input("거래 가격을 입력하세요: "))

cursor.execute("""
    insert into TRANSACTION_HISTORY (member_id, stock_code, transaction_date, transaction_type, quantity, price)
    values (%s, %s, %s, %s, %s, %s);
    """,(member_id, stock_code, transaction_date, transaction_type, quantity, price))
conn.commit()

# 사용자의 입력을 받아 관심종목 추가하기 
stock_code=input("관심 종목 코드를 입력하세요: ")

cursor.execute("""
    insert into WATCHLIST (member_id, stock_code)
    values (%s, %s);
    """,(member_id, stock_code))
conn.commit()

# 사용자가 선택한 거래 내역 삭제하기
delete_id = input("삭제할 거래 ID를 입력하세요: ")
member_id=int(input("회원번호를 입력하세요.:"))
result=get_transaction_history(member_id)
transaction_id=result[delete_id-1][0]

cursor.execute("""
    delete from TRANSACTION_HISTORY where transaction_id = %s;
    """,(transaction_id,))

conn.commit()

# 사용자가 선택한 관심 종목 삭제하기 
delete_code = input("삭제할 관심 종목 코드를 입력하세요: ")
member_id=int(input("회원번호를 입력하세요.:"))

cursor.execute("""
    delete from WATCHLIST where stock_code = %s and member_id = %s;
    """,(delete_code,member_id))

cursor.close()
conn.close()

from queries import get_transaction_history

member_id=1
result=get_transaction_history(member_id)
for rows in result:
    print(rows)


