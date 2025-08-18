from json import dumps
from typing import Any

from config import AppConfig
from logger import getLogger
from paho.mqtt import client as mqtt_client

logger = getLogger(__name__)


class MQTTClient:
    """
    A client for connecting to an MQTT broker and publishing/subscribing to topics.

    This class provides methods to connect to an MQTT broker, publish messages,
    subscribe to topics, and handle connection events.
    """

    def __init__(
        self,
        client_id: str,
        host: str,
        port: int,
        username: str,
        password: str,
        enable_websocket: bool,
    ):
        """
        Initialize an MQTT client.

        Args:
            client_id (str): Unique identifier for this client
            host (str): MQTT broker hostname or IP address
            port (int): MQTT broker port
            username (str): Authentication username
            password (str): Authentication password
            enable_websocket (bool): Use websockets instead of TCP if True
        """
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
        """
        Connect to the MQTT broker and start the network loop.
        """
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def disconnect(self):
        """
        Disconnect from the MQTT broker and stop the network loop.
        """
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(
        self, client: mqtt_client.Client, userdata: Any, flags: dict, rc: int
    ) -> None:
        """
        Callback for when the client connects to the broker.

        Args:
            client: The client instance
            userdata: User data of any type
            flags: Response flags sent by the broker
            rc (int): Connection result code
        """
        if rc == 0:
            self.connected = True
            logger.info(f"Connected to MQTT broker at {self.host}:{self.port}")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client: mqtt_client.Client, userdata: Any, rc: int) -> None:
        """
        Callback for when the client disconnects from the broker.

        Args:
            client: The client instance
            userdata: User data of any type
            rc (int): Disconnection result code
        """
        self.connected = False
        logger.info("Disconnected from MQTT broker")

    def publish(self, topic: str, payload: Any, qos: int = 1) -> bool:
        """
        Publish a message to a topic.

        Args:
            topic (str): The topic to publish to
            payload (Any): The message to publish (dictionaries will be JSON-encoded)
            qos (int, optional): Quality of Service level. Defaults to 1.

        Returns:
            bool: True if the message was published successfully, False otherwise
        """
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
        """
        Subscribe to a topic.

        Args:
            topic (str): The topic to subscribe to
            qos (int, optional): Quality of Service level. Defaults to 1.
            on_message (callable, optional): Callback for when a message is received.
                If None, a default handler will be used.
        """

        def __on_message(client, userdata, msg):
            logger.info(f"Received message on {msg.topic}: {msg.payload.decode()}")

        self.client.subscribe(topic, qos=qos)
        self.client.on_message = on_message or __on_message


def get_mqtt_client(app_config: AppConfig) -> MQTTClient:
    """
    Create and return an MQTT client using configuration from the application settings.

    This function initializes an MQTTClient instance with connection parameters
    extracted from the provided AppConfig object.

    Args:
        app_config (AppConfig): Application configuration containing MQTT connection settings

    Returns:
        MQTTClient: A configured MQTT client instance ready for connection
    """
    return MQTTClient(
        client_id=app_config.POWER_STATION_ID,
        host=app_config.MQTT_HOST,
        port=app_config.MQTT_PORT,
        username=app_config.MQTT_USERNAME,
        password=app_config.MQTT_PASSWORD,
        enable_websocket=app_config.ENABLE_WEBSOCKET,
    )
