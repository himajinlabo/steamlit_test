import asyncio
import websockets
import json

# GMOコインのWebSocket APIエンドポイント
GMO_URI = "wss://api.coin.z.com/ws/public/v1"

# bitbankのWebSocket APIエンドポイント
BITBANK_URI = "wss://stream.bitbank.cc/socket.io/?EIO=3&transport=websocket"

# 価格情報を格納する辞書
prices = {
    "GMO": None,
    "bitbank": None
}

async def subscribe_to_gmo():
    async with websockets.connect(GMO_URI) as ws:
        # GMOコインのチャネル購読リクエスト
        await ws.send(json.dumps({"command": "subscribe", "channel": "ticker", "symbol": "BTC_JPY"}))
        while True:
            response = await ws.recv()
            data = json.loads(response)
            if 'data' in data:
                prices["GMO"] = data['data']['ltp']
                print_prices()

async def subscribe_to_bitbank():
    async with websockets.connect(BITBANK_URI) as ws:
        # bitbankのチャネル購読リクエスト
        await ws.send('42["subscribe", "ticker_btc_jpy"]')
        while True:
            response = await ws.recv()
            if response.startswith('42') and 'ticker' in response:
                response_json = json.loads(response.lstrip('42'))
                if response_json[0] == 'ticker':
                    prices["bitbank"] = response_json[1]['last']
                    print_prices()

def print_prices():
    if prices["GMO"] and prices["bitbank"]:
        print(f"GMO: {prices['GMO']}, bitbank: {prices['bitbank']}")

async def main():
    await asyncio.gather(
        subscribe_to_gmo(),
        subscribe_to_bitbank(),
    )

# 非同期イベントループを実行
async def main():
    await asyncio.gather(
        subscribe_to_gmo(),
        subscribe_to_bitbank(),
    )

# 既存のイベントループを取得し、コルーチンを実行
loop = asyncio.get_event_loop()

# 既にイベントループが実行中の場合のための処理
if loop.is_running():
    # 非同期タスクをスケジュールする別の方法
    asyncio.ensure_future(main())
else:
    # イベントループが実行中でない場合は、通常通りコルーチンを実行
    loop.run_until_complete(main())
