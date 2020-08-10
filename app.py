from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    number = db.Column(db.Integer, unique=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Entry: %r Name: %r" % self.number, self.name



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login(username, password, methods=['POST', 'GET']):
    return render_template(login.html)

if __name__ == '__main__':
    app.run(debug=True)
