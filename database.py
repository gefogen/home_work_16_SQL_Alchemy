from config1 import DATAUSERS, DATAORDERS, DATAOFFER
from models import User, Order, Offer
from setup_db import db


class Database:
    def load_all_users(self):
        for user_info in DATAUSERS:
            user = User(
                id = user_info["id"],
                first_name = user_info["first_name"],
                last_name = user_info["last_name"],
                age = user_info["age"],
                email = user_info["email"],
                role = user_info["role"],
                phone = user_info["phone"]
            )
            db.session.add(user)
            db.session.commit()


    def load_all_orders(self):
        for order_info in DATAORDERS:
            order = Order(
                id = order_info["id"],
                name = order_info["name"],
                description = order_info["description"],
                start_date = order_info["start_date"],
                end_date = order_info["end_date"],
                address = order_info["address"],
                price = order_info["price"],
                customer_id = order_info["customer_id"],
                executor_id = order_info["executor_id"]
            )
            db.session.add(order)
            db.session.commit()


    def load_all_offers(self):
        for offer_info in DATAOFFER:
            offer = Offer(
                id = offer_info["id"],
                order_id = offer_info["order_id"],
                executor_id = offer_info["executor_id"]
            )
            db.session.add(offer)
            db.session.commit()