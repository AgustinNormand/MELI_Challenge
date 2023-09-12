from fastapi import HTTPException, Header, APIRouter
from pydantic import BaseModel
from datetime import datetime
from itertools import count
import os
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import time

class StateChange(BaseModel):
    current_status: int
    Change_at: datetime


class Secapp():
    def __init__(self):
        self.processed_id_counter = count(1)
        self.clients_apps_last_update_timestamps = {}  # DATABASE MISSING

        client = InfluxDBClient(url=self.get_config("INFLUXDB_URL"),
                                token=self.get_config("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"),
                                org=self.get_config("INFLUXDB_ORG"), debug=True)

        self.write_api = client.write_api(write_options=SYNCHRONOUS)

        self.last_criticity_update_value = None  # DATABASE MISSING
        self.last_criticity_update_timestamp = None  # DATABASE MISSING
        self.last_criticity_update_processed_id = None  # DATABASE MISSING

        # self.clients_apps_requests_timestamps = {} # ?

        self.router = APIRouter()
        self.router.add_api_route("/secapp/update", self.get_last_state, methods=["GET"])
        self.router.add_api_route("/secapp/update", self.update_state, methods=["POST"])

    def get_config(self, key):
        return os.getenv(key)

    def register_request(self, App_name, timestamp):
        point = {
            "measurement": "requests",
            "tags": {
                "app_name": App_name
            },
            "time": timestamp,
            "fields": {
                "cantidad": 1
            }
        }
        self.write_api.write(bucket=self.get_config("INFLUXDB_BUCKET_CONSUMERS"), record=point, time=timestamp, write_precision='s')

    async def get_last_state(self,
                             App_name: str = Header(None),
                             token: str = Header(None)):

        if token != self.get_config("APIKEY"):
            raise HTTPException(
                status_code=401,
                detail="Valor incorrecto del API Token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not App_name:
            raise HTTPException(status_code=400, detail="Falta el encabezado App-name")

        self.register_request(App_name, int(time.time()))

        if self.last_criticity_update_value is None:
            return {}

        if App_name in self.clients_apps_last_update_timestamps.keys():
            if self.clients_apps_last_update_timestamps[App_name] < self.last_criticity_update_timestamp:
                return {"current_status": self.last_criticity_update_value,
                        "status_change_id": self.last_criticity_update_processed_id,
                        "Change_at": self.last_criticity_update_timestamp}
            else:
                return {}
        else:
            self.clients_apps_last_update_timestamps[App_name] = self.last_criticity_update_timestamp

            return {"current_status": self.last_criticity_update_value,
                    "status_change_id": self.last_criticity_update_processed_id,
                    "Change_at": self.last_criticity_update_timestamp}

    async def update_state(self,
                           state: StateChange,
                           App_name: str = Header(None),
                           token: str = Header(None)):

        if token != os.getenv("APIKEY"):
            raise HTTPException(
                status_code=401,
                detail="Valor incorrecto del header Token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not App_name:
            raise HTTPException(
                status_code=400,
                detail="Falta el encabezado App-name"
            )

        processed_id = next(self.processed_id_counter)

        update_timestamp = state.dict()["Change_at"].strftime("%Y-%m-%dT%H:%M:%SZ")
        update_value = state.dict()["current_status"]

        if self.last_criticity_update_timestamp == None or update_timestamp > self.last_criticity_update_timestamp:
            self.last_criticity_update_timestamp = update_timestamp
            self.last_criticity_update_processed_id = processed_id
            self.last_criticity_update_value = update_value

        return {"processed_id": processed_id}
