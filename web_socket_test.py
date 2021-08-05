from twelvedata import TDClient

def on_event(e):
    # do whatever is needed with data
    print(e)
    
td = TDClient(apikey="c822604c71594044b6d972cf97e9dae8")
ws = td.websocket(on_event=on_event)
ws.subscribe(['BTC/USD:Coinbase'])
ws.connect()
ws.keep_alive()