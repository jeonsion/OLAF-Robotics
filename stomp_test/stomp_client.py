import socketio

# 클라이언트 인스턴스 생성
sio = socketio.AsyncClient()

async def connect():
    await sio.connect('http://localhost:5000')
    print('connection established')

@sio.on('reply')
async def on_reply(data):
    print('reply received with', data)
    await sio.disconnect()

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await connect()
    await sio.wait()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
