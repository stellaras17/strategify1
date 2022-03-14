import pyrebase, json
import websocket, requests
import talib
from threading import Thread

websockets = {
    "SOCKETBTC1M" : "wss://stream.binance.com:9443/ws/btcusdt@kline_1m",
    "SOCKETBTC5M" : "wss://stream.binance.com:9443/ws/btcusdt@kline_5m",
    "SOCKETBTC1H" : "wss://stream.binance.com:9443/ws/btcusdt@kline_1h",
    "SOCKETBTC4H" : "wss://stream.binance.com:9443/ws/btcusdt@kline_4h",
    "SOCKETBTC1D" : "wss://stream.binance.com:9443/ws/btcusdt@kline_1d",

    "SOCKETETH1M" : "wss://stream.binance.com:9443/ws/ethusdt@kline_1m",
    "SOCKETETH5M" : "wss://stream.binance.com:9443/ws/ethusdt@kline_5m",
    "SOCKETETH1H" : "wss://stream.binance.com:9443/ws/ethusdt@kline_1h",
    "SOCKETETH4H" : "wss://stream.binance.com:9443/ws/ethusdt@kline_4h",
    "SOCKETETH1D" : "wss://stream.binance.com:9443/ws/ethusdt@kline_1d",

    "SOCKETBNB1M" : "wss://stream.binance.com:9443/ws/bnbusdt@kline_1m",
    "SOCKETBNB5M" : "wss://stream.binance.com:9443/ws/bnbusdt@kline_5m",
    "SOCKETBNB1H" : "wss://stream.binance.com:9443/ws/bnbusdt@kline_1h",
    "SOCKETBNB4H" : "wss://stream.binance.com:9443/ws/bnbusdt@kline_4h",
    "SOCKETBNB1D" : "wss://stream.binance.com:9443/ws/bnbusdt@kline_1d",

    "SOCKETZIL1M" : "wss://stream.binance.com:9443/ws/zilusdt@kline_1m",
    "SOCKETZIL5M" : "wss://stream.binance.com:9443/ws/zilusdt@kline_5m",
    "SOCKETZIL1H" : "wss://stream.binance.com:9443/ws/zilusdt@kline_1h",
    "SOCKETZIL4H" : "wss://stream.binance.com:9443/ws/zilusdt@kline_4h",
    "SOCKETZIL1D" : "wss://stream.binance.com:9443/ws/zilusdt@kline_1d"
}

SMAs = {
    'BTC1m' : 0,
    'BTC5m' : 0,
    'BTC1h' : 0,
    'BTC4h' : 0,
    'BTC1d' : 0,

    'ETH1m' : 0,
    'ETH5m' : 0,
    'ETH1h' : 0,
    'ETH4h' : 0,
    'ETH1d' : 0,

    'BNB1m' : 0,
    'BNB5m' : 0,
    'BNB1h' : 0,
    'BNB4h' : 0,
    'BNB1d' : 0,

    'ZIL1m' : 0,
    'ZIL5m' : 0,
    'ZIL1h' : 0,
    'ZIL4h' : 0,
    'ZIL1d' : 0,
}

RSIs = {
    'BTC1m' : 0,
    'BTC5m' : 0,
    'BTC1h' : 0,
    'BTC4h' : 0,
    'BTC1d' : 0,

    'ETH1m' : 0,
    'ETH5m' : 0,
    'ETH1h' : 0,
    'ETH4h' : 0,
    'ETH1d' : 0,

    'BNB1m' : 0,
    'BNB5m' : 0,
    'BNB1h' : 0,
    'BNB4h' : 0,
    'BNB1d' : 0,

    'ZIL1m' : 0,
    'ZIL5m' : 0,
    'ZIL1h' : 0,
    'ZIL4h' : 0,
    'ZIL1d' : 0,
}

EMAs = {
    'BTC1m' : 0,
    'BTC5m' : 0,
    'BTC1h' : 0,
    'BTC4h' : 0,
    'BTC1d' : 0,

    'ETH1m' : 0,
    'ETH5m' : 0,
    'ETH1h' : 0,
    'ETH4h' : 0,
    'ETH1d' : 0,

    'BNB1m' : 0,
    'BNB5m' : 0,
    'BNB1h' : 0,
    'BNB4h' : 0,
    'BNB1d' : 0,

    'ZIL1m' : 0,
    'ZIL5m' : 0,
    'ZIL1h' : 0,
    'ZIL4h' : 0,
    'ZIL1d' : 0,
}

MACDs = {
    'BTC1m' : 0,
    'BTC5m' : 0,
    'BTC1h' : 0,
    'BTC4h' : 0,
    'BTC1d' : 0,

    'ETH1m' : 0,
    'ETH5m' : 0,
    'ETH1h' : 0,
    'ETH4h' : 0,
    'ETH1d' : 0,

    'BNB1m' : 0,
    'BNB5m' : 0,
    'BNB1h' : 0,
    'BNB4h' : 0,
    'BNB1d' : 0,

    'ZIL1m' : 0,
    'ZIL5m' : 0,
    'ZIL1h' : 0,
    'ZIL4h' : 0,
    'ZIL1d' : 0,
}

closes = {
    'BTC1m' : [],
    'BTC5m' : [],
    'BTC1h' : [],
    'BTC4h' : [],
    'BTC1d' : [],

    'ETH1m' : [],
    'ETH5m' : [],
    'ETH1h' : [],
    'ETH4h' : [],
    'ETH1d' : [],

    'BNB1m' : [],
    'BNB5m' : [],
    'BNB1h' : [],
    'BNB4h' : [],
    'BNB1d' : [],

    'ZIL1m' : [],
    'ZIL5m' : [],
    'ZIL1h' : [],
    'ZIL4h' : [],
    'ZIL1d' : [],
}

allStrats = {}
stratsBTC = {}
stratsETH = {}
stratsBNB = {}
stratsZIL = {}
timeperiodSmall = 12
timeperiod = 26
strats = None
firebase = None

def rotateList(l, n):
    return l[n:] + l[:n]

def initiateStrats():
    global allStrats, strats, firebase
    f = open('api.json')
    api = json.load(f)
    fireBaseConfig = api
    firebase = pyrebase.initialize_app(fireBaseConfig)
    db = firebase.database()
    strats = db.child("strats").get()

    for user in strats.each():
        usersstrats = firebase.database().child("strats").child(user.key()).get()
        for strat in usersstrats.each():
            if strat.val()['active'] == True:
                allStrats[strat.key()] = strat.val()
    splitStrats()

def splitStrats():
    global allStrats, stratsBTC, stratsETH, stratsBNB, stratsZIL
    for strat in allStrats:
        if allStrats[strat]['ticker'] == 'BTCUSDT':
            stratsBTC[strat] = allStrats[strat]
        elif allStrats[strat]['ticker'] == 'ETHUSDT':
            stratsETH[strat] = allStrats[strat]            
        elif allStrats[strat]['ticker'] == 'BNBUSDT':
            stratsBNB[strat] = allStrats[strat]
        elif allStrats[strat]['ticker'] == 'ZILUSDT':
            stratsZIL[strat] = allStrats[strat]
    return

def buyOrder(strat, price):
    user = findUser(strat)
    ticker = allStrats[strat]['ticker'][:3]
    amount = allStrats[strat]['amount']
    
    current = firebase.database().child("crypto").child(user).child(ticker).get().val()
    updated = current + (amount/price)
    firebase.database().child("crypto").child(user).update({ticker : updated})

    current = firebase.database().child("coins").child(user).get().val()
    updated = current - amount
    firebase.database().child("coins").update({user : updated})

def sellOrder(strat, price):
    user = findUser(strat)
    ticker = allStrats[strat]['ticker'][:3]
    amount = allStrats[strat]['amount']
    
    current = firebase.database().child("crypto").child(user).child(ticker).get().val()
    updated = current - (amount/price)
    firebase.database().child("crypto").child(user).update({ticker : updated})

    current = firebase.database().child("coins").child(user).get().val()
    updated = current + amount
    firebase.database().child("coins").update({user : updated})


def findUser(stratToFind):
    for user in strats.each():
        usersstrats = firebase.database().child("strats").child(user.key()).get()
        for strat in usersstrats.each():
            if strat.key() == stratToFind:
                return user.key()


def on_open(ws):
    print("opened connection")
    
def on_close(ws):
    print("closed connection")

def on_message(ws, message):
    global closes
    global SMAs
    global EMAs
    global MACDs
    global RSIs
    global timeperiod
    global timeperiodSmall

    json_message = json.loads(message)
    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']
    volume = candle['v']
    high = candle['h']
    low = candle['l']

    if is_candle_closed:
        print("candlestick closed at {}".format(close))
        if 'btc' in ws.url:
            if '1m' in ws.url:
                if len(closes['BTC1m']) < timeperiod:
                    closes['BTC1m'].append(close)
                else:
                    closes['BTC1m'] = rotateList(closes['BTC1m'],1)
                    closes['BTC1m'][-1] = close
                    SMAs['BTC1m'] = sum(closes['BTC1m']) / float(len(closes['BTC1m']))
                    EMAs["BTC1m"] = talib.EMA(closes['BTC1m'], timeperiod = timeperiod)
                    MACDs['BTC1m'] = talib.EMA(closes['BTC1m'], timeperiod = timeperiodSmall) - talib.EMA(closes['BTC1m'], timeperiod = timeperiod)
                    RSIs['BTC1m'] = talib.RSI(closes['BTC1m'], timeperiod=timeperiod)
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) > SMAs['BTC1m']:
                                buyOrder(strat, close)
            elif '5m' in ws.url:
                if len(closes['BTC5m']) < timeperiod:
                    closes['BTC5m'].append(close)
                else:
                    closes['BTC5m'] = rotateList(closes['BTC5m'],1)
                    closes['BTC5m'][-1] = close
                    SMAs['BTC5m'] = sum(closes['BTC5m']) / float(len(closes['BTC5m']))
                    EMAs["BTC5m"] = talib.EMA(closes['BTC5m'], timeperiod = timeperiod)
                    MACDs['BTC5m'] = talib.EMA(closes['BTC5m'], timeperiod = timeperiodSmall) - talib.EMA(closes['BTC5m'], timeperiod = timeperiod)
                    RSIs['BTC5m'] = talib.RSI(closes['BTC5m'], timeperiod=timeperiod)
            elif '1h' in ws.url:
                if len(closes['BTC1h']) < timeperiod:
                    closes['BTC1h'].append(close)
                else:
                    closes['BTC1h'] = rotateList(closes['BTC1h'],1)
                    closes['BTC1h'][-1] = close
                    SMAs['BTC1h'] = sum(closes['BTC1h']) / float(len(closes['BTC1h']))
                    EMAs["BTC1h"] = talib.EMA(closes['BTC1h'], timeperiod = timeperiod)
                    MACDs['BTC1h'] = talib.EMA(closes['BTC1h'], timeperiod = timeperiodSmall) - talib.EMA(closes['BTC1h'], timeperiod = timeperiod)
                    RSIs['BTC1h'] = talib.RSI(closes['BTC1h'], timeperiod=timeperiod)
            elif '4h' in ws.url:
                if len(closes['BTC4h']) < timeperiod:
                    closes['BTC4h'].append(close)
                else:
                    closes['BTC4h'] = rotateList(closes['BTC4h'],1)
                    closes['BTC4h'][-1] = close
                    SMAs['BTC4h'] = sum(closes['BTC4h']) / float(len(closes['BTC4h']))
                    EMAs["BTC4h"] = talib.EMA(closes['BTC4h'], timeperiod = timeperiod)
                    MACDs['BTC4h'] = talib.EMA(closes['BTC4h'], timeperiod = timeperiodSmall) - talib.EMA(closes['BTC4h'], timeperiod = timeperiod)
                    RSIs['BTC4h'] = talib.RSI(closes['BTC4h'], timeperiod=timeperiod)
            elif '1d' in ws.url:
                if len(closes['BTC1d']) < timeperiod:
                    closes['BTC1d'].append(close)
                else:
                    closes['BTC1d'] = rotateList(closes['BTC1d'],1)
                    closes['BTC1d'][-1] = close
                    SMAs['BTC1d'] = sum(closes['BTC1d']) / float(len(closes['BTC1d']))
                    EMAs["BTC1d"] = talib.EMA(closes['BTC1d'], timeperiod = timeperiod)
                    MACDs['BTC1d'] = talib.EMA(closes['BTC1d'], timeperiod = timeperiodSmall) - talib.EMA(closes['BTC1d'], timeperiod = timeperiod)
                    RSIs['BTC1d'] = talib.RSI(closes['BTC1d'], timeperiod=timeperiod)

        elif 'eth' in ws.url:
            if '1m' in ws.url:
                if len(closes['ETH1m']) < timeperiod:
                    closes['ETH1m'].append(close)
                else:
                    closes['ETH1m'] = rotateList(closes['ETH1m'],1)
                    closes['ETH1m'][-1] = close
                    SMAs['ETH1m'] = sum(closes['ETH1m']) / float(len(closes['ETH1m']))
                    EMAs["ETH1m"] = talib.EMA(closes['ETH1m'], timeperiod = timeperiod)
                    MACDs['ETH1m'] = talib.EMA(closes['ETH1m'], timeperiod = timeperiodSmall) - talib.EMA(closes['ETH1m'], timeperiod = timeperiod)
                    RSIs['ETH1m'] = talib.RSI(closes['ETH1m'], timeperiod=timeperiod)
            elif '5m' in ws.url:
                if len(closes['ETH5m']) < timeperiod:
                    closes['ETH5m'].append(close)
                else:
                    closes['ETH5m'] = rotateList(closes['ETH5m'],1)
                    closes['ETHETH5m5m'][-1] = close
                    SMAs['ETH5m'] = sum(closes['ETH5m']) / float(len(closes['ETH5m']))
                    EMAs["ETH5m"] = talib.EMA(closes['ETH5m'], timeperiod = timeperiod)
                    MACDs['ETH5m'] = talib.EMA(closes['ETH5m'], timeperiod = timeperiodSmall) - talib.EMA(closes['ETH5m'], timeperiod = timeperiod)
                    RSIs['ETH5m'] = talib.RSI(closes['ETH5m'], timeperiod=timeperiod)
            elif '1h' in ws.url:
                if len(closes['ETH1h']) < timeperiod:
                    closes['ETH1h'].append(close)
                else:
                    closes['ETH1h'] = rotateList(closes['ETH1h'],1)
                    closes['ETH1h'][-1] = close
                    SMAs['ETH1h'] = sum(closes['ETH1h']) / float(len(closes['ETH1h']))
                    EMAs["ETH1h"] = talib.EMA(closes['ETH1h'], timeperiod = timeperiod)
                    MACDs['ETH1h'] = talib.EMA(closes['ETH1h'], timeperiod = timeperiodSmall) - talib.EMA(closes['ETH1h'], timeperiod = timeperiod)
                    RSIs['ETH1h'] = talib.RSI(closes['ETH1h'], timeperiod=timeperiod)
            elif '4h' in ws.url:
                if len(closes['ETH4h']) < timeperiod:
                    closes['ETH4h'].append(close)
                else:
                    closes['ETH4h'] = rotateList(closes['ETH4h'],1)
                    closes['ETH4h'][-1] = close
                    SMAs['ETH4h'] = sum(closes['ETH4h']) / float(len(closes['ETH4h']))
                    EMAs["ETH4h"] = talib.EMA(closes['ETH4h'], timeperiod = timeperiod)
                    MACDs['ETH4h'] = talib.EMA(closes['ETH4h'], timeperiod = timeperiodSmall) - talib.EMA(closes['ETH4h'], timeperiod = timeperiod)
                    RSIs['ETH4h'] = talib.RSI(closes['ETH4h'], timeperiod=timeperiod)
            elif '1d' in ws.url:
                if len(closes['ETH1d']) < timeperiod:
                    closes['ETH1d'].append(close)
                else:
                    closes['ETH1d'] = rotateList(closes['ETH1d'],1)
                    closes['ETH1d'][-1] = close
                    SMAs['ETH1d'] = sum(closes['ETH1d']) / float(len(closes['ETH1d']))
                    EMAs["ETH1d"] = talib.EMA(closes['ETH1d'], timeperiod = timeperiod)
                    MACDs['ETH1d'] = talib.EMA(closes['ETH1d'], timeperiod = timeperiodSmall) - talib.EMA(closes['ETH1d'], timeperiod = timeperiod)
                    RSIs['ETH1d'] = talib.RSI(closes['ETH1d'], timeperiod=timeperiod)

        elif 'bnb' in ws.url:
            if '1m' in ws.url:
                if len(closes['BNB1m']) < timeperiod:
                    closes['BNB1m'].append(close)
                else:
                    closes['BNB1m'] = rotateList(closes['BNB1m'],1)
                    closes['BNB1m'][-1] = close
                    SMAs['BNB1m'] = sum(closes['BNB1m']) / float(len(closes['BNB1m']))
                    EMAs["BNB1m"] = talib.EMA(closes['BNB1m'], timeperiod = timeperiod)
                    MACDs['BNB1m'] = talib.EMA(closes['BNB1m'], timeperiod = timeperiodSmall) - talib.EMA(closes['BNB1m'], timeperiod = timeperiod)
                    RSIs['BNB1m'] = talib.RSI(closes['BNB1m'], timeperiod=timeperiod)
            elif '5m' in ws.url:
                if len(closes['BNB5m']) < timeperiod:
                    closes['BNB5m'].append(close)
                else:
                    closes['BNB5m'] = rotateList(closes['BNB5m'],1)
                    closes['BNB5m'][-1] = close
                    SMAs['BNB5m'] = sum(closes['BNB5m']) / float(len(closes['BNB5m']))
                    EMAs["BNB5m"] = talib.EMA(closes['BNB5m'], timeperiod = timeperiod)
                    MACDs['BNB5m'] = talib.EMA(closes['BNB5m'], timeperiod = timeperiodSmall) - talib.EMA(closes['BNB5m'], timeperiod = timeperiod)
                    RSIs['BNB5m'] = talib.RSI(closes['BNB5m'], timeperiod=timeperiod)
            elif '1h' in ws.url:
                if len(closes['BNB1h']) < timeperiod:
                    closes['BNB1h'].append(close)
                else:
                    closes['BNB1h'] = rotateList(closes['BNB1h'],1)
                    closes['BNB1h'][-1] = close
                    SMAs['BNB1h'] = sum(closes['BNB1h']) / float(len(closes['BNB1h']))
                    EMAs["BNB1h"] = talib.EMA(closes['BNB1h'], timeperiod = timeperiod)
                    MACDs['BNB1h'] = talib.EMA(closes['BNB1h'], timeperiod = timeperiodSmall) - talib.EMA(closes['BNB1h'], timeperiod = timeperiod)
                    RSIs['BNB1h'] = talib.RSI(closes['BNB1h'], timeperiod=timeperiod)
            elif '4h' in ws.url:
                if len(closes['BNB4h']) < timeperiod:
                    closes['BNB4h'].append(close)
                else:
                    closes['BNB4h'] = rotateList(closes['BNB4h'],1)
                    closes['BNB4h'][-1] = close
                    SMAs['BNB4h'] = sum(closes['BNB4h']) / float(len(closes['BNB4h']))
                    EMAs["BNB4h"] = talib.EMA(closes['BNB4h'], timeperiod = timeperiod)
                    MACDs['BNB4h'] = talib.EMA(closes['BNB4h'], timeperiod = timeperiodSmall) - talib.EMA(closes['BNB4h'], timeperiod = timeperiod)
                    RSIs['BNB4h'] = talib.RSI(closes['BNB4h'], timeperiod=timeperiod)
            elif '1d' in ws.url:
                if len(closes['BNB1d']) < timeperiod:
                    closes['BNB1d'].append(close)
                else:
                    closes['BNB1d'] = rotateList(closes['BNB1d'],1)
                    closes['BNB1d'][-1] = close
                    SMAs['BNB1d'] = sum(closes['BNB1d']) / float(len(closes['BNB1d']))
                    EMAs["BNB1d"] = talib.EMA(closes['BNB1d'], timeperiod = timeperiod)
                    MACDs['BNB1d'] = talib.EMA(closes['BNB1d'], timeperiod = timeperiodSmall) - talib.EMA(closes['BNB1d'], timeperiod = timeperiod)
                    RSIs['BNB1d'] = talib.RSI(closes['BNB1d'], timeperiod=timeperiod)

        elif 'zil' in ws.url:
            if '1m' in ws.url:
                if len(closes['ZIL1m']) < timeperiod:
                    closes['ZIL1m'].append(close)
                else:
                    closes['ZIL1m'] = rotateList(closes['ZIL1m'],1)
                    closes['ZIL1m'][-1] = close
                    SMAs['ZIL1m'] = sum(closes['ZIL1m']) / float(len(closes['ZIL1m']))
                    EMAs["ZIL1m"] = talib.EMA(closes['ZIL1m'], timeperiod = timeperiod)
                    MACDs['ZIL1m'] = talib.EMA(closes['ZIL1m'], timeperiod = timeperiodSmall) - talib.EMA(closes['ZIL1m'], timeperiod = timeperiod)
                    RSIs['ZIL1m'] = talib.RSI(closes['ZIL1m'], timeperiod=timeperiod)
            elif '5m' in ws.url:
                if len(closes['ZIL5m']) < timeperiod:
                    closes['ZIL5m'].append(close)
                else:
                    closes['ZIL5m'] = rotateList(closes['ZIL5m'],1)
                    closes['ZIL5m'][-1] = close
                    SMAs['ZIL5m'] = sum(closes['ZIL5m']) / float(len(closes['ZIL5m']))
                    EMAs["ZIL5m"] = talib.EMA(closes['ZIL5m'], timeperiod = timeperiod)
                    MACDs['ZIL5m'] = talib.EMA(closes['ZIL5m'], timeperiod = timeperiodSmall) - talib.EMA(closes['ZIL5m'], timeperiod = timeperiod)
                    RSIs['ZIL5m'] = talib.RSI(closes['ZIL5m'], timeperiod=timeperiod)
            elif '1h' in ws.url:
                if len(closes['ZIL1h']) < timeperiod:
                    closes['ZIL1h'].append(close)
                else:
                    closes['ZIL1h'] = rotateList(closes['ZIL1h'],1)
                    closes['ZIL1h'][-1] = close
                    SMAs['ZIL1h'] = sum(closes['ZIL1h']) / float(len(closes['ZIL1h']))
                    EMAs["ZIL1h"] = talib.EMA(closes['ZIL1h'], timeperiod = timeperiod)
                    MACDs['ZIL1h'] = talib.EMA(closes['ZIL1h'], timeperiod = timeperiodSmall) - talib.EMA(closes['ZIL1h'], timeperiod = timeperiod)
                    RSIs['ZIL1h'] = talib.RSI(closes['ZIL1h'], timeperiod=timeperiod)
            elif '4h' in ws.url:
                if len(closes['ZIL4h']) < timeperiod:
                    closes['ZIL4h'].append(close)
                else:
                    closes['ZIL4h'] = rotateList(closes['ZIL4h'],1)
                    closes['ZIL4h'][-1] = close
                    SMAs['ZIL4h'] = sum(closes['ZIL4h']) / float(len(closes['ZIL4h']))
                    EMAs["ZIL4h"] = talib.EMA(closes['ZIL4h'], timeperiod = timeperiod)
                    MACDs['ZIL4h'] = talib.EMA(closes['ZIL4h'], timeperiod = timeperiodSmall) - talib.EMA(closes['ZIL4h'], timeperiod = timeperiod)
                    RSIs['ZIL4h'] = talib.RSI(closes['ZIL4h'], timeperiod=timeperiod)
            elif '1d' in ws.url:
                if len(closes['ZIL1d']) < timeperiod:
                    closes['ZIL1d'].append(close)
                else:
                    closes['ZIL1d'] = rotateList(closes['ZIL1d'],1)
                    closes['ZIL1d'][-1] = close
                    SMAs['ZIL1d'] = sum(closes['ZIL1d']) / float(len(closes['ZIL1d']))
                    EMAs["ZIL1d"] = talib.EMA(closes['ZIL1d'], timeperiod = timeperiod)
                    MACDs['ZIL1d'] = talib.EMA(closes['ZIL1d'], timeperiod = timeperiodSmall) - talib.EMA(closes['ZIL1d'], timeperiod = timeperiod)
                    RSIs['ZIL1d'] = talib.RSI(closes['ZIL1d'], timeperiod=timeperiod)
        print(closes)
initiateStrats()
sellOrder('ID1', 10)
for socket in websockets:
    ws = websocket.WebSocketApp(websockets[socket], on_open = on_open, on_message = on_message, on_close = on_close)
    wst = Thread(target=ws.run_forever)
    wst.start()