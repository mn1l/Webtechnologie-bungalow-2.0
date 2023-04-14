import os
from forms import RegisterForm
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(db, app)


class Klant(db.Model):
    __tablename__ = 'customer'
    # Structuur
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.Text)
    email = db.Column(db.varchar)
    pw = db.Column(db.varchar)
    # Relaties
    bookings = db.relationship('Boekingen', backref='klant', lazy='dynamic')


    def __init__(self, email, pw):
            self.email = email
            self.pw = pw


class Bungalow(db.Model):
    __tablename__ = 'bungalow'
      # Structuur
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)
    size = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    # Relaties
    bookings = db.relationship('Boekingen', backref='bungalow', uselist=False)


    def __init__(self, name, size, price):
        self.name = name
        self.size = size
        self.price = price


class Boekingen(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id')) # Foreign key?
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalow.id')) # Foreign key?
    week = db.Column(db.Integer(52), nullable=False) # Not NULL
    # Relaties
    bungalow = db.relationship('Bungalow', backref='bookings', uselist=False)
    customer = db.relationship('Klant', backref='bookings', lazy='dynamic')

    def __init__(self, id, customer_id, bungalow_id, week):
        self.id = id
        self.customer_id = customer_id
        self.bungalow_id = bungalow_id
        self.week = week

@app.route('/')
def index():
     return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def klant_add():
    form = RegisterForm

    if form.validate_on_submit():
        customers = form.klant.data

        # Nieuwe klant
        new_customer = Klant(customers) 
        

        db.session.add(new_customer)        # Voeg toe
        db.session.commit()                 # Commit

        return redirect("index.html")

    return render_template("register.html", form=form ) #



