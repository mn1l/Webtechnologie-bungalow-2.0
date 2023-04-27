from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, EmailField, PasswordField, validators

class RegisterForm(FlaskForm):

    name = StringField('Uw naam')
    email = EmailField('Uw email')
    pw = PasswordField('Uw wachtwoord', validators=[validators.Length(min=8, message='Wachtwoord is te kort')])
    pw2 = PasswordField('Herhaal uw wachtwoord', validators=[validators.EqualTo('pw', 'Wachtwoord komt niet overeen')])
                        