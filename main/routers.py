from datetime import datetime

from flask import jsonify, request

from main.models import Client, ClientParking, Parking, create_app, db

app = create_app()


@app.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return jsonify(
        [
            {"id": client.id, "name": client.name, "surname": client.surname}
            for client in clients
        ]
    )


@app.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(
        {
            "id": client.id,
            "name": client.name,
            "surname": client.surname,
            "credit_card": client.credit_card,
            "car_number": client.car_number,
        }
    )


@app.route("/clients", methods=["POST"])
def create_client():
    data = request.json
    new_client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data.get("credit_card"),
        car_number=data.get("car_number"),
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify({"id": new_client.id}), 201


@app.route("/parkings", methods=["POST"])
def create_parking():
    data = request.json
    new_parking = Parking(
        address=data["address"],
        count_places=data["count_places"],
        count_available_places=data["count_places"],
        opened=data.get("opened", True),
    )
    db.session.add(new_parking)
    db.session.commit()
    return jsonify({"id": new_parking.id}), 201


@app.route("/client_parkings", methods=["POST"])
def check_in_parking():
    data = request.json
    client = Client.query.get_or_404(data["client_id"])
    parking = Parking.query.get_or_404(data["parking_id"])

    if not parking.opened:
        return jsonify({"error": "Parking is closed"}), 400
    if parking.count_available_places <= 0:
        return jsonify({"error": "No available places"}), 400
    if not client.credit_card:
        return jsonify({"error": "Client does not have a credit card"}), 400

    new_client_parking = ClientParking(
        client_id=client.id, parking_id=parking.id, time_in=datetime.now()
    )
    db.session.add(new_client_parking)
    parking.count_available_places -= 1
    db.session.commit()

    return jsonify({"id": new_client_parking.id}), 201


@app.route("/client_parkings", methods=["DELETE"])
def check_out_parking():
    data = request.json
    client_parking = ClientParking.query.filter_by(
        client_id=data["client_id"], parking_id=data["parking_id"], time_out=None
    ).first()

    if not client_parking:
        return jsonify({"error": "No active parking found for this client"}), 404

    client_parking.time_out = datetime.now()
    parking = Parking.query.get(client_parking.parking_id)
    parking.count_available_places += 1

    db.session.commit()

    return jsonify({"message": "Checked out successfully"}), 200
