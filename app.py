import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config1

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False     # Вывод русских слов jsonify

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), unique=True)

    def make_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    description = db.Column(db.String, nullable=True)
    start_date = db.Column(db.String, nullable=True)
    end_date = db.Column(db.String, nullable=True)
    address = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def make_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }

class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def make_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


db.create_all()

for data in config1.DATAUSERS:
    new_user = User(
        id=data["id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        email=data["email"],
        role=data["role"],
        phone=data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()

for data in config1.DATAORDERS:
    new_user = Order(
        id=data["id"],
        name=data['name'],
        description=data['description'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        address=data['address'],
        price=data['price'],
        customer_id=data["customer_id"],
        executor_id=data["executor_id"],
    )
    db.session.add(new_user)
    db.session.commit()

for data in config1.DATAOFFER:
    new_user = Offer(
        id=data["id"],
        order_id=data["order_id"],
        executor_id=data["executor_id"],
    )
    db.session.add(new_user)
    db.session.commit()


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