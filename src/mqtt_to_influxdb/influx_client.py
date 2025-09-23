from datetime import datetime

from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.domain.write_precision import WritePrecision


class InfluxWriter:
    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket
        self.org = org

    def write(self, measurement, tags, fields, timestamp=None):
        point = Point(measurement)
        for k, v in tags.items():
            point = point.tag(k, v)
        for k, v in fields.items():
            point = point.field(k, v)
        point = point.time(timestamp or datetime.utcnow(), WritePrecision.NS)
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)
