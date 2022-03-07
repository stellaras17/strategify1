import pyrebase, json
import websocket, requests
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

allStrats = stratsBTC = stratsETH = stratsBNB = stratsZIL = {}

def rotateList(l, n):
    return l[n:] + l[:n]

def initiateStrats():
    f = open('api.json')
    api = json.load(f)
    fireBaseConfig = api
    firebase = pyrebase.initialize_app(fireBaseConfig)
    db = firebase.database()
    global allStrats
    strats = db.child("strats").get()

    for user in strats.each():
        usersstrats = firebase.database().child("strats").child(user.key()).get()
        for strat in usersstrats.each():
            if strat.val()['active'] == True:
                allStrats[strat.key()] = strat.val()
    splitStrats()

def splitStrats():
    global allStrats
    for strat in allStrats:
        if allStrats[strat]['ticker'] == 'BTCUSDT':
            stratsBTC[strat] = allStrats[strat]
        elif allStrats[strat]['ticker'] == 'ETHUSDT':
            stratsETH[strat] = allStrats[strat]
        elif allStrats[strat]['ticker'] == 'BNBUSDT':
            stratsBNB[strat] = allStrats[strat]
        elif allStrats[strat]['ticker'] == 'ZILUSDT':
            stratsZIL[strat] = allStrats[strat]


def on_open(ws):
    print("opened connection")
    
def on_close(ws):
    print("closed connection")

def on_message(ws, message):
    global closes

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
                if len(closes['BTC1m']) < 14:
                    closes['BTC1m'].append(close)
                else:
                    closes['BTC1m'] = rotateList(closes['BTC1m'],1)
                    closes['BTC1m'][-1] = close
            elif '5m' in ws.url:
                if len(closes['BTC5m']) < 14:
                    closes['BTC5m'].append(close)
                else:
                    closes['BTC5m'] = rotateList(closes['BTC5m'],1)
                    closes['BTC5m'][-1] = close
            elif '1h' in ws.url:
                if len(closes['BTC1h']) < 14:
                    closes['BTC1h'].append(close)
                else:
                    closes['BTC1h'] = rotateList(closes['BTC1h'],1)
                    closes['BTC1h'][-1] = close
            elif '4h' in ws.url:
                if len(closes['BTC4h']) < 14:
                    closes['BTC4h'].append(close)
                else:
                    closes['BTC4h'] = rotateList(closes['BTC4h'],1)
                    closes['BTC4h'][-1] = close
            elif '1d' in ws.url:
                if len(closes['BTC1d']) < 14:
                    closes['BTC1d'].append(close)
                else:
                    closes['BTC1d'] = rotateList(closes['BTC1d'],1)
                    closes['BTC1d'][-1] = close

        elif 'eth' in ws.url:
            if '1m' in ws.url:
                if len(closes['ETH1m']) < 14:
                    closes['ETH1m'].append(close)
                else:
                    closes['ETH1m'] = rotateList(closes['ETH1m'],1)
                    closes['ETH1m'][-1] = close
            elif '5m' in ws.url:
                if len(closes['ETH5m']) < 14:
                    closes['ETH5m'].append(close)
                else:
                    closes['ETH5m'] = rotateList(closes['ETH5m'],1)
                    closes['ETH5m'][-1] = close
            elif '1h' in ws.url:
                if len(closes['ETH1h']) < 14:
                    closes['ETH1h'].append(close)
                else:
                    closes['ETH1h'] = rotateList(closes['ETH1h'],1)
                    closes['ETH1h'][-1] = close
            elif '4h' in ws.url:
                if len(closes['ETH4h']) < 14:
                    closes['ETH4h'].append(close)
                else:
                    closes['ETH4h'] = rotateList(closes['ETH4h'],1)
                    closes['ETH4h'][-1] = close
            elif '1d' in ws.url:
                if len(closes['ETH1d']) < 14:
                    closes['ETH1d'].append(close)
                else:
                    closes['ETH1d'] = rotateList(closes['ETH1d'],1)
                    closes['ETH1d'][-1] = close

        elif 'bnb' in ws.url:
            if '1m' in ws.url:
                if len(closes['BNB1m']) < 14:
                    closes['BNB1m'].append(close)
                else:
                    closes['BNB1m'] = rotateList(closes['BNB1m'],1)
                    closes['BNB1m'][-1] = close
            elif '5m' in ws.url:
                if len(closes['BNB5m']) < 14:
                    closes['BNB5m'].append(close)
                else:
                    closes['BNB5m'] = rotateList(closes['BNB5m'],1)
                    closes['BNB5m'][-1] = close
            elif '1h' in ws.url:
                if len(closes['BNB1h']) < 14:
                    closes['BNB1h'].append(close)
                else:
                    closes['BNB1h'] = rotateList(closes['BNB1h'],1)
                    closes['BNB1h'][-1] = close
            elif '4h' in ws.url:
                if len(closes['BNB4h']) < 14:
                    closes['BNB4h'].append(close)
                else:
                    closes['BNB4h'] = rotateList(closes['BNB4h'],1)
                    closes['BNB4h'][-1] = close
            elif '1d' in ws.url:
                if len(closes['BNB1d']) < 14:
                    closes['BNB1d'].append(close)
                else:
                    closes['BNB1d'] = rotateList(closes['BNB1d'],1)
                    closes['BNB1d'][-1] = close

        elif 'zil' in ws.url:
            if '1m' in ws.url:
                if len(closes['ZIL1m']) < 14:
                    closes['ZIL1m'].append(close)
                else:
                    closes['ZIL1m'] = rotateList(closes['ZIL1m'],1)
                    closes['ZIL1m'][-1] = close
            elif '5m' in ws.url:
                if len(closes['ZIL5m']) < 14:
                    closes['ZIL5m'].append(close)
                else:
                    closes['ZIL5m'] = rotateList(closes['ZIL5m'],1)
                    closes['ZIL5m'][-1] = close
            elif '1h' in ws.url:
                if len(closes['ZIL1h']) < 14:
                    closes['ZIL1h'].append(close)
                else:
                    closes['ZIL1h'] = rotateList(closes['ZIL1h'],1)
                    closes['ZIL1h'][-1] = close
            elif '4h' in ws.url:
                if len(closes['ZIL4h']) < 14:
                    closes['ZIL4h'].append(close)
                else:
                    closes['ZIL4h'] = rotateList(closes['ZIL4h'],1)
                    closes['ZIL4h'][-1] = close
            elif '1d' in ws.url:
                if len(closes['ZIL1d']) < 14:
                    closes['ZIL1d'].append(close)
                else:
                    closes['ZIL1d'] = rotateList(closes['ZIL1d'],1)
                    closes['ZIL1d'][-1] = close
        print(closes)
initiateStrats()

for socket in websockets:
    ws = websocket.WebSocketApp(websockets[socket], on_open = on_open, on_message = on_message, on_close = on_close)
    wst = Thread(target=ws.run_forever)
    wst.start()