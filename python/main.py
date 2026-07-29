from queries import (get_transaction_history, get_watchlist, get_invested_stocks, get_popular_stocks_by_age)

while True:
    print("==== 투자 포트폴리오 관리 시스템 ====")
    print("1. 거래 내역 조회")
    print("2. 관심 종목 조회")
    print("3. 현재 투자 중인 관심 종목 조회")
    print("4. 연령대별 인기 종목 조회")
    print("5. 종료")
    choice=input("메뉴를 선택하세요.:")

    if choice=="1":
        member_id=int(input("회원번호를 입력하세요.:"))
        result=get_transaction_history(member_id)
        print("========= 거래 내역 =========")
        for row in result:
            t_id,s_code, s_name, t_date, t_type, t_amount, t_price=row
            print(f"종목 코드: {s_code}")
            print(f"종목명: {s_name}")
            print(f"거래 날짜: {t_date}")
            print(f"거래 유형: {t_type}")
            print(f"거래 수량: {t_amount}")
            print(f"거래 가격(1주): {t_price}")
            print('-'*25)
            
    elif choice=="2":
        member_id=int(input("회원번호를 입력하세요.:"))
        result=get_watchlist(member_id)
        print("========= 관심 종목 =========")
        for row in result:
            w_id, s_code, s_name=row
            print(f"종목 코드: {s_code}")
            print(f"종목명: {s_name}")
            print('-'*25)

    elif choice=="3":
        member_id=int(input("회원번호를 입력하세요.:"))
        result=get_invested_stocks(member_id)
        print("===== 현재 투자 중인 관심 종목 =====")
        for row in result:
            s_code, s_name, nt_amount =row
            print(f"종목 코드: {s_code}")
            print(f"종목명: {s_name}")
            print(f"투자 수량: {nt_amount}")
            print('-'*25)

    elif choice=='4':
        result=get_popular_stocks_by_age()
        print("===== 연령대별 최다 관심 종목 =====")
        for row in result:
            a_range, s_code, s_name, a_num =row
            print(f"연령대: {a_range}")
            print(f"종목 코드: {s_code}")
            print(f"종목명: {s_name}")
            print(f"관심 인원: {a_num}")
            print('-'*25)

    elif choice=='5':
        print("프로그램을 종료합니다.")
        break

    else:
        print("잘못된 입력입니다.")
