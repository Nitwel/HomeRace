import pickle
import struct
import cv2
import socketio
import base64
import time

sio = socketio.Client()
sio.connect('http://localhost:1992')

vid = cv2.VideoCapture(0)

while True:
    img, image = vid.read()

    ret, buffer = cv2.imencode('.jpeg', image, [cv2.IMWRITE_JPEG_QUALITY, 30, cv2.IMWRITE_JPEG_OPTIMIZE, 0])
    b64 = base64.b64encode(buffer).decode("ascii")
    sio.emit('image', b64)
    
    time.sleep(1.0 / 25)
        
vid.release()
cv2.destroyAllWindows()
sio.disconnect()