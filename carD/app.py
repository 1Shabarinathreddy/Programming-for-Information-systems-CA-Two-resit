from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shabari:shabarinath@localhost:5432/carsdb'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route('/')
def landing():
    return render_template('landing.html')
        
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    phone = data['phone']
    password = generate_password_hash(data['password'])
    
    create_user = User(username=username, email=email, phone=phone, password=password)
    db.session.add(create_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username_or_email = data['username_or_email']
    password = data['password']
    
    user = User.query.filter((User.email == username_or_email) | (User.username == username_or_email)).first()
    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Login successful!'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
