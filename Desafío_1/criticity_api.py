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
        self.clients_apps_requests_timestamps = {}
        self.last_criticity_update_value = None
        self.last_criticity_update_timestamp = None
        self.last_criticity_update_processed_id = None

        self.router = APIRouter()
        self.router.add_api_route("/secapp/update", self.get_last_state, methods=["GET"])

    async def get_last_state(self, App_name: str = Header(None)):
        if not App_name:
            raise HTTPException(status_code=400, detail="Falta el encabezado App-name")

        if self.last_criticity_update_value is None or \
                self.clients_apps_requests_timestamps[App_name] >= self.last_criticity_update_timestamp:
            return {}

        if App_name in self.clients_apps_requests_timestamps.keys():
            if self.clients_apps_requests_timestamps[App_name] < self.last_criticity_update_timestamp:
                return {"current_status": self.last_criticity_update_value,
                        "status_change_id": self.last_criticity_update_processed_id,
                        "Change_at": self.last_criticity_update_timestamp}
        else:
            self.clients_apps_requests_timestamps[App_name] = self.last_criticity_update_timestamp

            return {"current_status": self.last_criticity_update_value,
                    "status_change_id": self.last_criticity_update_processed_id,
                    "Change_at": self.last_criticity_update_timestamp}

    # @app.post("/secapp/update", response_model=dict)
    # async def update_state(self, state: StateChange, App_name: str = Header(None)):
    #    if not App_name:
    #        raise HTTPException(status_code=400, detail="Falta el encabezado App-name")

    # Obtener el siguiente processed_id autoincremental

    # processed_id = next(self.processed_id_counter)

    # Almacenar el último cambio de estado con el processed_id autoincremental
    # app_states[App_name] = {"current_status": state.dict()["current_status"], "status_change_id": processed_id, "Change_at": state.dict()["Change_at"]}

    # last_criticity_update_timestamp = state.dict()["Change_at"]

    # return {"processed_id": processed_id}

if __name__ == "__main__":
    app = FastAPI()
    criticaly_api = Criticity_API()
    app.include_router(criticaly_api.router)
    uvicorn.run(app, host="0.0.0.0", port=8000)
