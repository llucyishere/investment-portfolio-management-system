from db_connection import get_connection

# 특정 회원의 거래 내역 조회 함수 
def get_transaction_history(member_id):
    conn=get_connection()
    cursor=conn.cursor()

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

    result=cursor.fetchall()

    cursor.close()
    conn.close()

    return result

# 사용자의 현재 투자 현황 조회 
def get_current_holdings(member_id):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""SELECT a.stock_code, b.stock_name,
    SUM(
        CASE
            WHEN a.transaction_type='buy' THEN a.quantity
            ELSE -a.quantity
        END
    ) AS total_quantity
    FROM transaction_history a INNER JOIN stock b ON a.stock_code = b.stock_code
    WHERE member_id = %s
    GROUP BY a.stock_code, b.stock_name
    HAVING total_quantity > 0;""",(member_id,))

    result=cursor.fetchall()

    cursor.close()
    conn.close()

    return result 

# 특정 회원의 관심 종목 조회 
def get_watchlist(member_id):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(""" 
    select WATCHLIST.watchlist_id as '관심 목록 ID',
           WATCHLIST.stock_code as '종목 코드',
           STOCK.stock_name as '종목 이름'
    from WATCHLIST inner join STOCK
    on WATCHLIST.stock_code = STOCK.stock_code
    where member_id = %s
    order by WATCHLIST.watchlist_id;""",(member_id,)
    )

    result=cursor.fetchall()

    cursor.close()
    conn.close()

    return result

# 관심 종목 중 현재 투자 중인 종목 조회 
def get_invested_stocks(member_id):
    conn=get_connection()
    cursor=conn.cursor()

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

    result=cursor.fetchall()

    cursor.close()
    conn.close()

    return result

# 연령대별 최고 인기 종목 조회
def get_popular_stocks_by_age():
    conn=get_connection()
    cursor=conn.cursor()

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

    result=cursor.fetchall()

    cursor.close()
    conn.close()

    return result

# 사용자가 거래 내역을 입력 
def insert_transaction_history(member_id, stock_code, transaction_date, transaction_type, quantity, price):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    insert into TRANSACTION_HISTORY (member_id, stock_code, transaction_date, transaction_type, quantity, price)
    values (%s, %s, %s, %s, %s, %s);
    """,(member_id, stock_code, transaction_date, transaction_type, quantity, price))

    conn.commit()

    cursor.close()
    conn.close()

# 존재하는 종목인지 확인 
def check_stock(stock_code):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    select count(*) from STOCK where stock_code = %s;
    """,(stock_code,))

    result=cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0]>0

# 사용자의 입력을 받아 관심종목 추가하기 
def insert_watchlist(member_id, stock_code):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    insert into WATCHLIST (member_id, stock_code)
    values (%s, %s);
    """,(member_id, stock_code))

    conn.commit()

    cursor.close()
    conn.close()

# 이미 등록된 관심종목인지 확인 
def check_watchlist(member_id,stock_code):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""select count(*) from watchlist where stock_code=%s and member_id=%s""",(stock_code,member_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0]>0

# 거래 내역 삭제 
def delete_transaction_history(transaction_id):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    delete from TRANSACTION_HISTORY where transaction_id = %s;
    """,(transaction_id,))

    conn.commit()

    cursor.close()
    conn.close()

# 관심 종목 삭제 
def delete_watchlist(member_id, stock_code):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    delete from WATCHLIST where stock_code = %s and member_id = %s;
    """,(stock_code,member_id))

    conn.commit()

    cursor.close()
    conn.close()

# 회원 가입 
def register_member(name,email, password, birth_date):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""insert into MEMBER(name,email,password,birth_date)
    values(%s,%s,%s,%s);""",(name,email,password,birth_date))

    conn.commit()

    cursor.close()
    conn.close()

# 이미 가입한 회원인지 확인 
def check_member(email):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""select count(*) from MEMBER where email=%s;""",(email,))

    result=cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0]>0

# 로그인 함수 
def login(email, password):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""select member_id from MEMBER where email=%s and password=%s;""",(email,password))

    result=cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]
    else:
        return None

# 등록된 주식 목록 조회 
def view_stocks():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""select stock_code, stock_name from STOCK;""")

    result=cursor.fetchall()

    cursor.close()
    conn.close()

    return result

# 주식 등록 요청 저장 
def stock_request(member_id, stock_code, stock_name, request_date):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""INSERT INTO STOCK_REQUEST(member_id, stock_code, stock_name, request_date)
    values(%s, %s, %s, %s)""",(member_id, stock_code, stock_name, request_date))

    conn.commit()

    cursor.close()
    conn.close()

# 이미 등록 요청된 주식인지 확인 
def check_request(stock_code):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""select count(*) from stock_request where stock_code=%s;""",(stock_code,))

    result=cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0]>0

# 등록 요청 조회 
def show_request():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""select * from stock_request where status="대기";""")

    result=cursor.fetchall()

    cursor.close()
    conn.close()

    return result 

# 요청 등록 처리 
def confirm_request(request_id):
    conn=get_connection()
    cursor=conn.cursor()

    # 선택한 요청의 요청 내용 정보 가져옴 
    cursor.execute("""select stock_code, stock_name from stock_request where request_id=%s""",
                    (request_id,))
    stock=cursor.fetchone()
    # 가져온 요청 내용을 stock에 저장 
    cursor.execute("""insert into stock(stock_code, stock_name) values(%s, %s)""", 
                   stock)
    # 요청 처리 상태 업데이트 
    cursor.execute("""update stock_request set status=%s where request_id=%s""",("처리",request_id,))

    conn.commit()

    cursor.close()
    conn.close()