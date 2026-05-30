from flask import Blueprint, request, jsonify
from models import db, User, Booking, Property
from routes.properties import token_required
from functools import wraps

admin = Blueprint("admin", __name__)

def admin_required(f):
    @wraps(f)
    @token_required
    def wrapper(*args, **kwargs):
        if request.user.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return wrapper

@admin.route("/admin/stats", methods=["GET"])
@admin_required
def get_stats():
    return jsonify({
        "total_users": User.query.count(),
        "total_properties": Property.query.count(),
        "total_bookings": Booking.query.count()
    })

@admin.route("/admin/users", methods=["GET"])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "email": u.email,
        "role": u.role,
        "created_at": str(u.created_at)
    } for u in users])

@admin.route("/admin/bookings", methods=["GET"])
@admin_required
def get_all_bookings():
    bks = Booking.query.all()
    result = []
    for b in bks:
        user = User.query.get(b.user_id)
        prop = Property.query.get(b.property_id)
        result.append({
            "id": b.id,
            "user_id": b.user_id,
            "user_email": user.email if user else "Unknown",
            "property_id": b.property_id,
            "property_name": prop.title if prop else "Unknown",
            "price_per_night": prop.price_per_night if prop else 0,
            "check_in": str(b.check_in),
            "check_out": str(b.check_out),
            "status": b.status
        })
    return jsonify(result)

@admin.route("/admin/properties", methods=["GET"])
@admin_required
def get_all_properties():
    props = Property.query.all()
    return jsonify([{
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price_per_night": p.price_per_night,
        "image_url": p.image_url,
        "owner_id": p.owner_id
    } for p in props])

@admin.route("/admin/properties", methods=["POST"])
@admin_required
def admin_add_property():
    data = request.get_json()
    if not data.get("title") or not data.get("price_per_night"):
        return jsonify({"error": "Title and price required"}), 400
    prop = Property(
        title=data["title"],
        description=data.get("description", ""),
        price_per_night=float(data["price_per_night"]),
        owner_id=request.user["user_id"]
    )
    db.session.add(prop)
    db.session.commit()
    return jsonify({"message": "Property added", "id": prop.id}), 201

@admin.route("/admin/properties/<int:id>", methods=["PUT"])
@admin_required
def admin_edit_property(id):
    prop = Property.query.get_or_404(id)
    data = request.get_json()
    if "title" in data:
        prop.title = data["title"]
    if "description" in data:
        prop.description = data["description"]
    if "price_per_night" in data:
        prop.price_per_night = float(data["price_per_night"])
    db.session.commit()
    return jsonify({"message": "Property updated"})

@admin.route("/admin/properties/<int:id>", methods=["DELETE"])
@admin_required
def admin_delete_property(id):
    prop = Property.query.get_or_404(id)
    db.session.delete(prop)
    db.session.commit()
    return jsonify({"message": "Property deleted"})

@admin.route("/admin/users/<int:id>/role", methods=["PUT"])
@admin_required
def update_user_role(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if data.get("role") not in ["user", "admin"]:
        return jsonify({"error": "Role must be user or admin"}), 400
    user.role = data["role"]
    db.session.commit()
    return jsonify({"message": f"Role updated to {user.role}"})
