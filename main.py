from dotenv import dotenv_values
import paho.mqtt.client as mqtt
import json
config = dotenv_values(".env")


class MQTTListener:
    def __init__(self, ip, port, username, password, topic) -> None:
        self.ip = ip
        self.port = port
        self.client = mqtt.Client()
        self.username = username
        self.password = password
        self.topic = topic

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code:{rc}")

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(self.topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        data = json.loads(data)
        print(data)

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.connect(self.ip, self.port, 60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()
        
my_client = MQTTListener("93.13.93.22", 1883, config["MQTT_USER"], config["MQTT_PASS"], "test/antoine/sub")
my_client.start()
