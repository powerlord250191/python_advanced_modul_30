from datetime import datetime

import pytest


@pytest.mark.parametrize("rout", ["/clients", "/clients/1"])
def test_clients_rout(client, rout):
    response = client.get(rout)
    assert response.status_code == 200


def test_create_client(client):
    data_client = {
        "name": "John",
        "surname": "Wick",
        "credit_card": "164 1654 4646 644",
        "car_number": "867 sda",
    }
    request = client.post("/clients", json=data_client)
    assert request.status_code == 201


def test_create_parking(parking):
    data_parking = {
        "address": "test address",
        "opened": True,
        "count_places": 15,
        "count_available_places": 15,
    }
    request = parking.post("/parkings", json=data_parking)
    assert request.status_code == 201


def test_create_check_in_parking(client_parking):
    data_client_parking = {
        "client_id": 1,
        "parking_id": 1,
        "time_in": datetime.now(),
        "time_out": None,
    }
    request = client_parking.post("/client_parkings", data_client_parking)
    assert request.status_code == 201


def test_delete_check_in_parking(client_parking):
    data_client_parking = {
        "client_id": 1,
        "parking_id": 1,
    }
    request = client_parking.delete("/client_parkings", data_client_parking)
    assert request.status_code == 201
