def on_open(ws):
    print("opened connection")

def on_close(ws):
    print("closed connection")

def on_message(ws, message):

    #print("recieved message")
    json_message = json.loads(message)
    #print(json_message)
    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']
    volume = candle['v']
    high = candle['h']
    low = candle['l']

    if is_candle_closed:
        print("candlestick closed at {}".format(close))

socketbtc1m = websocket.WebSocketApp(websockets['SOCKETBTC1M'], on_open=on_open,
                            on_close=on_close, on_message=on_message)
socketbtc1m.run_forever()