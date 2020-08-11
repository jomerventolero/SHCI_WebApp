from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap


app = Flask(__name__)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "thisismysecretkey"



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    phone_number = StringField('phone', validators=[InputRequired(), Length(max=11)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    number = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(80), nullable=False)

    '''
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, pass_word):
        self.password_hash = generate_password_hash(pass_word)

    def verify_password(self, pass_word):
        return check_password_hash(self.password_hash, pass_word)
    '''

    def __repr__(self):
        return "<Entry: %r Name: %r" % self.number, self.name

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        usr = form.username.data
        pwd = form.password.data
        login_user = Profile.query.filter_by(username=usr).first()
        if login_user.password == pwd:
            return render_template('dashboard', login_user.username)
        else:
            return "Wrong password"
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        usr = form.username.data
        pwd = form.password.data
        email = form.email.data
        phone_number = form.phone_number.data
        new_user = Profile(username=usr, password=pwd, phone_number=phone_number, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)
