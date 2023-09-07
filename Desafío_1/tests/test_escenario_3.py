import pytest
from fastapi.testclient import TestClient
from criticity_api import Criticity_API
from fastapi import FastAPI

app = FastAPI()
criticaly_api = Criticity_API()
app.include_router(criticaly_api.router)

client = TestClient(app)

@pytest.fixture
def api_url():
    return 'http://localhost:8000/secapp/update'

def test_first_request(api_url):
    # Encabezado de ejemplo con el nombre de la aplicación
    headers = {
        "App-name": "secapp01"
    }

    # Realiza la solicitud GET al endpoint /secapp/update
    response = client.get("/secapp/update", headers=headers)

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario vacío
    assert response.json() == {}




