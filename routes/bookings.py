from flask import Blueprint, request, jsonify
from models import db, Booking
from routes.properties import token_required
from datetime import datetime

bookings = Blueprint('bookings', __name__)

@bookings.route('/bookings', methods=['POST'])
@token_required
def create_booking():
    data = request.get_json()
    
    # Check availability
    existing = Booking.query.filter_by(
        property_id=data['property_id']
    ).filter(
        Booking.check_in <= data['check_out'],
        Booking.check_out >= data['check_in']
    ).first()
    
    if existing:
        return jsonify({'error': 'Property not available for these dates'}), 400

    booking = Booking(
        user_id=request.user['user_id'],
        property_id=data['property_id'],
        check_in=datetime.strptime(data['check_in'], '%Y-%m-%d').date(),
        check_out=datetime.strptime(data['check_out'], '%Y-%m-%d').date()
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'message': 'Booking confirmed', 'id': booking.id}), 201

@bookings.route('/bookings', methods=['GET'])
@token_required
def get_bookings():
    bks = Booking.query.filter_by(user_id=request.user['user_id']).all()
    return jsonify([{
        'id': b.id,
        'property_id': b.property_id,
        'check_in': str(b.check_in),
        'check_out': str(b.check_out),
        'status': b.status
    } for b in bks])
