from datetime import datetime, timedelta

import pytest
from main.models import Client, ClientParking, Parking
from main.models import db as _db
from main.routers import app as routers_app


@pytest.fixture
def start_app():
    app = routers_app
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    with app.app_context():
        _db.create_all()
        test_client = Client(
            name="test_name",
            surname="test_surname",
            credit_card="1644 56464 4461",
            car_number="test_number",
        )
        test_parking = Parking(
            address="test address",
            opened=True,
            count_places=15,
            count_available_places=15,
        )

        _db.session.add_all([test_client, test_parking])
        _db.session.commit()

        test_client_parking = ClientParking(
            client_id=test_client.id,
            parking_id=test_parking.id,
            time_in=datetime.now(),
            time_out=datetime.now() + timedelta(hours=1),
        )

        _db.session.add_all([test_client_parking])
        _db.session.commit()

        yield app

        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(start_app):
    yield start_app.test_client()


@pytest.fixture
def database(start_app):
    from main.models import db as test_db

    yield test_db
