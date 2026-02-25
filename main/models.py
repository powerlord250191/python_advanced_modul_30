from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Инициализация бд
    db.init_app(app)

    with app.app_context():
        # Создание таблиц
        db.create_all()

    return app


class Client(db.Model):  # type: ignore
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), nullable=True)
    car_number = db.Column(db.String(10), nullable=True)


class Parking(db.Model):  # type: ignore
    __tablename__ = "parking"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, default=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)


class ClientParking(db.Model):  # type: ignore
    __tablename__ = "client_parking"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"), nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)

    client = db.relationship("Client", backref="client_parkings")
    parking = db.relationship("Parking", backref="client_parkings")
