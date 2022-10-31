import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


db.create_all()


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(300))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer,db.ForeignKey(f"{User.__tablename__}.id"))
    executor_id = db.Column(db.Integer,db.ForeignKey(f"{User.__tablename__}.id"))


db.create_all()


class Offer(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey(f"{Order.__tablename__}.id"))
    executor_id = db.Column(db.Integer,db.ForeignKey(f"{User.__tablename__}.id"))


db.create_all()


def load_json(file_json):
    """Чтение данных из json-файла"""
    with open(file_json,mode='r',encoding='utf-8') as file:
        data = json.load(file)
        return data


def users_db_load(db_table):
    """Загрузка данных в БД"""
    with app.app_context():
        users = load_json(os.path.join('data','users.json'))
        for user in users:
            db.session.add(
                db_table(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    age=user.age,
                    email=user.email,
                    role=user.role,
                    phone=user.phone
                )
            )
        db.session.commit()


@app.route('/users')
def users_page():
    return User.query.all()


with app.app_context():
    users_db_load(User)
    app.run(debug=True)
