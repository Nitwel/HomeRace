import paho.mqtt.client as mqtt
import time

def t(self, time):
    return round(time * 1000)

class MQTT:
    def __init__(self, ip = "192.168.0.47", user = "race", pw = "race"):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.username_pw_set(user, pw)

        client.connect(ip)

        self.startTime = 0
        self.endTime = 0

        self.messages = []

        client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("/home/data")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        if "pong" in str(msg.payload):
            self.endTime = time.time()
            print("From %s to %s | took %s" % (t(self.startTime), t(self.endTime), t(self.endTime - self.startTime)))
