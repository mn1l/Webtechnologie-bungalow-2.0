from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Boekingen, Klant, Bungalow
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", user=current_user)

@views.route('/boekingen')
def boekingen():

    results = db.session.execute(db.select(Boekingen, Bungalow)
                                 .filter(Boekingen.bungalow_id == Bungalow.id)
                                 .filter(Boekingen.customer_id == current_user.id)).scalars()
    return render_template("mijnboekingen.html", user=current_user, boekingen=results)


