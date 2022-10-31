# from flask_sqlalchemy import SQLAlchemy
# import main
#
# #db = SQLAlchemy(main.app)
#
#
# class User(db.Model):
#     __tablename__ = "users"
#
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50))
#     last_name = db.Column(db.String(50))
#     age = db.Column(db.Integer)
#     email = db.Column(db.String(100))
#     role = db.Column(db.String(100))
#     phone = db.Column(db.String(100))
#
#
# db.create_all()
#
#
# class Order(db.Model):
#     __tablename__ = "orders"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     description = db.Column(db.String(50))
#     start_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)
#     address = db.Column(db.String(300))
#     price = db.Column(db.Integer)
#     customer_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))
#     executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))
#
#
# db.create_all()
#
#
# class Offer(db.Model):
#     __tablename__ = "offers"
#
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey(f"{Order.__tablename__}.id"))
#     executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))
#
#
# db.create_all()
