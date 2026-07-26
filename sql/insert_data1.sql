USE investment_portfolio;


-- 회원 데이터 삽입
INSERT INTO MEMBER (name, email, password, birth_date)
VALUES
('김루씨', 'lucykimlucy@naver.com', '1234', '2004-11-01'),
('김루아', 'luakim@naver.com', '2345', '2000-06-20'),
('김룰루', 'lulukim@naver.com', '3456', '1990-02-10');


-- 종목 데이터 삽입
INSERT INTO STOCK (stock_code, stock_name)
VALUES
('GOOGL', '알파벳 A'),
('AAPL', '애플'),
('000660', 'SK하이닉스'),
('005930', '삼성전자');


-- 거래 내역 데이터 삽입
INSERT INTO TRANSACTION_HISTORY
(member_id, stock_code, transaction_date, transaction_type, quantity, price)
VALUES
(1, 'GOOGL', '2026-03-17', 'buy', 1, 451433),
(1, 'AAPL', '2025-05-03', 'buy', 1, 371433),
(1, 'AAPL', '2026-06-01', 'sell', 1, 471433),
(2, '000660', '2026-04-28', 'buy', 3, 1333000),
(2, '000660', '2026-05-14', 'buy', 2, 1745000),
(2, '000660', '2026-06-17', 'sell', 3, 2521000),
(3, '005930', '2025-01-17', 'buy', 10, 51000),
(3, '005930', '2026-03-24', 'sell', 5, 61800),
(3, 'GOOGL', '2026-07-24', 'buy', 2, 467939);


-- 관심 종목 데이터 삽입
INSERT INTO WATCHLIST (member_id, stock_code)
VALUES
(1, 'GOOGL'),
(1, '000660'),
(2, '000660'),
(3, '000660');