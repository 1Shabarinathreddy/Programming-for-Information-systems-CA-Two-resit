from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/cars_db'
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


# Route for Signup API
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

if __name__ == '__main__':
    app.run(debug=True)
