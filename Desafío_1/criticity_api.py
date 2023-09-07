import uvicorn
from fastapi import FastAPI, HTTPException, Header, APIRouter
from pydantic import BaseModel
from datetime import datetime
from itertools import count


class StateChange(BaseModel):
    current_status: int
    Change_at: datetime

class Criticity_API():
    def __init__(self):
        self.processed_id_counter = count(0)
        self.clients_apps_last_update_timestamps = {}
        self.last_criticity_update_value = None
        self.last_criticity_update_timestamp = None
        self.last_criticity_update_processed_id = None

        self.clients_apps_requests_timestamps = {}

        self.router = APIRouter()
        self.router.add_api_route("/secapp/update", self.get_last_state, methods=["GET"])
        self.router.add_api_route("/secapp/update", self.update_state, methods=["POST"])

    async def get_last_state(self, App_name: str = Header(None)):
        if not App_name:
            raise HTTPException(status_code=400, detail="Falta el encabezado App-name")

        self.clients_apps_requests_timestamps[App_name] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

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

    async def update_state(self, state: StateChange, App_name: str = Header(None)):
        if not App_name:
            raise HTTPException(status_code=400, detail="Falta el encabezado App-name")

        processed_id = next(self.processed_id_counter)

        update_timestamp = state.dict()["Change_at"].strftime("%Y-%m-%dT%H:%M:%SZ")
        update_value = state.dict()["current_status"]

        if self.last_criticity_update_timestamp == None or update_timestamp > self.last_criticity_update_timestamp:
            self.last_criticity_update_timestamp = update_timestamp
            self.last_criticity_update_processed_id = processed_id
            self.last_criticity_update_value = update_value

        return {"processed_id": processed_id}


if __name__ == "__main__":
    app = FastAPI()
    criticaly_api = Criticity_API()
    app.include_router(criticaly_api.router)
    uvicorn.run(app, host="0.0.0.0", port=8000)
