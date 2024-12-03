from flask import Flask, request, jsonify, render_template,  session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.secret_key = "b8b1d5a3c3a24f82a7bc4012a6e9d158"
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

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(200), nullable=False)


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
        session['user_id'] = user.id
        print(session)
        return jsonify({'message': 'Login successful!', 'redirect': '/dashboard'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    flash('You have been logged out successfully!')
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)
