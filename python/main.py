from queries import (get_transaction_history, get_watchlist, get_invested_stocks, get_popular_stocks_by_age, insert_transaction_history, check_stock, insert_watchlist, delete_transaction_history, delete_watchlist)

while True:
    print("==== 투자 포트폴리오 관리 시스템 ====")
    print("1. 거래 내역 조회")
    print("2. 관심 종목 조회")
    print("3. 현재 투자 중인 관심 종목 조회")
    print("4. 연령대별 인기 종목 조회")
    print("5. 거래 내역 입력")
    print("6. 관심 종목 입력")
    print("7. 거래 내역 삭제")
    print("8. 관심 종목 삭제")
    print("9. 종료")
    choice=input("메뉴를 선택하세요.:")

    if choice=="1":
        member_id=int(input("회원번호를 입력하세요.:"))
        result=get_transaction_history(member_id)
        print("========= 거래 내역 =========")
        for i,row in enumerate(result,start=1):
            t_id,s_code, s_name, t_date, t_type, t_amount, t_price=row
            print(f"등록 순번: {i}")
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
        member_id=int(input("회원번호를 입력하세요.:"))
        stock_code=input("종목 코드를 입력하세요.:")
        if not check_stock(stock_code):
            print("존재하지 않는 종목입니다. 다시 입력하거나 등록 신청을 해주세요.")
            continue
        transaction_date=input("거래 날짜를 입력하세요.(YYYY-MM-DD):")
        transaction_type=input("거래 유형을 입력하세요.(buy/sell):")
        quantity=int(input("거래 수량을 입력하세요.:"))
        price=int(input("거래 가격(1주)을 입력하세요.:"))
        insert_transaction_history(member_id, stock_code, transaction_date, transaction_type, quantity, price)
        print("거래 내역이 성공적으로 입력되었습니다.")

    elif choice=='6':
        member_id=int(input("회원번호를 입력하세요.:"))
        stock_code=input("관심 종목 코드를 입력하세요.:")
        if not check_stock(stock_code):
            print("존재하지 않는 종목입니다. 다시 입력하거나 등록 신청을 해주세요.")
            continue
        insert_watchlist(member_id, stock_code)
        print("관심 종목이 성공적으로 추가되었습니다.")

    elif choice=='7':
        member_id=int(input("회원번호를 입력하세요.:"))
        delete_id = int(input("삭제할 거래 ID를 입력하세요: "))
        result=get_transaction_history(member_id)
        transaction_id=result[delete_id-1][0]

        delete_transaction_history(transaction_id)
        print("거래 내역이 성공적으로 삭제되었습니다.")

    elif choice=='8':
        member_id=int(input("회원번호를 입력하세요.:"))
        delete_code = input("삭제할 관심 종목 코드를 입력하세요: ")

        delete_watchlist(member_id,delete_code)
        print("관심 종목이 성공적으로 삭제되었습니다.")
        

    elif choice=='9':
        print("프로그램을 종료합니다.")
        break

    else:
        print("잘못된 입력입니다.")
