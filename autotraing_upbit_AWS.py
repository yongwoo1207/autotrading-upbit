#파이스탁 240분봉 예시
import pyupbit
import time
import datetime

#목표값 불러오기
def cal_target(ticker):
    df = pyupbit.get_ohlcv(ticker, 'minute240')
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    target = today['open'] + yesterday_range*0.4
    return target


#객체생성
access = 'a'
secret = 'a'


log_in = pyupbit.Upbit(access, secret)   #Upbit 클래스 즉, 거래API에 접근할 수 있는 변수이다
my_KRW_balance = log_in.get_balance('KRW')   #원화잔고 변수
print(my_KRW_balance)


#변수설정
target = cal_target('KRW-ETC')
op_mode = False
hold = False

while True:
    now = datetime.datetime.now()

    #매도시도
    if now.hour in [1, 5, 9, 13, 17, 21] and now.minute == 00 and 00 <= now.second <=1:
        if op_mode is True and hold is True:
            ETC_balance = log_in.get_balance('KRW-ETC')
            log_in.sell_market_order('KRW-ETC', ETC_balance)
            hold = False

        op_mode = False
        time.sleep(10)

    #4시간 마다 목표가 갱신
    if now.hour in [1, 5, 9, 13, 17, 21] and now.minute == 0 and 20 <= now.second <=30:  #출력값에서 값을 주면 값을 벗어날 수 있어서 범위로 줬다.
        target = cal_target('KRW-ETC')
        time.sleep(10)   #초 시간 구간동안 계속 반복되어서 달아둬 1회만 반복
        op_mode =True

    price = pyupbit.get_current_price('KRW-ETC')

    #매초마다 조건을 확인한 후 매수 시도 
    if op_mode is True and hold is False and price >= target:
        #매수
        krw_balance = log_in.get_balance('KRW')
        log_in.buy_market_order('KRW-ETC', krw_balance *0.8)
        hold = True

    print('현재시간:{} 목표가:{} 현재가:{} 보유상태:{} 동작상태:{}'.format(now, target, price, hold, op_mode))
    time.sleep(1)   #1초에 한번씩 코인 가격 불러오기 위해서 1초 쉬어간다.
