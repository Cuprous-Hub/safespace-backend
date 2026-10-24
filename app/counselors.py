from flask import Blueprint, request, jsonify
from app import db
from app.models import Counselor, Booking
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

counselors_bp = Blueprint('counselors', __name__)

@counselors_bp.route('/', methods=['GET'])
def get_counselors():
    counselors = Counselor.query.filter_by(available=True).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'specialty': c.specialty,
        'bio': c.bio
    } for c in counselors])

@counselors_bp.route('/<int:counselor_id>/book', methods=['POST'])
@jwt_required()
def book_session(counselor_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    date = datetime.fromisoformat(data['date'])
    booking = Booking(user_id=user_id, counselor_id=counselor_id, date=date)
    db.session.add(booking)
    db.session.commit()
    return jsonify({'message': 'Session booked successfully', 'id': booking.id}), 201