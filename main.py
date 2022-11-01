import os
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

users_json = 'users.json'
orders_json = 'orders.json'
offers_json = 'offers.json'


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def as_dict(self):
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
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    address = db.Column(db.String(300))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))

    def as_dict(self):
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
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f"{Order.__tablename__}.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))

    def as_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


def load_json(file_json):
    """Чтение данных из json-файла"""
    with open(file_json, mode='r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def db_load(file_json, model):
    """Загрузка данных в БД"""
    with app.app_context():
        data = load_json(os.path.join('data', file_json))
        for i in data:
            db.session.add(model(**i))
        db.session.commit()


@app.route('/users', methods=["GET", "POST"])
def users_page():
    if request.method == "GET":
        return jsonify([user.as_dict() for user in User.query.all()])
    if request.method == "POST":
        user = json.loads(request.data)
        db.session.add(
            User(
                id=user.get("id"),
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                age=user.get("age"),
                email=user.get("email"),
                role=user.get("role"),
                phone=user.get("phone"),
            )
        )
        db.session.commit()
        return f"Пользователь с id:{user['id']} создан"


@app.route('/users/<int:pk>', methods=["PUT", "GET", "DELETE"])
def user_page(pk):
    if request.method == "GET":
        return jsonify(User.query.get(pk).as_dict())
    if request.method == "PUT":
        user_id = User.query.get(pk)
        user = json.loads(request.data)

        user_id.first_name = user["first_name"]
        user_id.last_name = user["last_name"]
        user_id.age = user["age"]
        user_id.email = user["email"]
        user_id.role = user["role"]
        user_id.phone = user["phone"]

        db.session.add(user_id)
        db.session.commit()

        return f"Данные пользователя с id:{user_id.id} обновлены"

    if request.method == "DELETE":
        user = User.query.get(pk)
        db.session.delete(user)
        db.session.commit()
        return f"Пользователь с id:{user.id} удалён"


@app.route('/orders', methods=["GET", "POST"])
def orders_page():
    if request.method == "GET":
        return jsonify([order.as_dict() for order in Order.query.all()])
    if request.method == "POST":
        order = json.loads(request.data)
        db.session.add(
            Order(
                id=order.get("id"),
                name=order.get("name"),
                description=order.get("description"),
                start_date=order.get("start_date"),
                end_date=order.get("end_date"),
                address=order.get("address"),
                price=order.get("price"),
                customer_id=order.get("customer_id"),
                executor_id=order.get("executor_id"),
            )
        )
        db.session.commit()
        return f"Заказ с id:{order['id']} создан"


@app.route('/orders/<int:pk>', methods=["PUT", "GET", "DELETE"])
def order_page(pk):
    if request.method == "GET":
        return jsonify(Order.query.get(pk).as_dict())
    if request.method == "PUT":
        order_id = Order.query.get(pk)
        order = json.loads(request.data)

        order_id.name = order["name"]
        order_id.description = order["description"]
        order_id.start_date = order["start_date"]
        order_id.end_date = order["end_date"]
        order_id.address = order["address"]
        order_id.price = order["price"]
        order_id.customer_id = order["customer_id"]
        order_id.executor_id = order["executor_id"]

        db.session.add(order_id)
        db.session.commit()

        return f"Данные заказа с id:{order_id.id} обновлены"

    if request.method == "DELETE":
        order = Order.query.get(pk)
        db.session.delete(order)
        db.session.commit()
        return f"Заказ с id:{order.id} удалён"


@app.route('/offers', methods=["GET", "POST"])
def offers_page():
    if request.method == "GET":
        return jsonify([offer.as_dict() for offer in Offer.query.all()])
    if request.method == "POST":
        offer = json.loads(request.data)
        db.session.add(
            Offer(
                id=offer.get("id"),
                order_id=offer.get("order_id"),
                executor_id=offer.get("executor_id"),
            )
        )
        db.session.commit()
        return f"Предложение с id:{offer['id']} создано"


@app.route('/offers/<int:pk>', methods=["PUT", "GET", "DELETE"])
def offer_page(pk):
    if request.method == "GET":
        return jsonify(Offer.query.get(pk).as_dict())
    if request.method == "PUT":
        offer_id = Offer.query.get(pk)
        offer = json.loads(request.data)

        offer_id.order_id = offer["order_id"]
        offer_id.executor_id = offer["executor_id"]

        db.session.add(offer_id)
        db.session.commit()

        return f"Данные предложения с id:{offer_id.id} обновлены"

    if request.method == "DELETE":
        offer = Offer.query.get(pk)
        db.session.delete(offer)
        db.session.commit()
        return f"Предложение с id:{offer.id} удалёно"


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        db_load(users_json, User)
        db_load(offers_json, Offer)
        db_load(orders_json, Order)

        app.run(debug=True)
