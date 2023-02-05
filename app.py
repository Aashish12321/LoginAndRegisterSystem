from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import InputRequired, Email, Length, DataRequired, ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import column
import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# App Setup
app = Flask(__name__)


# Creating database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SecretVanekoSecretHoMaVandina'
db = SQLAlchemy(app)


# creating 'Users' table in 'users.db' database.
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"


app.app_context().push()

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=100)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=100)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])
    submit = SubmitField('Submit')



# Routes
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        oneRow = Users.query.filter_by(username = form.username.data)
        
        if bcrypt.check_password_hash(hashed_password, form.password.data):
            return f"<h2>Welcome {form.username.data} !</h2>"
            # return redirect('/')

        else:
            return "<h2>Wrong username or password.</h2>"
            # return redirect('/register')
    
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Users(username = form.username.data, password=hashed_password )
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')
    
    return render_template('register.html', form=form)


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
