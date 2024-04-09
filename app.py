from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
import mandrill

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MANDRILL_API_KEY'] = 'md-qdqA-637dFS7FZY-oqO8gQ'  # Your Mandrill API key
app.config['SECRET_KEY'] = 'bofa'    
db = SQLAlchemy(app)

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    image = db.Column(db.String(100))

# Set up database and load dummy data if necessary
def setup_database():
    with app.app_context():
        db.create_all()
        if not User.query.first():
            load_dummy_data()

# Load dummy user data
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

# Send welcome email
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

# Register endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    new_user = User(name=data['name'], email=data['email'], password_hash=generate_password_hash(data['password']), phone=data['phone'], image=data['image'])
    db.session.add(new_user)
    db.session.commit()

    send_welcome_email(data['email'])
    return jsonify({'message': 'User registered successfully'}), 201

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

# Get session endpoint
@app.route('/session', methods=['GET'])
def getSession():
    return jsonify({}), 200

# Profile endpoint (GET and PUT)
@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'image': user.image
        }), 200
    elif request.method == 'PUT':
        data = request.json
        user.name = data.get('name', user.name)
        user.phone = data.get('phone', user.phone)
        user.image = data.get('image', user.image)
        db.session.commit()
        return jsonify({'message': 'User profile updated successfully'}), 200

# Logout endpoint
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
