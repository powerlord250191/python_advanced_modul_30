import factory
from faker import Faker

from main.models import Client, db, Parking

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.lazy_attribute(lambda x: fake.first_name())
    surname = factory.lazy_attribute(lambda x: fake.last_name())
    credit_card = factory.lazy_attribute(lambda x: fake.credit_card_number())
    car_number = factory.lazy_attribute(lambda x: fake.bothify(text="??###??"))


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.LazyAttribute(lambda x: fake.address())
    opened = factory.LazyAttribute(lambda x: fake.boolean())
    count_places = factory.LazyAttribute(lambda x: fake.random_int(min=10, max=150))
    count_available_places = factory.LazyAttribute(lambda p: p.count_places)
