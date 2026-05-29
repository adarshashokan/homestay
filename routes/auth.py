from flask import Blueprint, request, jsonify
import bcrypt, jwt, os, re
from models import db, User

auth = Blueprint('auth', __name__)

def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def validate_password(password):
    return len(password) >= 8

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Input validation
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    if not validate_password(data['password']):
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    # bcrypt hashing
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt(rounds=12))
    user = User(email=data['email'], password_hash=hashed.decode())
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    
    # Timing-safe comparison
    if user and bcrypt.checkpw(data['password'].encode(), user.password_hash.encode()):
        token = jwt.encode(
            {'user_id': user.id, 'role': user.role},
            os.environ.get('JWT_SECRET', 'jwt-secret-key'),
            algorithm='HS256'
        )
        return jsonify({'token': token, 'role': user.role})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully'})
