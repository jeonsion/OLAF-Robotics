import socketio

# Socket.IO 서버 생성
sio = socketio.Server()

# Flask 애플리케이션 생성
app = socketio.WSGIApp(sio)

# 'connect' 이벤트 핸들러
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

# 'disconnect' 이벤트 핸들러
@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

# 'message' 이벤트 핸들러
@sio.event
def message(sid, data):
    print('Message received from client:', data)
    sio.emit('reply', 'Message received: ' + data, room=sid)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('localhost', 8000)), app)
