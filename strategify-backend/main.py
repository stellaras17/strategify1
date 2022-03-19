import pyrebase, json
import websocket, time
import talib
import numpy as np
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
rsiperiod = 21
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
    coins = firebase.database().child("coins").child(user).get().val()
    ticker = allStrats[strat]['ticker'][:3]
    amount = allStrats[strat]['amount']

    if coins > amount:
        
        current = firebase.database().child("crypto").child(user).child(ticker).get().val()
        updated = current + (amount/price)
        firebase.database().child("crypto").child(user).update({ticker : updated})

        current = firebase.database().child("coins").child(user).get().val()
        updated = current - amount
        firebase.database().child("coins").update({user : updated})

        dbOrder(user, amount, allStrats[strat]['name'], allStrats[strat]['ticker'], time.time(), 'BUY')    
    else:
        dbOrder(user, amount, allStrats[strat]['name'], allStrats[strat]['ticker'], time.time(), 'ERROR' ) 

def sellOrder(strat, price):
    user = findUser(strat)
    coins = firebase.database().child("coins").child(user).get().val()
    ticker = allStrats[strat]['ticker'][:3]
    amount = allStrats[strat]['amount']
    
    if coins > amount:
        current = firebase.database().child("crypto").child(user).child(ticker).get().val()
        updated = current - (amount/price)
        firebase.database().child("crypto").child(user).update({ticker : updated})

        current = firebase.database().child("coins").child(user).get().val()
        updated = current + amount
        firebase.database().child("coins").update({user : updated})

        dbOrder(user, amount, allStrats[strat]['name'], allStrats[strat]['ticker'], time.time(), 'SELL' )  
    else:
        dbOrder(user, amount, allStrats[strat]['name'], allStrats[strat]['ticker'], time.time(), 'ERROR' )

def dbOrder(user, amount, strat, ticker, time, type):
    order = {
        "amount": amount,
        "strat": strat,
        "ticker": ticker,
        "time": time,
        "type": type
    }
    firebase.database().child("orders").child(user).push(order)



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
                    closes['BTC1m'].append(float(close))
                else:
                    closes['BTC1m'] = rotateList(closes['BTC1m'],1)
                    closes['BTC1m'][-1] = float(close)
                    SMAs['BTC1m'] = sum(closes['BTC1m']) / float(len(closes['BTC1m']))
                    EMAs["BTC1m"] = (talib.EMA(np.array(closes['BTC1m']), timeperiod = timeperiod))[-1]
                    MACDs['BTC1m'] = (talib.EMA(np.array(closes['BTC1m']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BTC1m']), timeperiod = timeperiod))[-1]
                    RSIs['BTC1m'] = (talib.RSI(np.array(closes['BTC1m']), timeperiod=rsiperiod))[-1]
                    
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BTC1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BTC1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BTC1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BTC1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BTC1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BTC1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BTC1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BTC1m']:
                                sellOrder(strat, float(close))
            elif '5m' in ws.url:
                if len(closes['BTC5m']) < timeperiod:
                    closes['BTC5m'].append(float(close))
                else:
                    closes['BTC5m'] = rotateList(closes['BTC5m'],1)
                    closes['BTC5m'][-1] = float(close)
                    SMAs['BTC5m'] = sum(closes['BTC5m']) / float(len(closes['BTC5m']))
                    EMAs["BTC5m"] = (talib.EMA(np.array(closes['BTC5m']), timeperiod = timeperiod))[-1]
                    MACDs['BTC5m'] = (talib.EMA(np.array(closes['BTC5m']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BTC5m']), timeperiod = timeperiod))[-1]
                    RSIs['BTC5m'] = (talib.RSI(np.array(closes['BTC5m']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BTC5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BTC5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BTC5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BTC5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BTC5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BTC5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BTC5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BTC5m']:
                                sellOrder(strat, float(close))
            elif '1h' in ws.url:
                if len(closes['BTC1h']) < timeperiod:
                    closes['BTC1h'].append(float(close))
                else:
                    closes['BTC1h'] = rotateList(closes['BTC1h'],1)
                    closes['BTC1h'][-1] = float(close)
                    SMAs['BTC1h'] = sum(closes['BTC1h']) / float(len(closes['BTC1h']))
                    EMAs["BTC1h"] = (talib.EMA(np.array(closes['BTC1h']), timeperiod = timeperiod))[-1]
                    MACDs['BTC1h'] = (talib.EMA(np.array(closes['BTC1h']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BTC1h']), timeperiod = timeperiod))[-1]
                    RSIs['BTC1h'] = (talib.RSI(np.array(closes['BTC1h']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BTC1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BTC1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BTC1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BTC1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BTC1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BTC1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BTC1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BTC1h']:
                                sellOrder(strat, float(close))
                    RSIs['BTC1h'] = talib.RSI(closes['BTC1h'], timeperiod=timeperiod)
            elif '4h' in ws.url:
                if len(closes['BTC4h']) < timeperiod:
                    closes['BTC4h'].append(float(close))
                else:
                    closes['BTC4h'] = rotateList(closes['BTC4h'],1)
                    closes['BTC4h'][-1] = float(close)
                    SMAs['BTC4h'] = sum(closes['BTC4h']) / float(len(closes['BTC4h']))
                    EMAs["BTC4h"] = (talib.EMA(np.array(closes['BTC4h']), timeperiod = timeperiod))[-1]
                    MACDs['BTC4h'] = (talib.EMA(np.array(closes['BTC4h']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BTC4h']), timeperiod = timeperiod))[-1]
                    RSIs['BTC4h'] = (talib.RSI(np.array(closes['BTC4h']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BTC4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BTC4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BTC4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BTC4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BTC4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BTC4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BTC4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BTC4h']:
                                sellOrder(strat, float(close))
            elif '1d' in ws.url:
                if len(closes['BTC1d']) < timeperiod:
                    closes['BTC1d'].append(float(close))
                else:
                    closes['BTC1d'] = rotateList(closes['BTC1d'],1)
                    closes['BTC1d'][-1] = float(close)
                    SMAs['BTC1d'] = sum(closes['BTC1d']) / float(len(closes['BTC1d']))
                    EMAs["BTC1d"] = (talib.EMA(np.array(closes['BTC1d']), timeperiod = timeperiod))[-1]
                    MACDs['BTC1d'] = (talib.EMA(np.array(closes['BTC1d']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BTC1d']), timeperiod = timeperiod))[-1]
                    RSIs['BTC1d'] = (talib.RSI(np.array(closes['BTC1d']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BTC1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BTC1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BTC1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BTC1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BTC1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BTC1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BTC1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BTC1d']:
                                sellOrder(strat, float(close))

        elif 'eth' in ws.url:
            if '1m' in ws.url:
                if len(closes['ETH1m']) < timeperiod:
                    closes['ETH1m'].append(float(close))
                else:
                    closes['ETH1m'] = rotateList(closes['ETH1m'],1)
                    closes['ETH1m'][-1] = float(close)
                    SMAs['ETH1m'] = sum(closes['ETH1m']) / float(len(closes['ETH1m']))
                    EMAs["ETH1m"] = (talib.EMA(np.array(closes['ETH1m']), timeperiod = timeperiod))[-1]
                    MACDs['ETH1m'] = (talib.EMA(np.array(closes['ETH1m']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ETH1m']), timeperiod = timeperiod))[-1]
                    RSIs['ETH1m'] = (talib.RSI(np.array(closes['ETH1m']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ETH1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ETH1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ETH1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ETH1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ETH1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ETH1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ETH1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ETH1m']:
                                sellOrder(strat, float(close))
            elif '5m' in ws.url:
                if len(closes['ETH5m']) < timeperiod:
                    closes['ETH5m'].append(float(close))
                else:
                    closes['ETH5m'] = rotateList(closes['ETH5m'],1)
                    closes['ETH5m'][-1] = close
                    SMAs['ETH5m'] = sum(closes['ETH5m']) / float(len(closes['ETH5m']))
                    EMAs["ETH5m"] = (talib.EMA(np.array(closes['ETH5m']), timeperiod = timeperiod))[-1]
                    MACDs['ETH5m'] = (talib.EMA(np.array(closes['ETH5m']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ETH5m']), timeperiod = timeperiod))[-1]
                    RSIs['ETH5m'] = (talib.RSI(np.array(closes['ETH5m']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ETH5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ETH5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ETH5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ETH5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ETH5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ETH5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ETH5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ETH5m']:
                                sellOrder(strat, float(close))
            elif '1h' in ws.url:
                if len(closes['ETH1h']) < timeperiod:
                    closes['ETH1h'].append(float(close))
                else:
                    closes['ETH1h'] = rotateList(closes['ETH1h'],1)
                    closes['ETH1h'][-1] = close
                    SMAs['ETH1h'] = sum(closes['ETH1h']) / float(len(closes['ETH1h']))
                    EMAs["ETH1h"] = (talib.EMA(np.array(closes['ETH1h']), timeperiod = timeperiod))[-1]
                    MACDs['ETH1h'] = (talib.EMA(np.array(closes['ETH1h']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ETH1h']), timeperiod = timeperiod))[-1]
                    RSIs['ETH1h'] = (talib.RSI(np.array(closes['ETH1h']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ETH1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ETH1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ETH1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ETH1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ETH1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ETH1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ETH1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ETH1h']:
                                sellOrder(strat, float(close))
            elif '4h' in ws.url:
                if len(closes['ETH4h']) < timeperiod:
                    closes['ETH4h'].append(float(close))
                else:
                    closes['ETH4h'] = rotateList(closes['ETH4h'],1)
                    closes['ETH4h'][-1] = float(close)
                    SMAs['ETH4h'] = sum(closes['ETH4h']) / float(len(closes['ETH4h']))
                    EMAs["ETH4h"] = (talib.EMA(np.array(closes['ETH4h']), timeperiod = timeperiod))[-1]
                    MACDs['ETH4h'] = (talib.EMA(np.array(closes['ETH4h']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ETH4h']), timeperiod = timeperiod))[-1]
                    RSIs['ETH4h'] = (talib.RSI(np.array(closes['ETH4h']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ETH4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ETH4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ETH4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ETH4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ETH4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ETH4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ETH4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ETH4h']:
                                sellOrder(strat, float(close))
            elif '1d' in ws.url:
                if len(closes['ETH1d']) < timeperiod:
                    closes['ETH1d'].append(float(close))
                else:
                    closes['ETH1d'] = rotateList(closes['ETH1d'],1)
                    closes['ETH1d'][-1] = float(close)
                    SMAs['ETH1d'] = sum(closes['ETH1d']) / float(len(closes['ETH1d']))
                    EMAs["ETH1d"] = (talib.EMA(np.array(closes['ETH1d']), timeperiod = timeperiod))[-1]
                    MACDs['ETH1d'] = (talib.EMA(np.array(closes['ETH1d']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ETH1d']), timeperiod = timeperiod))[-1]
                    RSIs['ETH1d'] = (talib.RSI(np.array(closes['ETH1d']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ETH1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ETH1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ETH1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ETH1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ETH1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ETH1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ETH1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ETH1d']:
                                sellOrder(strat, float(close))

        elif 'bnb' in ws.url:
            if '1m' in ws.url:
                if len(closes['BNB1m']) < timeperiod:
                    closes['BNB1m'].append(float(close))
                else:
                    closes['BNB1m'] = rotateList(closes['BNB1m'],1)
                    closes['BNB1m'][-1] = float(close)
                    SMAs['BNB1m'] = sum(closes['BNB1m']) / float(len(closes['BNB1m']))
                    EMAs["BNB1m"] = (talib.EMA(np.array(closes['BNB1m']), timeperiod = timeperiod))[-1]
                    MACDs['BNB1m'] = (talib.EMA(np.array(closes['BNB1m']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BNB1m']), timeperiod = timeperiod))[-1]
                    RSIs['BNB1m'] = (talib.RSI(np.array(closes['BNB1m']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BNB1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BNB1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BNB1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BNB1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BNB1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BNB1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BNB1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BNB1m']:
                                sellOrder(strat, float(close))
            elif '5m' in ws.url:
                if len(closes['BNB5m']) < timeperiod:
                    closes['BNB5m'].append(float(close))
                else:
                    closes['BNB5m'] = rotateList(closes['BNB5m'],1)
                    closes['BNB5m'][-1] = float(close)
                    SMAs['BNB5m'] = sum(closes['BNB5m']) / float(len(closes['BNB5m']))
                    EMAs["BNB5m"] = (talib.EMA(np.array(closes['BNB5m']), timeperiod = timeperiod))[-1]
                    MACDs['BNB5m'] = (talib.EMA(np.array(closes['BNB5m']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BNB5m']), timeperiod = timeperiod))[-1]
                    RSIs['BNB5m'] = (talib.RSI(np.array(closes['BNB5m']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BNB5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BNB5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BNB5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BNB5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BNB5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BNB5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BNB5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BNB5m']:
                                sellOrder(strat, float(close))
            elif '1h' in ws.url:
                if len(closes['BNB1h']) < timeperiod:
                    closes['BNB1h'].append(float(close))
                else:
                    closes['BNB1h'] = rotateList(closes['BNB1h'],1)
                    closes['BNB1h'][-1] = float(close)
                    SMAs['BNB1h'] = sum(closes['BNB1h']) / float(len(closes['BNB1h']))
                    EMAs["BNB1h"] = (talib.EMA(np.array(closes['BNB1h']), timeperiod = timeperiod))[-1]
                    MACDs['BNB1h'] = (talib.EMA(np.array(closes['BNB1h']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BNB1h']), timeperiod = timeperiod))[-1]
                    RSIs['BNB1h'] = (talib.RSI(np.array(closes['BNB1h']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BNB1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BNB1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BNB1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BNB1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BNB1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BNB1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BNB1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BNB1h']:
                                sellOrder(strat, float(close))
            elif '4h' in ws.url:
                if len(closes['BNB4h']) < timeperiod:
                    closes['BNB4h'].append(float(close))
                else:
                    closes['BNB4h'] = rotateList(closes['BNB4h'],1)
                    closes['BNB4h'][-1] = float(close)
                    SMAs['BNB4h'] = sum(closes['BNB4h']) / float(len(closes['BNB4h']))
                    EMAs["BNB4h"] = (talib.EMA(np.array(closes['BNB4h']), timeperiod = timeperiod))[-1]
                    MACDs['BNB4h'] = (talib.EMA(np.array(closes['BNB4h']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BNB4h']), timeperiod = timeperiod))[-1]
                    RSIs['BNB4h'] = (talib.RSI(np.array(closes['BNB4h']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BNB4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BNB4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BNB4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BNB4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BNB4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BNB4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BNB4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BNB4h']:
                                sellOrder(strat, float(close))
            elif '1d' in ws.url:
                if len(closes['BNB1d']) < timeperiod:
                    closes['BNB1d'].append(float(close))
                else:
                    closes['BNB1d'] = rotateList(closes['BNB1d'],1)
                    closes['BNB1d'][-1] = float(close)
                    SMAs['BNB1d'] = sum(closes['BNB1d']) / float(len(closes['BNB1d']))
                    EMAs["BNB1d"] = (talib.EMA(np.array(closes['BNB1d']), timeperiod = timeperiod))[-1]
                    MACDs['BNB1d'] = (talib.EMA(np.array(closes['BNB1d']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['BNB1d']), timeperiod = timeperiod))[-1]
                    RSIs['BNB1d'] = (talib.RSI(np.array(closes['BNB1d']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['BNB1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['BNB1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['BNB1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['BNB1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['BNB1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['BNB1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['BNB1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['BNB1d']:
                                sellOrder(strat, float(close))

        elif 'zil' in ws.url:
            if '1m' in ws.url:
                if len(closes['ZIL1m']) < timeperiod:
                    closes['ZIL1m'].append(float(close))
                else:
                    closes['ZIL1m'] = rotateList(closes['ZIL1m'],1)
                    closes['ZIL1m'][-1] = float(close)
                    SMAs['ZIL1m'] = sum(closes['ZIL1m']) / float(len(closes['ZIL1m']))
                    EMAs["ZIL1m"] = (talib.EMA(np.array(closes['ZIL1m']), timeperiod = timeperiod))[-1]
                    MACDs['ZIL1m'] = (talib.EMA(np.array(closes['ZIL1m']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ZIL1m']), timeperiod = timeperiod))[-1]
                    RSIs['ZIL1m'] = (talib.RSI(np.array(closes['ZIL1m']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ZIL1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ZIL1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ZIL1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ZIL1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ZIL1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ZIL1m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ZIL1m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ZIL1m']:
                                sellOrder(strat, float(close))
            elif '5m' in ws.url:
                if len(closes['ZIL5m']) < timeperiod:
                    closes['ZIL5m'].append(float(close))
                else:
                    closes['ZIL5m'] = rotateList(closes['ZIL5m'],1)
                    closes['ZIL5m'][-1] = float(close)
                    SMAs['ZIL5m'] = sum(closes['ZIL5m']) / float(len(closes['ZIL5m']))
                    EMAs["ZIL5m"] = (talib.EMA(np.array(closes['ZIL5m']), timeperiod = timeperiod))[-1]
                    MACDs['ZIL5m'] = (talib.EMA(np.array(closes['ZIL5m']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ZIL5m']), timeperiod = timeperiod))[-1]
                    RSIs['ZIL5m'] = (talib.RSI(np.array(closes['ZIL5m']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ZIL5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ZIL5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ZIL5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ZIL5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ZIL5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ZIL5m']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ZIL5m']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ZIL5m']:
                                sellOrder(strat, float(close))
            elif '1h' in ws.url:
                if len(closes['ZIL1h']) < timeperiod:
                    closes['ZIL1h'].append(float(close))
                else:
                    closes['ZIL1h'] = rotateList(closes['ZIL1h'],1)
                    closes['ZIL1h'][-1] = float(close)
                    SMAs['ZIL1h'] = sum(closes['ZIL1h']) / float(len(closes['ZIL1h']))
                    EMAs["ZIL1h"] = (talib.EMA(np.array(closes['ZIL1h']), timeperiod = timeperiod))[-1]
                    MACDs['ZIL1h'] = (talib.EMA(np.array(closes['ZIL1h']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ZIL1h']), timeperiod = timeperiod))[-1]
                    RSIs['ZIL1h'] = (talib.RSI(np.array(closes['ZIL1h']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ZIL1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ZIL1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ZIL1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ZIL1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ZIL1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ZIL1h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ZIL1h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ZIL1h']:
                                sellOrder(strat, float(close))
            elif '4h' in ws.url:
                if len(closes['ZIL4h']) < timeperiod:
                    closes['ZIL4h'].append(float(close))
                else:
                    closes['ZIL4h'] = rotateList(closes['ZIL4h'],1)
                    closes['ZIL4h'][-1] = float(close)
                    SMAs['ZIL4h'] = sum(closes['ZIL4h']) / float(len(closes['ZIL4h']))
                    EMAs["ZIL4h"] = (talib.EMA(np.array(closes['ZIL4h']), timeperiod = timeperiod))[-1]
                    MACDs['ZIL4h'] = (talib.EMA(np.array(closes['ZIL4h']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ZIL4h']), timeperiod = timeperiod))[-1]
                    RSIs['ZIL4h'] = (talib.RSI(np.array(closes['ZIL4h']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ZIL4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ZIL4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ZIL4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ZIL4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ZIL4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ZIL4h']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ZIL4h']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ZIL4h']:
                                sellOrder(strat, float(close))
            elif '1d' in ws.url:
                if len(closes['ZIL1d']) < timeperiod:
                    closes['ZIL1d'].append(float(close))
                else:
                    closes['ZIL1d'] = rotateList(closes['ZIL1d'],1)
                    closes['ZIL1d'][-1] = float(close)
                    SMAs['ZIL1d'] = sum(closes['ZIL1d']) / float(len(closes['ZIL1d']))
                    EMAs["ZIL1d"] = (talib.EMA(np.array(closes['ZIL1d']), timeperiod = timeperiod))[-1]
                    MACDs['ZIL1d'] = (talib.EMA(np.array(closes['ZIL1d']), timeperiod = timeperiodSmall))[-1] - (talib.EMA(np.array(closes['ZIL1d']), timeperiod = timeperiod))[-1]
                    RSIs['ZIL1d'] = (talib.RSI(np.array(closes['ZIL1d']), timeperiod=rsiperiod))[-1]
                    for strat in stratsBTC:
                        if strat['buyConditions']['indicator'] == 'SMA':
                            if int(strat['buyConditions']['targetValue']) >= SMAs['ZIL1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= SMAs['ZIL1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'EMA':
                            if int(strat['buyConditions']['targetValue']) >= EMAs['ZIL1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= EMAs['ZIL1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'MACD':
                            if int(strat['buyConditions']['targetValue']) >= MACDs['ZIL1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= MACDs['ZIL1d']:
                                sellOrder(strat, float(close))
                        if strat['buyConditions']['indicator'] == 'RSI':
                            if int(strat['buyConditions']['targetValue']) >= RSIs['ZIL1d']:
                                buyOrder(strat, float(close))
                            if int(strat['sellConditions']['targetValue']) <= RSIs['ZIL1d']:
                                sellOrder(strat, float(close))
        print(len(closes['BTC1m']), closes['BTC1m'], SMAs['BTC1m'],EMAs['BTC1m'],MACDs['BTC1m'],RSIs['BTC1m'])

threads = []
sockets = []        
def main():
    initiateStrats()
    global threads, sockets

    for socket in websockets:
        ws = websocket.WebSocketApp(websockets[socket], on_open = on_open, on_message = on_message, on_close = on_close)
        sockets.append(ws)
        wst = Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        threads.append(wst)

    time.sleep(120)

    for ws in sockets:
        ws.close()

    for thread in threads:
        thread.join()

    threads = []
    sockets = []
    main()

if __name__ == "__main__":
    main()