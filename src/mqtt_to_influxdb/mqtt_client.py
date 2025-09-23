from typing import Callable

from paho.mqtt import client as mqtt_client


class MQTTClient:
    def __init__(self, host, port, username="", password=""):
        self.host = host
        self.port = port
        self.client = mqtt_client.Client()
        if username and password:
            self.client.username_pw_set(username, password)
        self.connected = False

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.connected = rc == 0

    def subscribe(self, topic: str, on_message: Callable):
        self.client.subscribe(topic)
        self.client.on_message = on_message

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
