import pytest
import requests
from fastapi.testclient import TestClient
from criticity_api import app
import json

client = TestClient(app)

@pytest.fixture
def api_url():
    return 'http://localhost:8000/secapp/update'

def test_escenario_1(api_url):
    # Encabezado de ejemplo con el nombre de la aplicación
    headers = {
        "App-name": "secapp01"
    }

    # Datos de ejemplo para la solicitud POST
    data = {
        "current_status": 5,
        "Change_at": "2017-07-21T17:32:28Z"
    }

    # Realiza la solicitud POST al endpoint /secapp/update
    response = client.post("/secapp/update", data=json.dumps(data), headers=headers)

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta incluya el campo "processed_id"
    assert "processed_id" in response.json()