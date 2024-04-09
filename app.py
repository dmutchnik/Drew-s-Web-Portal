# Flask Backend (app.py)

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import generate_password_hash, check_password_hash
import mandrill

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MANDRILL_API_KEY'] = 'md-qdqA-637dFS7FZY-oqO8gQ'  # Your Mandrill API key
app.config['SECRET_KEY'] = 'bofa'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, supports_credentials=True)  # Enable CORS for all routes

# Define your User model here
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100))  # Add password_hash column
    phone = db.Column(db.String(20))
    image = db.Column(db.String(100))

def setup_database():
    with app.app_context():
        db.create_all()
        if not User.query.first():  # Check if there are any existing users in the database
            load_dummy_data()

def load_dummy_data():
    dummy_users = [
        {'name': 'John Doe', 'email': 'john@example.com', 'password_hash': generate_password_hash('password123'), 'phone': '1234567890', 'image': 'path/to/image1.jpg'},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'password_hash': generate_password_hash('password456'), 'phone': '0987654321', 'image': 'path/to/image2.jpg'},
        # Add more dummy users as needed
    ]
    
    for data in dummy_users:
        new_user = User(**data)
        db.session.add(new_user)

    db.session.commit()

# Call the function to set up the database
setup_database()

# Function to send welcome email
def send_welcome_email(email):
    mandrill_client = mandrill.Mandrill(app.config['MANDRILL_API_KEY'])
    message = {
        'from_email': 'test@limudnaim.co.il',
        'to': [{'email': email}],
        'subject': 'Welcome to Our Platform!',
        'text': 'Welcome to our platform! We are excited to have you onboard.'
    }
    try:
        result = mandrill_client.messages.send(message=message)
        print(result)
    except mandrill.Error as e:
        print(f'Error sending welcome email: {e}')

@app.route('/register', methods=['POST'])
def register():
    print("registering")
    data = request.form
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create a new user
    new_user = User(name=data['name'], email=data['email'], password_hash=generate_password_hash(data['password']), phone=data['phone'], image=data['image'])
    db.session.add(new_user)
    db.session.commit()

    # Send welcome email upon successful registration
    send_welcome_email(data['email'])

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    # Query the user by email
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        # Set session variables
        session['user_id'] = user.id
        print(session['user_id'])
        print(session.keys(), session.values)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/session', methods=['GET'])
def getS():
    print(session['user_id'])
    print(session.keys(), session.values)
    return jsonify({}), 200

@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    # Check if user is logged in
    print(session.keys(), session.values)
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401
    user_id = session['user_id']
    user = User.query.get(user_id)
    print(user)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    # GET request: Return user profile
    if request.method == 'GET':
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'image': user.image
        }), 200
    # PUT request: Update user profile
    elif request.method == 'PUT':
        data = request.json
        user.name = data.get('name', user.name)
        user.phone = data.get('phone', user.phone)
        user.image = data.get('image', user.image)
        db.session.commit()
        return jsonify({'message': 'User profile updated successfully'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    # Clear session variables
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)