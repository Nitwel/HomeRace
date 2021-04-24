import pickle
import struct
import socketio
import base64
import time
import cv2

sio = socketio.Client()
sio.connect('http://localhost:1992')

vid = cv2.VideoCapture(0)
fps = 30
sleep_time = 1.0 / fps

frame = 0
frameTimes = []

while True:
    start_time = time.time()
    img, image = vid.read()

    ret, buffer = cv2.imencode('.jpeg', image, [cv2.IMWRITE_JPEG_QUALITY, 30, cv2.IMWRITE_JPEG_OPTIMIZE, 0, cv2.IMWRITE_JPEG_RST_INTERVAL, 10])
    b64 = base64.b64encode(buffer).decode("ascii")
    sio.emit('image', b64)

    end_time = time.time()

    diff_time = end_time - start_time

    final_sleep_time = sleep_time - diff_time if diff_time <= sleep_time else 0
    if final_sleep_time > 0:
        time.sleep(final_sleep_time)

    frameTimes.append(final_sleep_time)

    frame += 1

    if frame >= 60:
        print("Average Frametime: %s" % (sum(frameTimes) / len(frameTimes)))
        frame = 0
        frameTimes = []

        
vid.release()
cv2.destroyAllWindows()
sio.disconnect()