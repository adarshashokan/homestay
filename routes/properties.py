from flask import Blueprint, request, jsonify
from models import db, Property
from functools import wraps
import jwt, os

properties = Blueprint('properties', __name__)

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        try:
            payload = jwt.decode(token, os.environ.get('JWT_SECRET', 'jwt-secret-key'), algorithms=['HS256'])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return wrapper

@properties.route('/properties', methods=['GET'])
def get_properties():
    props = Property.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'price_per_night': p.price_per_night,
        'image_url': p.image_url
    } for p in props])

@properties.route('/properties', methods=['POST'])
@token_required
def add_property():
    data = request.get_json()
    prop = Property(
        title=data['title'],
        description=data['description'],
        price_per_night=data['price_per_night'],
        owner_id=request.user['user_id']
    )
    db.session.add(prop)
    db.session.commit()
    return jsonify({'message': 'Property added', 'id': prop.id}), 201

@properties.route('/properties/<int:id>', methods=['DELETE'])
@token_required
def delete_property(id):
    prop = Property.query.get_or_404(id)
    db.session.delete(prop)
    db.session.commit()
    return jsonify({'message': 'Property deleted'})
