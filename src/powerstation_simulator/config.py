from os import getenv
from typing import Annotated

from logger import getLogger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = getLogger(__name__)


class AppConfig(BaseSettings):
    """
    AppConfig is the main configuration class for the power station application.

    This class defines all the necessary configuration parameters for the application,
    including station metadata, MQTT broker settings, and simulator configurations.
    It uses Pydantic's BaseSettings for environment variable loading and validation.

    Environment variables are loaded from a .env.sample file by default.
    """

    model_config = SettingsConfigDict(
        env_file=".env.sample",
        env_file_encoding="utf-8",
        validate_by_name=False,
        case_sensitive=True,
        extra="ignore",
    )

    # Metadata (static info)
    POWER_STATION_ID: Annotated[str, Field()] = "PS_001"
    LOCATION: Annotated[str, Field()] = "Dhaka, Bangladesh"
    CAPACITY_KW: Annotated[int, Field()] = 1000

    # MQTT broker config
    MQTT_HOST: Annotated[str, Field()] = "127.0.0.1"
    MQTT_PORT: Annotated[int, Field()] = 1883
    MQTT_USERNAME: Annotated[str, Field()] = "extinctcoder"
    MQTT_PASSWORD: Annotated[str, Field()] = "Mosquitto123456#"
    MQTT_TOPIC_PREFIX: Annotated[str, Field()] = "smartgrid/powerstation"

    ENABLE_WEBSOCKET: Annotated[bool, Field()] = False

    # Simulator settings
    PUBLISH_INTERVAL_SECONDS: Annotated[int, Field()] = 1

    STATUS_PUBLISH_INTERVAL_SECONDS: int = PUBLISH_INTERVAL_SECONDS * 2
    METADATA_PUBLISH_INTERVAL_SECONDS: int = PUBLISH_INTERVAL_SECONDS * 5


def load_power_station_configs(station_prefix: str | None = None) -> AppConfig:
    """
    Dynamically loads the config for a specific power station prefix, e.g., 'PS_001'.
    If no prefix is provided explicitly, reads from the STATION_PREFIX env var.
    """
    station_prefix = station_prefix or getenv("STATION_PREFIX")

    logger.info(f"Simple Power Station SIMULATOR serving station : {station_prefix}")

    if not station_prefix:
        return AppConfig()  # fallback to default or global settings

    class AppConfigWithPrefix(AppConfig):
        model_config = {
            **AppConfig.model_config,
            "env_prefix": station_prefix.upper().replace("-", "_") + "_",
        }

    return AppConfigWithPrefix()
