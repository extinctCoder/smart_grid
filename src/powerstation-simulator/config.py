from os import getenv
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        validate_by_name=False,
        case_sensitive=True,
        extra="ignore",
    )

    # Metadata (static info)
    POWER_STATION_ID: Annotated[str, Field(alias="POWER_STATION_ID")] = "ps-001"
    LOCATION: Annotated[str, Field(alias="LOCATION")] = "Dhaka, Bangladesh"
    CAPACITY_KW: Annotated[int, Field(alias="CAPACITY_KW")] = 1000

    # MQTT broker config
    MQTT_HOST: Annotated[str, Field(alias="MQTT_HOST")] = "localhost"
    MQTT_PORT: Annotated[int, Field(alias="MQTT_PORT")] = 1883
    MQTT_USERNAME: Annotated[str, Field(alias="MQTT_USERNAME")] = "extinctcoder"
    MQTT_PASSWORD: Annotated[str, Field(alias="MQTT_PASSWORD")] = "Mosquitto123456#"
    MQTT_TOPIC_PREFIX: Annotated[str, Field(alias="MQTT_TOPIC_PREFIX")] = (
        "smartgrid/powerstation"
    )

    ENABLE_WEBSOCKET: Annotated[bool, Field(alias="ENABLE_WEBSOCKET")] = False

    # Simulator settings
    PUBLISH_INTERVAL_SECONDS: Annotated[
        int, Field(alias="PUBLISH_INTERVAL_SECONDS")
    ] = 2

    STATUS_PUBLISH_INTERVAL_SECONDS: int = PUBLISH_INTERVAL_SECONDS * 2
    METADATA_PUBLISH_INTERVAL_SECONDS: int = PUBLISH_INTERVAL_SECONDS * 5


def load_power_station_configs(station_prefix: str | None = None) -> AppConfig:
    """
    Dynamically loads the config for a specific power station prefix, e.g., 'PS_001'.
    If no prefix is provided explicitly, reads from the STATION_PREFIX env var.
    """
    station_prefix = station_prefix or getenv("STATION_PREFIX")

    if not station_prefix:
        return AppConfig()  # fallback to default or global settings

    class AppConfigWithPrefix(AppConfig):
        model_config = {
            **AppConfig.model_config,
            "env_prefix": station_prefix.upper().replace("-", "_") + "_",
        }

    return AppConfigWithPrefix()
