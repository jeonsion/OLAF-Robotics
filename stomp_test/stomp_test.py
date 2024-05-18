import stomp

# 연결할 서버 정보
HOST = 'localhost'
PORT = 8082
WS_PATH = '/ws'
SUBSCRIPTION_URL = '/sub/channel/eddy'

# STOMP 클라이언트 ID
CLIENT_ID = 'stomp-python-client'

# STOMP 서버 연결을 위한 URL
CONNECT_URL = f'ws://{HOST}:{PORT}{WS_PATH}'

class StompClient(stomp.ConnectionListener):
    def on_message(self, headers, body):
        print(f"Received message: {body}")

# STOMP 클라이언트 생성
conn = stomp.Connection([(HOST, PORT)])

# 이벤트 리스너 설정
conn.set_listener(CLIENT_ID, StompClient())

# 연결 및 구독
conn.connect(wait=True)
conn.subscribe(destination=SUBSCRIPTION_URL, id=1, ack='auto')

# 연결 유지를 위해 대기
while True:
    pass

# 연결 종료
conn.disconnect()
