import json

from flask import Flask, request, jsonify
from models import User, Order, Offer
from setup_db import db
from database import Database



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False     # Вывод русских слов jsonify

db.create_all()

Database().load_all_users()
Database().load_all_orders()
Database().load_all_offers()


@app.route("/users/", methods=['GET', 'POST'])
def page_users():
    """ Вывод всех пользователей """
    if request.method == "GET":
        result = []
        for user in User.query.all():
            result.append(user.make_dict())

        return jsonify(result)

    elif request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()

        return "Пользователь добавлен", 201


@app.route("/users/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def page_user(uid: int):
    """ Вывод одного пользователя """
    if request.method == "GET":
        return jsonify(User.query.get(uid).make_dict())

    elif request.method == "DELETE":
        user_data = User.query.get(uid)
        db.session.delete(user_data)
        db.session.commit()

        return "Пользователь удален"

    elif request.method == "PUT":
        user_data = json.loads(request.data)
        new_data = User.query.get(uid)
        new_data.first_name = user_data["first_name"]
        new_data.last_name = user_data["last_name"]
        new_data.age = user_data["age"]
        new_data.email = user_data["email"]
        new_data.role = user_data["role"]
        new_data.phone = user_data["phone"]

        return "Пользователь обновлен"


@app.route("/orders/", methods=['GET', 'POST'])
def page_orders():
    """ Вывод всех orders """
    if request.method == "GET":
        result = []
        for order in Order.query.all():
            result.append(order.make_dict())

        return jsonify(result)

    elif request.method == "POST":
        user_data = json.loads(request.data)
        new_user = Order(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()

        return "Заказ добавлен"


@app.route("/orders/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def page_order(uid: int):
    """ Вывод одного order """
    if request.method == "GET":
        return jsonify(Order.query.get(uid).make_dict())

    elif request.method == "DELETE":
        user_data = User.query.get(uid)
        db.session.delete(user_data)
        db.session.commit()

        return "Заказ удален"

    elif request.method == "PUT":
        user_data = json.loads(request.data)
        new_data = User.query.get(uid)
        new_data.first_name = user_data["first_name"]
        new_data.last_name = user_data["last_name"]
        new_data.age = user_data["age"]
        new_data.email = user_data["email"]
        new_data.role = user_data["role"]
        new_data.phone = user_data["phone"]

        return "Заказ обновлен"


@app.route("/offers/", methods=['GET', 'POST'])
def page_offers():
    """ Вывод всех offers """
    if request.method == "GET":
        result = []
        for offer in Offer.query.all():
            result.append(offer.make_dict())

        return jsonify(result)

    elif request.method == "POST":
        user_data = json.loads(request.data)
        new_user = Offer(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()

        return "Offers добавлен"


@app.route("/offers/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def page_offer(uid: int):
    """ Вывод одного order """
    if request.method == "GET":
        return jsonify(Offer.query.get(uid).make_dict())

    elif request.method == "DELETE":
        user_data = User.query.get(uid)
        db.session.delete(user_data)
        db.session.commit()

        return "Offers удален"

    elif request.method == "PUT":
        user_data = json.loads(request.data)
        new_data = User.query.get(uid)
        new_data.first_name = user_data["first_name"]
        new_data.last_name = user_data["last_name"]
        new_data.age = user_data["age"]
        new_data.email = user_data["email"]
        new_data.role = user_data["role"]
        new_data.phone = user_data["phone"]

        return "Offers обновлен"


if __name__ == '__main__':
    app.run(debug=True)