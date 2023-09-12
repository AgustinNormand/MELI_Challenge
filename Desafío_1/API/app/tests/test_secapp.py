import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
import json
from app.Secapp import Secapp


def client_setup():
    app = FastAPI()
    secapp = Secapp()
    app.include_router(secapp.router)

    client = TestClient(app)
    return client


def set_state(client, app_name, current_status, timestamp):

    # Encabezado de ejemplo con el nombre de la aplicación
    headers = {
        "App-name": app_name
    }

    # Datos de ejemplo para la solicitud POST
    data = {
        "current_status": current_status,
        "Change_at": timestamp
    }

    # Realiza la solicitud POST al endpoint /secapp/update
    response = client.post("/secapp/update", data=json.dumps(data), headers=headers)

    return response


def get_state(client, app_name):
    # Encabezado de ejemplo con el nombre de la aplicación
    headers = {
        "App-name": app_name
    }

    # Realiza la solicitud GET al endpoint /secapp/update
    response = client.get("/secapp/update", headers=headers)

    return response


def test_first_request():
    # Configuro el cliente de prueba
    client = client_setup()

    # Consulto el estado de criticidad
    response = get_state(client, "secapp01")

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario vacío
    assert response.json() == {}


def test_escenario_1():
    # Configuro el cliente de prueba
    client = client_setup()

    # Consulto el estado de criticidad
    response = set_state(client, "secapp01", 5, "2017-07-21T17:32:28Z")

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta incluya el campo "processed_id"
    assert "processed_id" in response.json()


def test_escenario_2():
    # Configuro el cliente de prueba
    client = client_setup()

    timestamp = "2018-07-21T17:32:28Z"
    current_state = 5

    # Establezco el estado de criticidad
    response = set_state(client, "secapp01", current_state, timestamp)

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta incluya el campo "processed_id"
    assert "processed_id" in response.json()

    process_id = response.json()["processed_id"]

    # Consulto el estado de criticidad
    response = get_state(client, "secapp02")

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario con los datos correctos
    assert response.json() == {"current_status": current_state, "status_change_id": process_id, "Change_at": timestamp}


def test_escenario_3():
    # Configuro el cliente de prueba
    client = client_setup()

    timestamp = "2019-07-21T17:32:28Z"
    current_state = 5

    # Establezco el estado de criticidad
    response = set_state(client, "secapp01", current_state, timestamp)

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta incluya el campo "processed_id"
    assert "processed_id" in response.json()

    process_id = response.json()["processed_id"]

    response = get_state(client, "secapp02")

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario con los datos correctos
    assert response.json() == {"current_status": current_state, "status_change_id": process_id, "Change_at": timestamp}

    response = get_state(client, "secapp02")

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario vacío
    assert response.json() == {}
