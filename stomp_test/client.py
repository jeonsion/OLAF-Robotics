import socketio

# Socket.IO 클라이언트 생성
sio = socketio.Client()

# 연결 이벤트 핸들러
@sio.event
def connect():
    print('서버에 연결되었습니다.')

    # 서버로 메시지 전송
    sio.emit('message', '안녕하세요!')

# 메시지 이벤트 핸들러
@sio.event
def message(data):
    print('서버로부터 메시지 수신:', data)

# 서버에 연결
sio.connect('http://localhost:8000')

# 서버로부터 메시지 수신 대기
sio.wait()