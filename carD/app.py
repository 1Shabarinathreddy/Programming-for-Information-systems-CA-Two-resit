from flask import Flask, request, jsonify, render_template,  session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "b8b1d5a3c3a24f82a7bc4012a6e9d158"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shabari:shabarinath@localhost:5432/carsdb'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
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


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    booking_date = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    car = db.relationship('Car', backref=db.backref('bookings', lazy=True))



@app.route('/')
def landing():
    return render_template('landing.html')
        
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/book-cars', methods=['GET'])
def book_cars():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('book_cars.html')
@app.route('/car-bookings', methods=['GET'])
def car_bookings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('car_bookings.html')

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

@app.route('/add-car', methods=['GET', 'POST'])
def add_car():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['user_id']
        model = request.form['model']
        price = request.form['price']
        contact_number = request.form['contact_number']
        photo = request.files['photo']
        
        if photo:
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            
            new_car = Car(user_id=user_id, model=model, price=price, contact_number=contact_number, photo=filename)
            db.session.add(new_car)
            db.session.commit()
            return jsonify({'message': 'Car added successfully!', 'status': 'success'}), 200
    return render_template('add_car.html')


@app.route('/api/my-cars', methods=['GET'])
def api_my_cars():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401
    user_id = session['user_id']
    cars = Car.query.filter_by(user_id=user_id).all()
    cars_list = [{'id': car.id, 'model': car.model, 'price': car.price, 'contact_number': car.contact_number, 'photo': car.photo} for car in cars]
    return jsonify({'cars': cars_list}), 200

@app.route('/my-cars', methods=['GET'])
def my_cars():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('my_cars.html')

@app.route('/api/delete-car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401
    user_id = session['user_id']
    car = Car.query.filter_by(id=car_id, user_id=user_id).first()
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'Car deleted successfully!'}), 200
    return jsonify({'message': 'Car not found'}), 404

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('landing'))

@app.route('/api/get-car/<int:car_id>', methods=['GET'])
def get_car(car_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401
    user_id = session['user_id']
    car = Car.query.filter_by(id=car_id, user_id=user_id).first()
    if car:
        return jsonify({
            'model': car.model,
            'price': car.price,
            'contact_number': car.contact_number
        }), 200
    return jsonify({'message': 'Car not found'}), 404

@app.route('/api/update-car/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401
    user_id = session['user_id']
    car = Car.query.filter_by(id=car_id, user_id=user_id).first()
    if not car:
        return jsonify({'message': 'Car not found'}), 404

    data = request.get_json()
    car.model = data.get('model', car.model)
    car.price = data.get('price', car.price)
    car.contact_number = data.get('contact_number', car.contact_number)
    
    db.session.commit()
    return jsonify({'message': 'Car updated successfully!'}), 200



# API to book a car
@app.route('/api/book-car/<int:car_id>', methods=['POST'])
def book_car(car_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401
    user_id = session['user_id']
    car = Car.query.get(car_id)

    if not car:
        return jsonify({'message': 'Car not found'}), 404

    if car.user_id == user_id:
        return jsonify({'message': 'You cannot book your own car.'}), 403

    # Create a booking
    booking = Booking(user_id=user_id, car_id=car.id, booking_date=datetime.now())
    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': 'Car booked successfully!'}), 200


@app.route('/api/available-cars', methods=['GET'])
def available_cars():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    user_id = session['user_id']
    
    # Fetch all cars except those owned by the logged-in user
    cars = Car.query.filter(Car.user_id != user_id).all()
    cars_list = [
        {
            'id': car.id,
            'model': car.model,
            'price': car.price,
            'contact_number': car.contact_number,
            'photo': car.photo
        }
        for car in cars
    ]
    
    return jsonify({'cars': cars_list}), 200

@app.route('/api/car-bookings', methods=['GET'])
def api_car_bookings():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401
    user_id = session['user_id']
    cars_owned = Car.query.filter_by(user_id=user_id).all()
    car_ids = [car.id for car in cars_owned]
    bookings = Booking.query.filter(Booking.car_id.in_(car_ids)).all()
    bookings_list = [{
        'car_model': booking.car.model,
        'booking_date': booking.booking_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': booking.status,
        'booked_by': booking.user.username,
        'booked_user_contact': booking.user.phone
    } for booking in bookings]
    return jsonify({'bookings': bookings_list}), 200



if __name__ == '__main__':
    app.run(debug=True)
