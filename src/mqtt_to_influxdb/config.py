from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.sample",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # MQTT broker config
    MQTT_HOST: Annotated[str, Field()] = "127.0.0.1"
    MQTT_PORT: Annotated[int, Field()] = 1883
    MQTT_USERNAME: Annotated[str, Field()] = "extinctcoder"
    MQTT_PASSWORD: Annotated[str, Field()] = "Mosquitto123456#"
    MQTT_TOPIC: Annotated[str, Field()] = "smartgrid"

    ENABLE_WEBSOCKET: Annotated[bool, Field()] = False

    # InfluxDB config
    INFLUX_HOST: Annotated[str, Field()] = "influxdb"
    INFLUX_PORT: Annotated[int, Field()] = 8086

    INFLUX_TOKEN: Annotated[str, Field()] = "admin123"
    INFLUX_ORG: Annotated[str, Field()] = "smartgrid/#"
    INFLUX_BUCKET: Annotated[str, Field()] = "telemetry"

    INFLUX_URL: str = f"http://{INFLUX_HOST}:{INFLUX_PORT}"
