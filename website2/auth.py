from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Klant, Bungalow, Boekingen
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm.exc import NoResultFound

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
     return render_template('index.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pw')
        
        try: 
            user = db.session.execute(db.select(Klant).where(Klant.email == email)).scalar_one()
        except NoResultFound:  
            user = None
        
        if user:
            if check_password_hash(user.pw, password):
                flash('Succesvol ingelogd!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect wachtwoord, try again', category='error')
        else:
            flash('Email does not exist.', category='error')   

    return render_template("login.html", user=current_user )  

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('firstName')
        pw1 = request.form.get('password1')
        pw2 = request.form.get('password2')

        klant = Klant.query.filter_by(email=email).first()
        if klant:
            flash('Email is al in gebruik.', category='error')
        elif pw1 != pw2:
            flash('Wachtwoorden komen niet overeen.', category='error')
        elif len(pw1) < 8:
            flash('Wachtwoord is te kort.', category='error')
        else:
            new_klant = Klant(email=email, name=name, pw=generate_password_hash(pw1, method='sha256'))
            db.session.add(new_klant)                    # Voeg toe
            db.session.commit()                          # Commit
            login_user(new_klant, remember=True)
            flash('Account aangemaakt!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("register.html", klant=current_user)

@auth.route('/bungalows')
def bungalows():
     return render_template('rooms.html')

@auth.route('/bungalow/<int:bungalow_id>', methods=["GET", "POST"])
def bungalow(bungalow_id):
    bungalow = db.get_or_404(Bungalow, bungalow_id)

    if request.method == 'POST':
        week = request.form.get('week')

        #boeking = Boekingen.query.filter_by(week='week')
        #if boeking:
        #    flash('Datum is niet beschikbaar', category='error')
        #else:
        new_boeking = Boekingen(week=week, customer_id = current_user.id, bungalow_id = bungalow.id)
        db.session.add(new_boeking)                   
        db.session.commit()
        flash('Boeking succesvol!', category='success')
        return redirect(url_for('views.home'))

    #print(list(db.session.execute(db.select(Bungalow)).scalars()))
    return render_template('huisjes.html', bungalow = bungalow)

@auth.route('/boekingen')
@login_required
def boekingen():

    results = db.session.execute(db.select(Boekingen, Bungalow)
                                 .filter(Boekingen.bungalow_id == Bungalow.id)
                                 .filter(Boekingen.customer_id == current_user.id)).scalars()
    return render_template("mijnboekingen.html", user=current_user, boekingen=results)


@auth.route('/delete/<int:id>')
def delete_pl(id):
    result = db.get_or_404(Boekingen, id)
    db.session.delete(result)
    db.session.commit()
    flash("Boeking geannuleerd.")
    return redirect(url_for("views.home"))

@auth.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_pl(id):
    result = db.get_or_404(Boekingen, id)

    if request.method == 'POST':
        new_week = request.form["week"]
        if not new_week:
            flash("Er waren geen wijzigingen")
        old_boeking = result.boeking
        result.boeking = new_week
        flash(f"Updated {old_boeking} to {new_week}.")
        return ...
    
    elif request.method == 'POST':
        new_bungalow = request.form["bungalow"]
        if not new_bungalow:
            flash("Er waren geen wijzigingen")
        old_bungalow = result_bungalow
        result_bungalow = new_bungalow
        flash(f"Updated {old_bungalow} to {new_bungalow}")
        return ...
    
    return ...

        
    