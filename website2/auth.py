from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Klant
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

#@auth.route('/login', methods=['GET','POST'])
#def login():
#    if request.method == 'POST':
#        email = request.form.get('email')
#        password = request.form.get('password')
#
#        user = User.query.filter_by(email=email).first()
#        if user:
#            if check_password_hash(user.password, password):
#                flash('Logged in successfully!', category='success')
#                login_user(user, remember=True)
#                return redirect(url_for('views.home'))
#            else:
#                flash('Incorrect password, try again', category='error')
#        else:
#            flash('Email does not exist.', category='error')                



#   return render_template("login.html", user=current_user )

#@auth.route('/logout')
#@login_required
#def logout():
#    logout_user()
#    return redirect(url_for('auth.login'))

#@auth.route('/sign-up', methods=['GET','POST'])
#def sign_up():
#    if request.method == 'POST':
#        email = request.form.get('email')
#        first_name = request.form.get('firstName')
#        password1 = request.form.get('password1')
#        password2 = request.form.get('password2')#
#
#        user = User.query.filter_by(email=email).first()
#        if user:
#            flash('Email already exists.', category = 'error')
#        elif len(email) < 4:
#            flash('Email must be greater than 3 characters.', category='error')
#        elif len(first_name) < 2:
#            flash('First name must be greater than 1 characters.', category='error')
#        elif password1 != password2:
#            flash('Passwords don\'t match.', category='error')
#        elif len(password1) < 7:
#            flash('Password must be atleast 7 characters', category='error')
#        else:
#            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
#            db.session.add(new_user)
#            db.session.commit()
#            login_user(user, remember=True)
#            flash('Account created!', category='success')
#            return redirect(url_for('views.home'))

#    return render_template("sign_up.html", user=current_user)

# --------------------------------------------------------------------------------------------------------------------------------

@auth.route('/')
def index():
     return render_template('index.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Klant.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')   

    return render_template("login.html", user=current_user )  

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
            login_user(klant, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('index.html'))
        
    return render_template("register.html", klant=current_user)

@auth.route('/rooms')
def rooms():
     return render_template('rooms.html')

@auth.route('/boeking4')
def boeking4():
     return render_template('boeking4.html')

@auth.route('/boeking6')
def boeking6():
     return render_template('boeking6.html')

@auth.route('/boeking8')
def boeking8():
     return render_template('boeking8.html')


