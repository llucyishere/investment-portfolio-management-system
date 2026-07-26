-- 회원 전체 조회 
select * 
from MEMBER;

-- 특정 회원의 거래 내역 조회 
-- python과 연동해 현재 로그인 한 회원의 member_id를 불러와 where절 조건에 연결 
-- 사용자가 정렬 기준(날짜순, 거래순)을 선택해 order by절에 연결 
select TRANSACTION_HISTORY.transaction_id as '거래 ID', 
       TRANSACTION_HISTORY.stock_code as '종목 코드', 
       STOCK.stock_name as '종목 이름', 
       TRANSACTION_HISTORY.transaction_date as '거래 날짜', 
       TRANSACTION_HISTORY.transaction_type as '거래 유형', 
       TRANSACTION_HISTORY.quantity as '수량', 
       TRANSACTION_HISTORY.price as '가격'
from TRANSACTION_HISTORY inner join STOCK 
on TRANSACTION_HISTORY.stock_code = STOCK.stock_code
where member_id = 1
order by TRANSACTION_HISTORY.transaction_date;

-- 특정 회원의 관심 종목 조회 
-- python과 연동해 현재 로그인 한 회원의 member_id를 불러와 where절 조건에 연결 
-- 사용자가 정렬 기준(추가순, 종목코드순, 종목이름순)을 선택해 order by절에 연결 
select WATCHLIST.watchlist_id as '관심 목록 ID',
       WATCHLIST.stock_code as '종목 코드',
       STOCK.stock_name as '종목 이름'
from WATCHLIST inner join STOCK
on WATCHLIST.stock_code = STOCK.stock_code
where member_id = 1
order by WATCHLIST.watchlist_id;

-- 관심 종목 중 실제 투자 중인 종목 조회 
-- python과 연동해 현재 로그인 한 회원의 member_id를 불러와 where절 조건에 연결
-- 사용자가 정렬 기준(종목코드순, 종목이름순, 보유수량순)을 선택해 order by절에 연결
-- 상단에 총 보유 종목 수 조회 기능 추가 
select t.stock_code as '종목 코드',
       s.stock_name as '종목 이름',
       sum(case when transaction_type = 'buy' then quantity else -quantity end) as '보유 수량'
from transaction_history t inner join stock s
on t.stock_code = s.stock_code
where t.member_id = 1 and t.stock_code in (select stock_code from WATCHLIST where member_id = 1)
group by t.stock_code
having sum(case when transaction_type = 'buy' then quantity else -quantity end) > 0
order by t.stock_code;

-- 연령대별 인기 관심 종목 조회 
-- 회원의 연령대에 맞는 종목에 색상을 달리하는 UI 추가 
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

