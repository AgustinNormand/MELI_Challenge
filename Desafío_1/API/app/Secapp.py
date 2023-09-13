from fastapi import HTTPException, Header, APIRouter
from pydantic import BaseModel
from datetime import datetime
import os
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from app.initializer import Initializer
import logging

class StateChange(BaseModel):
    current_status: int
    Change_at: datetime

class Secapp():
    def __init__(self, config=None):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()

        self.config = config

        self.client = InfluxDBClient(url=self.get_config("INFLUXDB_URL"),
                                     token=self.get_config("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"),
                                     org=self.get_config("INFLUXDB_ORG"), debug=False)

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

        self.initialize_values()

        self.router = APIRouter()
        self.router.add_api_route("/secapp/update", self.get_last_state, methods=["GET"])
        self.router.add_api_route("/secapp/update", self.update_state, methods=["POST"])

    def get_config(self, key):
        if self.config is None:
            return os.getenv(key)
        else:
            return self.config[key]

    def initialize_values(self):
        initializer = Initializer(self.client, self.logger, self.config)

        self.processed_id_counter = initializer.process_id()

        self.logger.info(f"processed_id_counter: {self.processed_id_counter}")

        self.last_criticity_update_value, self.last_criticity_update_date, self.last_criticity_update_processed_id = initializer.criticity()
        logging.info(f"last_criticity_update_value: {self.last_criticity_update_value}")
        logging.info(f"last_criticity_update_date: {self.last_criticity_update_date}")
        logging.info(f"last_criticity_update_processed_id: {self.last_criticity_update_processed_id}")

        self.clients_apps_last_update_timestamps = initializer.clients_apps_last_update_timestamps()
        #logging.info(f"clients_apps_last_update_timestamps: {self.clients_apps_last_update_timestamps}")
        for app_name in self.clients_apps_last_update_timestamps.keys():
            self.logger.info(f"{app_name} - {self.clients_apps_last_update_timestamps[app_name]}")

    def register_consumer_request(self, App_name, timestamp):
        point = {
            "measurement": "requests",
            "tags": {
                "app_name": App_name
            },
            "fields": {
                "cantidad": 1
            }
        }
        self.write_api.write(bucket=self.get_config("INFLUXDB_BUCKET_CONSUMERS"), record=point, time=timestamp,
                             write_precision='s')

    def register_producer_request(self, App_name, timestamp, process_id, criticity_value):
        point = {
            "measurement": "criticity_updates",
            "time": int(timestamp),
            "tags": {
                "app_name": App_name,
                "process_id_tag": process_id,
            },
            "fields": {
                "process_id": process_id,
                "criticity_value": criticity_value
            }
        }
        self.write_api.write(bucket=self.get_config("INFLUXDB_BUCKET_PRODUCERS"), record=point, write_precision='s')

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

        self.register_consumer_request(App_name, int(time.time()))

        if self.last_criticity_update_value is None:
            return {}

        if App_name in self.clients_apps_last_update_timestamps.keys():
            self.logger.info(f"App name in keys, checking {self.clients_apps_last_update_timestamps[App_name]} {self.last_criticity_update_date}")
            if self.clients_apps_last_update_timestamps[App_name] < self.last_criticity_update_date:
                return {"current_status": self.last_criticity_update_value,
                        "status_change_id": self.last_criticity_update_processed_id,
                        "Change_at": self.last_criticity_update_date}
            else:
                return {}
        else:
            self.clients_apps_last_update_timestamps[App_name] = self.last_criticity_update_date

            return {"current_status": self.last_criticity_update_value,
                    "status_change_id": self.last_criticity_update_processed_id,
                    "Change_at": self.last_criticity_update_date}

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

        update_date = state.dict()["Change_at"]
        update_value = state.dict()["current_status"]

        self.register_producer_request(App_name, update_date.timestamp(), processed_id, update_value)

        if self.last_criticity_update_date == None or update_date > self.last_criticity_update_date:
            self.last_criticity_update_date = update_date
            self.last_criticity_update_processed_id = processed_id
            self.last_criticity_update_value = update_value

        return {"processed_id": processed_id}
