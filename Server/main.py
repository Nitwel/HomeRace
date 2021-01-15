import paho.mqtt.client as mqtt
import time

startTime = 0
endTime = 0

def t(time):
    return round(time * 1000)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/home/data")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if "pong" in str(msg.payload):
        endTime = time.time()
        print("From %s to %s | took %s" % (t(startTime), t(endTime), t(endTime - startTime)))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("race", "race")

client.connect("192.168.0.47")


client.loop_start()

while True:
    input("Press")
    startTime = time.time()
    client.publish("/home/data", "ping")