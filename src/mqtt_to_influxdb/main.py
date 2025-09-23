# import json
# from datetime import datetime

# from config import AppConfig
# from influx_client import InfluxWriter
# from logger import getLogger
# from mqtt_client import MQTTClient

# logger = getLogger(__name__)


# def on_mqtt_message(writer: InfluxWriter, measurement: str):
#     def handler(client, userdata, msg):
#         logger.info(f"Received MQTT message on {msg.topic}: {msg.payload}")
#         try:
#             payload = msg.payload.decode()
#             try:
#                 data = json.loads(payload)
#             except Exception:
#                 data = {"raw": payload}
#             tags = {"topic": msg.topic}
#             fields = {k: v for k, v in data.items() if isinstance(v, (int, float, str))}
#             writer.write(measurement, tags, fields, datetime.utcnow())
#             logger.info(f"Written to InfluxDB: {msg.topic} {fields}")
#         except Exception as e:
#             logger.error(f"Error processing message: {e}")

#     return handler


# def main():
#     config = AppConfig()
#     logger.info("Starting MQTT to InfluxDB bridge...")

#     writer = InfluxWriter(
#         url=config.INFLUX_URL,
#         token=config.INFLUX_TOKEN,
#         org=config.INFLUX_ORG,
#         bucket=config.INFLUX_BUCKET,
#     )

#     mqtt = MQTTClient(
#         host=config.MQTT_HOST,
#         port=config.MQTT_PORT,
#         username=config.MQTT_USERNAME,
#         password=config.MQTT_PASSWORD,
#     )
#     mqtt.connect()
#     # for topic in config.MQTT_TOPICS.split(","):
#     mqtt.subscribe("smartgrid/#", on_mqtt_message(writer, "telemetry"))

#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         mqtt.disconnect()
#         logger.info("Shutting down.")


# if __name__ == "__main__":
#     main()


import os
import time

from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "smartgrid"
url = "http://127.0.0.1:8086"
token = "zitFapF3vtTqLmgwETwW0bDNpKlHT5fG6r6N1yRHjtHJnaXmxCqxb9Ky5R-GvRbNjILtzG1ORUiwK6dvDtsndw=="

write_client = InfluxDBClient(url=url, token=token, org=org)

bucket = "telemetry"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
    point = Point("measurement1").tag("tagname1", "tagvalue1").field("field1", value)
    write_api.write(bucket=bucket, org="smartgrid", record=point)
    print(f"Wrote point with field1={value}")
    time.sleep(1)  # separate points by 1 second
