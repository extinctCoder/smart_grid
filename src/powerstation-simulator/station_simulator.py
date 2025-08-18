from random import random
from threading import Thread
from time import sleep
from typing import Any

from config import AppConfig
from logger import getLogger
from mqtt_client import MQTTClient, get_mqtt_client

logger = getLogger(__name__)


class StationSimulator:
    metadata_topic: str = "metadata"
    output_topic: str = "output"
    status_topic: str = "status"
    control_topic: str = "control"

    def __init__(self, app_config: AppConfig):
        self.online: bool = False
        self.running: bool = False
        self.app_config: AppConfig = app_config
        self.mqqt_client: MQTTClient = get_mqtt_client(app_config=app_config)

    def startup_sequence(self):
        logger.info("Initializing StationSimulator startup-sequence...")
        self.mqqt_client.connect()
        sleep(0.01)
        self.online = True

        # Subscribe to control channel
        self.mqqt_client.subscribe(
            topic=f"{self.app_config.MQTT_TOPIC_PREFIX}/{self.app_config.POWER_STATION_ID}/{self.control_topic}",
            on_message=self.__handle_control,
        )

        # Start metadata + status loops
        self.__status_thread: Thread = Thread(target=self.__publish_status_loop)
        self.__metadata_thread: Thread = Thread(target=self.__publish_metadata_loop)
        self.__output_thread: Thread = Thread(target=self.__publish_output_loop)
        self.__status_thread.start()
        self.__metadata_thread.start()
        self.__output_thread.start()

        logger.info("StationSimulator startup-sequence COMPLETED.")

    def shutdown_sequence(self):
        logger.info("Initializing StationSimulator shutdown-sequence...")
        logger.info("!!!...PLEASE DO NOT REPEATEDLY PRESS 'Ctrl+C' ...!!!")
        self.online = False
        self.running = False
        if hasattr(self, "__status_thread") and self.__status_thread.is_alive():
            self.__status_thread.join()
        if hasattr(self, "__metadata_thread") and self.__metadata_thread.is_alive():
            self.__metadata_thread.join()
        if hasattr(self, "__output_thread") and self.__output_thread.is_alive():
            self.__output_thread.join()

        self.mqqt_client.disconnect()
        logger.info("StationSimulator shutdown-sequence COMPLETED.")

    def simulate_output(self) -> int:
        """
        Simulates the power output of the station.
        This is a placeholder for actual simulation logic.
        """
        # For now, we just return a random value between 0 and capacity
        return int(
            self.app_config.CAPACITY_KW * 0.8
            + (self.app_config.CAPACITY_KW * 0.4 * random())
        )

    def publish_metadata(self):
        self.mqqt_client.publish(
            topic=f"{self.app_config.MQTT_TOPIC_PREFIX}/{self.metadata_topic}/{self.app_config.POWER_STATION_ID}",
            payload=dict(
                location=self.app_config.LOCATION,
                capacity_kw=self.app_config.CAPACITY_KW,
            ),
        )

    def publish_status(self):
        self.mqqt_client.publish(
            topic=f"{self.app_config.MQTT_TOPIC_PREFIX}/{self.app_config.POWER_STATION_ID}/{self.status_topic}",
            payload="running" if self.running else "online",
        )

    def publish_output(self):
        self.mqqt_client.publish(
            topic=f"{self.app_config.MQTT_TOPIC_PREFIX}/{self.app_config.POWER_STATION_ID}/{self.output_topic}",
            payload=self.simulate_output() if self.running else 0,
        )

    def __publish_metadata_loop(self):
        while self.online:
            self.publish_metadata()
            sleep(self.app_config.METADATA_PUBLISH_INTERVAL_SECONDS)

    def __publish_status_loop(self):
        while self.online:
            self.publish_status()
            sleep(self.app_config.STATUS_PUBLISH_INTERVAL_SECONDS)

    def __publish_output_loop(self):
        while self.online:
            self.publish_output()
            sleep(self.app_config.PUBLISH_INTERVAL_SECONDS)

    def __handle_control(self, client: Any, userdata: Any, message: Any):
        """
        Handle incoming control messages:
        - '1' => start()
        - '0' => stop()
        """

        payload = message.payload.decode()
        logger.info(f"Control message received: {payload}")

        normalized_command = str(payload).strip()

        if normalized_command not in ("0", "1"):
            logger.warning(f"Unknown control command (expected '0' or '1'): {payload}")
            return

        self.control(is_start=normalized_command == "1")

    def control(self, is_start: bool):
        logger.info(f"StationSimulator is {'starting' if is_start else 'stopping'}...")
        self.running = is_start
        logger.info(f"StationSimulator {'started' if is_start else 'stopped'}.")
