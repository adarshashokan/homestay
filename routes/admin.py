from flask import Blueprint, request, jsonify
from models import db, User, Booking, Property
from routes.properties import token_required
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @token_required
    def wrapper(*args, **kwargs):
        if request.user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return wrapper

@admin.route('/admin/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'email': u.email,
        'role': u.role,
        'created_at': str(u.created_at)
    } for u in users])

@admin.route('/admin/bookings', methods=['GET'])
@admin_required
def get_all_bookings():
    bks = Booking.query.all()
    return jsonify([{
        'id': b.id,
        'user_id': b.user_id,
        'property_id': b.property_id,
        'check_in': str(b.check_in),
        'check_out': str(b.check_out),
        'status': b.status
    } for b in bks])

@admin.route('/admin/stats', methods=['GET'])
@admin_required
def get_stats():
    return jsonify({
        'total_users': User.query.count(),
        'total_properties': Property.query.count(),
        'total_bookings': Booking.query.count()
    })
