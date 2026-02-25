from main.models import Client
from tests.facktoryes_tests import ClientFactory, ParkingFactory


def test_create_client_factory(client, database):
    client_object = ClientFactory()
    database.session.add(client_object)
    database.session.commit()
    assert client_object.id is not None
    assert len(database.session.query(Client).all()) == 2


def test_create_parking_factory(client, database):
    parking_object = ParkingFactory()
    database.session.add(parking_object)
    database.session.commit()
    assert parking_object.id is not None
    assert parking_object.count_available_places == parking_object.count_places
