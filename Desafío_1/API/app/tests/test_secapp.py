import json
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def set_state(app_name, current_status, timestamp):
    # Encabezado de ejemplo con el nombre de la aplicación
    headers = {
        "App-name": app_name,
        "Token": os.getenv("APIKEY")
    }

    # Datos de ejemplo para la solicitud POST
    data = {
        "current_status": current_status,
        "Change_at": timestamp
    }

    # Realiza la solicitud POST al endpoint /secapp/update
    #response = client.post("/secapp/update", data=json.dumps(data), headers=headers)
    response = requests.post(url=os.getenv("API_URL"), headers=headers, json=data)

    return response


def get_state(app_name):
    # Encabezado de ejemplo con el nombre de la aplicación
    headers = {
        "App-name": app_name,
        "Token": os.getenv("APIKEY")
    }

    # Realiza la solicitud GET al endpoint /secapp/update
    #response = client.get("/secapp/update", headers=headers)
    response = requests.get(url=os.getenv("API_URL"), headers=headers)

    return response


def test_escenario_1():
    # Obtengo la fecha y hora actual
    actual_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Establezco el estado de criticidad
    response = set_state("test_secapp01", 5, actual_datetime)

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta incluya el campo "processed_id"
    assert "processed_id" in response.json()


def test_escenario_2():
    # Obtengo la fecha y hora actual
    actual_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Guardo el estado de criticidad para posterior uso
    current_state = 5

    # Establezco el estado de criticidad
    response = set_state("test_secapp01", current_state, actual_datetime)

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta incluya el campo "processed_id"
    assert "processed_id" in response.json()

    # Guardo el ID para posterior uso
    process_id = response.json()["processed_id"]

    # Consulto el estado de criticidad
    response = get_state("test_secapp02")

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario con los datos correctos
    assert response.json() == {"current_status": current_state,
                               "status_change_id": process_id,
                               "Change_at": actual_datetime}


def test_escenario_3():
    # Obtengo la fecha y hora actual
    actual_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Guardo el estado de criticidad para posterior uso
    current_state = 5

    # Establezco el estado de criticidad
    response = set_state("test_secapp01", current_state, actual_datetime)

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta incluya el campo "processed_id"
    assert "processed_id" in response.json()

    process_id = response.json()["processed_id"]

    response = get_state("test_secapp02")

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario con los datos correctos
    assert response.json() == {"current_status": current_state,
                               "status_change_id": process_id,
                               "Change_at": actual_datetime}

    response = get_state("test_secapp02")

    # Verifica que la respuesta tenga el código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario vacío
    assert response.json() == {}
