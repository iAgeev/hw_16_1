import os
import json
from flask import Flask,jsonify,request
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


@app.route('/users', methods=["GET", "PUT"])
def users_page():
    if request.method == "GET":
        return jsonify([user.as_dict() for user in User.query.all()])
    if request.method == "PUT":
        pass


@app.route('/users/<int:pk>')
def user_page(pk):
    return jsonify(User.query.get(pk).as_dict())


@app.route('/orders', methods=["GET", "PUT"])
def orders_page():
    return jsonify([order.as_dict() for order in Order.query.all()])


@app.route('/orders/<int:pk>')
def order_page(pk):
    return jsonify(Order.query.get(pk).as_dict())


@app.route('/offers', methods=["GET", "PUT"])
def offers_page():
    return jsonify([offer.as_dict() for offer in Offer.query.all()])


@app.route('/offers/<int:pk>')
def offer_page(pk):
    return jsonify(Offer.query.get(pk).as_dict())


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        db_load(users_json, User)
        db_load(offers_json, Offer)
        db_load(orders_json, Order)

        app.run(debug=True)
