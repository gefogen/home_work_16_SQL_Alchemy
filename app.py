import json

from flask import Flask, request, jsonify
from models import User, Order, Offer
from setup_db import db
from database import Database

app = Flask(__name__)

# Закидываем настройки, которые скоро использует алхимия
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False  # Вывод русских слов jsonify

# Связываем базу данных и приложение
db.init_app(app)

# Связываем контекст с основным приложеним
# Чтобы не использовать with context
app.app_context().push()

# Создаем все таблицы
# В реальном коде это нужно вынести
db.create_all()

# Пишем в базу
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

        return "Пользователь добавлен"


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

        db.session.add(new_data)
        db.session.commit()

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
        order_data = json.loads(request.data)
        new_user = Order(
            id=order_data['id'],
            name=order_data['name'],
            description=order_data['description'],
            start_date=order_data['start_date'],
            end_date=order_data['end_date'],
            address=order_data['address'],
            price=order_data['price'],
            customer_id=order_data['customer_id'],
            executor_id=order_data['executor_id'],
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
        user_data = Order.query.get(uid)
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

        db.session.add(new_data)
        db.session.commit()

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
        offer_data = json.loads(request.data)
        new_user = Offer(
            id=offer_data['id'],
            order_id=offer_data['order_id'],
            executor_id=offer_data['executor_id']
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
        user_data = Offer.query.get(uid)
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

        db.session.add(new_data)
        db.session.commit()

        return "Offers обновлен"


if __name__ == '__main__':
    app.run(debug=True)
