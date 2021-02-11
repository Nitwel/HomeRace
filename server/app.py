import eventlet
import socketio
import sys

from classes.mqtt import MQTT

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

mqtt = MQTT()

@sio.on('image')
def image(sid, data):
    sio.emit('image', data)
    

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('event', {'response': 'my response'})

@sio.on('ping')
def ping(sid, data):
    print('message ', data)
    return 'pong'

@sio.on('drive')
def drive(sid, data):
    print(data)
    mqtt.drive(data)

if __name__ == '__main__':
    if(len(sys.argv) > 1 and sys.argv[1] == 'dev'):
        eventlet.wsgi.server(eventlet.listen(('', 1992)), app)
    else:
        eventlet.wsgi.server(eventlet.wrap_ssl(eventlet.listen(('', 1992)), certfile='cert.crt', keyfile='private.key', server_side=True), app)