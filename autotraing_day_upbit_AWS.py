'''
단순 변동성 돌파 
1일 봉 기준 거래
주 코인 이더리움클래식
'''


#파이스탁 1일봉 예시
import pyupbit
import time
import datetime

#목표값 불러오기
def cal_target(ticker):
    df = pyupbit.get_ohlcv(ticker, 'day')
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    target = today['open'] + yesterday_range*0.4
    return target


#객체생성
access = 'a' #자신의 key 입력하기
secret = 'a'
log_in = pyupbit.Upbit(access, secret)
my_KRW_balance = log_in.get_balance('KRW')   #원화잔고 변수


#변수설정
target = cal_target('KRW-ETC')
op_mode = False
hold = False

while True:
    now = datetime.datetime.now()

    #매도시도
    if now.hour == 8 and now.minute == 59 and 50 <= now.second <=59:
        if op_mode is True and hold is True:
            ETC_balance = log_in.get_balance('KRW-ETC')
            log_in.sell_market_order('KRW-ETC', ETC_balance)
            hold = False

        op_mode = False
        time.sleep(10)

    #하루 마다 목표가 갱신
    if now.hour == 9 and now.minute == 0 and 20 <= now.second <=30:  #출력값에서 값을 주면 값을 벗어날 수 있어서 범위로 줬다.
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
