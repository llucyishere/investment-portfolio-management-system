from queries import (login, register_member, check_member
                     ,get_transaction_history, insert_transaction_history, delete_transaction_history
                     ,get_watchlist, insert_watchlist, delete_watchlist, check_stock, check_watchlist
                     ,get_popular_stocks_by_age, view_stocks 
                     ,stock_request, check_request, show_request, confirm_request)
from datetime import date 
import streamlit as st
import pandas as pd

# 초기 상태 설정 
if "member_id" not in st.session_state:
    st.session_state.member_id = None

if "page" not in st.session_state:
    st.session_state.page = "home"

if "email" not in st.session_state:
    st.session_state.email = None


# 사이드바 메뉴 
# 메인으로 돌아가기 
if st.sidebar.button("홈으로"):
    st.session_state.page="home"
# 종목 등록 요청 
if st.sidebar.button("종목 등록 요청하기"):
    st.session_state.page="request_stock"
# 관리자 페이지 
if st.session_state.email=="admin@email.com":
    if st.sidebar.button("등록 요청 관리"):
        st.session_state.page = "request_manage"
# 회원 관리 
st.sidebar.header("회원 관리")
if st.session_state.member_id:
    st.sidebar.write(f"{st.session_state.email}님, 환영합니다!")
    if st.sidebar.button("로그아웃"):
        st.session_state.member_id = None
        st.session_state.email = None
        st.session_state.page = "home"
        st.rerun()
else:
    if st.sidebar.button("회원 가입"):
        st.session_state.page = "register_member"
    if st.sidebar.button("로그인"):
        st.session_state.page = "login"
# 거래 내역 관리 
st.sidebar.header("거래 내역 관리")
if st.sidebar.button("거래 내역 조회"):
    st.session_state.page = "transaction_history"
if st.sidebar.button("거래 내역 입력"):
    st.session_state.page = "insert_transaction_history"
if st.sidebar.button("거래 내역 삭제"):
    st.session_state.page = "delete_transaction_history"
# 관심 종목 관리 
st.sidebar.header("관심 종목 관리")
if st.sidebar.button("관심 종목 조회"):
    st.session_state.page = "watchlist"
if st.sidebar.button("관심 종목 입력"):
    st.session_state.page = "insert_watchlist"
if st.sidebar.button("관심 종목 삭제"):
    st.session_state.page = "delete_watchlist"


# 각 메뉴별 페이지 구현 
page = st.session_state.get("page", "home")
# 기본 시작 화면 
if page=="home":
    if st.session_state.member_id:
        st.title(f"{st.session_state.email}님, 환영합니다!")
        st.write("연령대별 최다 인기 종목 현황")
        result=get_popular_stocks_by_age()
        df=pd.DataFrame(result,
                        columns=["연령대","종목 코드","종목명","관심 인원 수"]
                            )
        st.dataframe(df)
    else:
        st.title("주렁주렁")
        st.write("개인 투자 포트폴리오 관리 웹 서비스입니다. 로그인 후 기능들을 이용할 수 있습니다.")
# 회원 가입 화면 
if page=="register_member":
    st.title("회원 가입")
    name = st.text_input("이름:")
    email = st.text_input("이메일:")
    password = st.text_input("비밀번호:", type="password")
    birth_date = st.date_input("생년월일:", value=date(1900, 1, 1), min_value=date(1900,1,1), max_value=date.today())
    if st.button("회원 가입하기"):
        if check_member(email):
            st.error("이미 가입된 회원입니다.")
        else:
            register_member(name, email, password, birth_date)
            st.success("회원 가입이 완료되었습니다. 로그인하세요.")

# 로그인 화면 
if page=="login":
    st.title("로그인")
    email = st.text_input("이메일:")
    password = st.text_input("비밀번호:", type="password")
    if st.button("로그인하기"):
        member_id = login(email, password)
        if member_id:
            st.session_state.member_id = member_id
            st.session_state.email = email 
            st.success("로그인 되었습니다.")
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("잘못된 정보입니다. 신규 회원은 회원가입을 진행하세요.")

# 거래 내역 조회 화면 
if page=="transaction_history":
    if st.session_state.member_id is None:
        st.error("로그인이 필요합니다.")
    else:
        st.title("거래 내역 조회")
        result=get_transaction_history(st.session_state.member_id)
        if result:
            df=pd.DataFrame(result,
                            columns=["거래 ID","종목 코드","종목명","거래 날짜","거래 유형","거래 수량","거래 가격(1주)"
                                ])
            # transaction_id 컬럼은 제거하고 등록 순번 컬럼을 추가
            df=df.drop(columns=["거래 ID"])
            df.insert(0,"등록 순번",range(1,len(df)+1))
            df["거래 가격(1주)"]=df["거래 가격(1주)"].apply(lambda x: f"{x:,}")

            st.dataframe(df)
        else:
            st.write("저장된 거래 내역이 없습니다.")

# 거래 내역 입력 화면 
if page=="insert_transaction_history":
    if st.session_state.member_id is None:
        st.error("로그인이 필요합니다.")
    else:
        st.title("거래 내역 입력")

        st.write("입력 가능한 종목(없는 종목은 등록 신청을 먼저 해주세요.)")
        result=view_stocks()
        df=pd.DataFrame(result,
                        columns=["종목 코드","종목명"]
                            )
        st.dataframe(df)

        stock_code = st.text_input("종목 코드:")
        transaction_date = st.date_input("거래 날짜:", value=date.today(), min_value=date(1900,1,1), max_value=date.today())
        transaction_type = st.selectbox("거래 유형:", ["buy", "sell"])
        quantity = st.number_input("거래 수량:", min_value=1, step=1)
        price = st.number_input("거래 가격(1주):", min_value=1, step=1)

        if st.button("입력하기"):
            insert_transaction_history(st.session_state.member_id, stock_code, transaction_date, transaction_type, quantity, price)
            st.success("거래 내역이 성공적으로 입력되었습니다.")

# 거래 내역 삭제 화면 
if page=="delete_transaction_history":
    if st.session_state.member_id is None:
        st.error("로그인이 필요합니다.")
    else:
        st.title("거래 내역 삭제")
        st.write("등록된 거래 내역")
        result=get_transaction_history(st.session_state.member_id)
        if result:
            df=pd.DataFrame(result,
                            columns=["거래 ID","종목 코드","종목명","거래 날짜","거래 유형","거래 수량","거래 가격(1주)"
                                ])
            # transaction_id 컬럼은 제거하고 등록 순번 컬럼을 추가
            df=df.drop(columns=["거래 ID"])
            df.insert(0,"등록 순번",range(1,len(df)+1))
            df["거래 가격(1주)"]=df["거래 가격(1주)"].apply(lambda x: f"{x:,}")

            st.dataframe(df)

            delete_id = st.number_input("삭제할 거래 등록 순번을 입력하세요:", min_value=1, max_value=len(df), step=1)
            if st.button("삭제하기"):
                transaction_id=result[delete_id-1][0]
                delete_transaction_history(transaction_id)
                st.success("거래 내역이 성공적으로 삭제되었습니다.")
                st.session_state.page = "delete_transaction_history"
                st.rerun()
        else:
            st.write("저장된 거래 내역이 없습니다.")

# 관심 종목 조회 화면 
if page=="watchlist":
    if st.session_state.member_id is None:
        st.error("로그인이 필요합니다.")
    else:
        st.title("관심 종목 조회")
        result=get_watchlist(st.session_state.member_id)
        if result:
            df=pd.DataFrame(result,
                            columns=["관심 목록 ID","종목 코드","종목명"]
                                )
            df=df.drop(columns=["관심 목록 ID"])
            df.insert(0,"등록 순번",range(1,len(df)+1))
            st.dataframe(df)
        else:
            st.write("저장된 관심 종목이 없습니다.")

# 관심 종목 추가 화면 
if page=="insert_watchlist":
    if st.session_state.member_id is None:
        st.error("로그인이 필요합니다.")
    else:
        st.title("관심 종목 추가")

        st.write("입력 가능한 종목(없는 종목은 등록 신청을 먼저 해주세요.)")
        result=view_stocks()
        df=pd.DataFrame(result,
                        columns=["종목 코드","종목명"]
                            )
        st.dataframe(df)

        stock_code = st.text_input("관심 종목 코드:")
        if st.button("추가하기"):
            if not check_stock(stock_code):
                st.error("존재하지 않는 종목입니다. 다시 입력하거나 등록 신청을 해주세요.")
            elif check_watchlist(st.session_state.member_id, stock_code):
                st.error("이미 등록된 종목입니다.")
            else:
                insert_watchlist(st.session_state.member_id, stock_code)
                st.success("관심 종목이 성공적으로 추가되었습니다.")

# 관심 종목 삭제 화면 
if page=="delete_watchlist":
    if st.session_state.member_id is None:
        st.error("로그인이 필요합니다.")
    else:
        st.title("관심 종목 삭제")

        result=get_watchlist(st.session_state.member_id)
        if result:
            df=pd.DataFrame(result,
                            columns=["관심 목록 ID","종목 코드","종목명"]
                                )
            df=df.drop(columns=["관심 목록 ID"])
            df.insert(0,"등록 순번",range(1,len(df)+1))
            st.dataframe(df)

            delete_code = st.text_input("삭제할 관심 종목 코드를 입력하세요:")
            if st.button("삭제하기"):
                delete_watchlist(st.session_state.member_id, delete_code)
                st.success("관심 종목이 성공적으로 삭제되었습니다.")
                st.session_state.page = "delete_watchlist"
                st.rerun()
        else:
            st.write("저장된 관심 종목이 없습니다.")

# 종목 등록 요청 화면 
if page=="request_stock":
    if st.session_state.member_id is None:
        st.write("로그인이 필요합니다.")
    else:
        st.title("종목 등록 요청")
        st.write("등록을 원하는 종목의 정보를 입력해주세요.")
        stock_code = st.text_input("종목 코드:")
        stock_name = st.text_input("종목명:")
        request_date=date.today()

        if st.button("등록 요청하기"):
            if check_stock(stock_code):
                st.error("이미 등록된 종목입니다.")
            elif check_request(stock_code):
                st.error("이미 등록 요청된 종목입니다. 처리를 기다려주세요.")
            else:
                stock_request(st.session_state.member_id, stock_code, stock_name, request_date)
                st.success(f"종목 등록 요청이 성공적으로 제출되었습니다. (종목 코드: {stock_code}, 종목명: {stock_name})")

# 관리자 전용 요청 관리 페이지 
if page=="request_manage":
    st.write("대기 요청 목록")
    result=show_request()

    if result:
        df=pd.DataFrame(result,
                        columns=["등록 순번","회원 ID", "종목 코드","종목 이름","등록 날짜","처리 상태"])
        st.dataframe(df)

        request_id=st.number_input("등록 처리할 순번을 입력하세요.:", min_value=1,max_value=len(df), step=1 )
        if st.button("등록 처리"):
            confirm_request(request_id)
            st.success("등록 처리 되었습니다.")
            st.rerun()
    else:
        st.write("처리할 요청이 없습니다.")

