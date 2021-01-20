import paho.mqtt.client as mqtt
import time
import asyncio

class MQTT:
    def __init__(self, ip = "192.168.0.47", user = "race", pw = "race"):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.username_pw_set(user, pw)
        client.connect(ip)
        client.loop_start()

        self.client = client
        self.cartIps = []

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("/carts")

    def on_message(self, client, userdata, [topic, payload]):
        print(topic+" "+str(payload))

        message = str(payload)

        if topic == '/carts':
            if message == 'hey':
                self.cartIps = []

            if message.startswith('ho'):
                message = message.replace('ho', '')
                self.cartIps.append(message)
            

        if "pong" in str(msg.payload):
            print("pong")

    async def get_carts(self):
        self.client.publish('/carts', 'hey')
        await asyncio.sleep(1)
        return self.cartIps