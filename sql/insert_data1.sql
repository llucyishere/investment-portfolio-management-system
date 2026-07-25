USE investment_portfolio;


-- 회원 데이터 삽입
INSERT INTO MEMBER (name, email, password, birth_date)
VALUES
('김루씨', 'lucykimlucy@naver.com', '1234', '2004-11-01'),
('김루아', 'luakim@naver.com', '2345', '2000-06-20'),
('김룰루', 'lulukim@naver.com', '3456', '1990-02-10');


-- 종목 데이터 삽입
INSERT INTO STOCK (stock_code, stock_na