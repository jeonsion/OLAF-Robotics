import argparse
import asyncio
import websockets
import stomper

async def connect():
    ws_url = f"ws://{args.host}:{args.port}/ws"
    async with websockets.connect(ws_url) as websocket:
        # Sending a CONNECT frame to establish the STOMP connection
        await websocket.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")

        # Subscribing to the bookinfo channel
        sub_bookinfo = stomper.subscribe("/sub/channel/bookinfo", idx="bookinfo")
        await websocket.send(sub_bookinfo)

        # Infinite loop to keep the connection alive and receive messages
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="STOMP Client")
    parser.add_argument(
        "--host", default="192.168.0.106", help="Host for WebSocket server (default: 192.168.0.106)"
    )
    parser.add_argument(
        "--port", type=int, default=8082, help="Port for WebSocket server (default: 8082)"
    )

    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(connect())
