import pyrebase, json
import websocket
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

allStrats = stratsBTC = stratsETH = stratsBNB = stratsZIL = {}

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

    #print("recieved message")
    json_message = json.loads(message)
    print(json_message)
    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']
    volume = candle['v']
    high = candle['h']
    low = candle['l']

    if is_candle_closed:
        print("candlestick closed at {}".format(close))


initiateStrats()

for socket in websockets:
    print(websockets[socket])
    ws = websocket.WebSocketApp(websockets[socket], on_message = on_message, on_close = on_close)
    wst = Thread(target=ws.run_forever)
    wst.start()




