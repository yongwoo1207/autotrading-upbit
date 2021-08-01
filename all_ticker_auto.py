import pyupbit
import time
import datetime
import winsound # 매수되면 소리나도록 하기 위해 import
import pandas
import random


#매수, 매도시 나오는 소리 설정
def beepsound():
    fr = 2000    # range : 37 ~ 32767
    du = 1000     # 1000 ms ==1second
    winsound.Beep(fr, du) # winsound.Beep(frequency, duration)


#계정 로그인 및 원화 잔고 들고 오기
f = open('upbit key.txt')
key = f.readlines()
access = key[1].strip()
secret = key[2].strip()
f.close()
log_in = pyupbit.Upbit(access, secret)   #Upbit 클래스 즉, 거래API에 접근할 수 있는 변수이다


#공통변수
KRW_ticker = pyupbit.get_tickers('KRW')
hold = False
op_mode = False

#가격 함수
def get_price(ticker):
    price = pyupbit.get_current_price(ticker)
    return price


#변동성 돌파전략 목표가 정하기
def get_target(ticker):
    price = get_price(ticker)
    df = pyupbit.get_ohlcv(ticker, 'day')
    before = df.iloc[-2]
    now = df.iloc[-1]
    target = now['open'] + (before['high'] - before['low'])*0.4
    return target


#목표가 갱신
def target_prices(ticker):
    if now.hour == 9 :
        if now.minute == 00 and 10 <= now.second <= 20:
            target_price = get_target(ticker)
    return target_price


while True:
    #반복되는 변수들
    now = datetime.datetime.now()
    my_KRW_balance = log_in.get_balance(ticker = 'KRW')


    #ma5_ticker 중에서 변동성 돌파전략 충족하는 티커
    #하루마다 목표가 갱신하기
    dolpa_ticker = []
    if now.hour == 9 and now.minute == 00 and 00 <= now.second <= 10:
        op_mode = True

    while op_mode == True:
        for i in KRW_ticker:
            price = get_price(i)
            target = get_target(i)
            print('현재 검토중인 종목:', i)

            if price > target:
                dolpa_ticker.append(i)
            else:
                pass
            time.sleep(0.2)
        if len(dolpa_ticker) == 0:
            print('돌파전략 충족 종목 없음')
        else:
            print('돌파전략 충족 종목 : ', dolpa_ticker)
            break


    #가격 변동률 구하기 (현재 1분봉)
    price_gap_dict = {}
    for i in dolpa_ticker:
        dolpa_price = pyupbit.get_price(i)
        df = pyupbit.get_ohlcv(i, 'minute1', 1)[-1]
        bp = df['open']
        price_gap = dolpa_price / bp
        price_gap_dict[i] = price_gap



    #가격 변동률 순으로 정렬
    price_gap_dict.items()
    price_gap_rank = sorted(price_gap_dict.items(), key=lambda x:x[1], reverse=True)


    #가격 상위 종목 target_ticker로 입력하기
    target_ticker = []
    if len(price_gap_rank) > 4:
        for i in range(0,4):
            target_ticker.append(price_gap_rank[i][0])
    else:
        for i in range(len(price_gap_rank)):
            target_ticker.append(price_gap_rank[i][0])
    print('매수할 종목 :',target_ticker)

    if len(target_ticker) > 0:
        KRW_balance = my_KRW_balance/len(target_ticker)
    else:
        pass


    #매수
    if op_mode == True and hold == False and len(target_ticker) > 0:
        for i in target_ticker:
            log_in.buy_market_order(i, KRW_balance)
            hold = True
            op_mode = False
            beepsound()
            print('종목:{} 소유여부{}'.format(target_ticker, hold))


    #시간이 되면 매도 하기
    if hold==True and now.hour == 12 :
        if now.minute == 00 and 00 <= now.second <= 2:
            for i in target_ticker:
               coin_balance = log_in.get_balance(i)
               log_in.sell_market_order(i, coin_balance)
               beepsound()
               print('{} 매도가 정상처리되었습니다.'.format(target_ticker))
               hold = False
