from json import dumps
from typing import Any

from paho.mqtt import client as mqtt_client

from config import AppConfig
from logger import getLogger

logger = getLogger(__name__)


class MQTTClient:
    def __init__(
        self,
        client_id: str,
        host: str,
        port: int,
        username: str,
        password: str,
        enable_websocket: bool,
    ):
        self.host: str = host
        self.port: int = port
        self.connected: bool = False

        self.client: mqtt_client.Client = mqtt_client.Client(
            client_id=client_id,
            transport="websockets" if enable_websocket else "tcp",
        )
        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def connect(self):
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(
        self, client: mqtt_client.Client, userdata: Any, flags: dict, rc: int
    ) -> None:
        if rc == 0:
            self.connected = True
            logger.info(f"Connected to MQTT broker at {self.host}:{self.port}")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client: mqtt_client.Client, userdata: Any, rc: int) -> None:
        self.connected = False
        logger.info("Disconnected from MQTT broker")

    def publish(self, topic: str, payload: Any, qos: int = 1) -> bool:
        if not self.connected:
            logger.warning("MQTT client not connected. Cannot publish.")
            return False

        result = self.client.publish(
            topic=topic,
            payload=dumps(payload) if isinstance(payload, dict) else payload,
            qos=qos,
        )

        if not result.rc:
            logger.debug(f"Published to topic {topic}: {payload}")
            return True
        logger.error(f"Failed to publish to topic {topic}")
        return False

    def subscribe(
        self, topic: str, qos: int = 1, on_message: Any | None = None
    ) -> None:
        def __on_message(client, userdata, msg):
            logger.info(f"Received message on {msg.topic}: {msg.payload.decode()}")

        self.client.subscribe(topic, qos=qos)
        self.client.on_message = on_message or __on_message


def get_mqtt_client(app_config: AppConfig) -> MQTTClient:
    return MQTTClient(
        client_id=app_config.POWER_STATION_ID,
        host=app_config.MQTT_HOST,
        port=app_config.MQTT_PORT,
        username=app_config.MQTT_USERNAME,
        password=app_config.MQTT_PASSWORD,
        enable_websocket=app_config.ENABLE_WEBSOCKET,
    )
