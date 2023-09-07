import uvicorn
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime
from itertools import count

app = FastAPI()

app_states = {}
app_last_request_time = {}
processed_id_counter = count(0)

class StateChange(BaseModel):
    current_status: int
    Change_at: datetime

class Criticity_API():
    def __init__(self):
        self.process_id = 0

    @app.get("/secapp/update", response_model=dict)
    async def get_last_state(App_name: str = Header(None)):
        if not App_name:
            raise HTTPException(status_code=400, detail="Falta el encabezado App-name")

        if App_name in app_states:
            return app_states[App_name]
        else:
            raise HTTPException(status_code=404, detail="No se encontró ningún estado para la aplicación")

    @app.post("/secapp/update", response_model=dict)
    async def update_state(state: StateChange, App_name: str = Header(None)):
        if not App_name:
            raise HTTPException(status_code=400, detail="Falta el encabezado App-name")

        # Obtener el siguiente processed_id autoincremental
        processed_id = next(processed_id_counter)

        # Almacenar el último cambio de estado con el processed_id autoincremental
        app_states[App_name] = {"current_status": state.dict()["current_status"], "status_change_id": processed_id, "Change_at": state.dict()["Change_at"]}

        # Registrar el timestamp de la solicitud
        app_last_request_time[App_name] = datetime.now()
        return {"processed_id": processed_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)