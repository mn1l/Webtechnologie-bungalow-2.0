from . import db
from flask_login import UserMixin

class Klant(db.Model, UserMixin):
    __tablename__ = 'customer'
    # Structuur
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    pw = db.Column(db.String(150))
    name = db.Column(db.String(150))
    # Relaties
    bookings = db.relationship('Boekingen', backref='klant', lazy='dynamic')


class Bungalow(db.Model):
    __tablename__ = 'bungalow'
      # Structuur
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)
    size = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    # Relaties
    bookings = db.relationship('Boekingen', backref='bungalow', uselist=False)


class Boekingen(db.Model):
    __tablename__ = 'bookings'
    table_args = (
        db.UniqueConstraint('bungalow_id', 'week'),
    )
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False) # Not NULL
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id')) # Foreign key?
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalow.id')) # Foreign key?



