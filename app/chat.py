from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

chat_bp = Blueprint('chat', __name__)

ALLOWED_TOPICS = [
    'anxiety', 'depression', 'stress', 'loneliness', 
    'grief', 'self-esteem', 'relationships', 'motivation',
    'sadness', 'overwhelmed', 'support', 'mental health'
]

def is_allowed(message):
    message_lower = message.lower()
    return any(topic in message_lower for topic in ALLOWED_TOPICS)

@chat_bp.route('/', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    message = data.get('message', '')

    if not is_allowed(message):
        return jsonify({
            'response': "I'm here to support you with mental health topics like anxiety, depression, stress, and loneliness. Could you tell me more about how you're feeling?"
        }), 200

    return jsonify({
        'response': "Thank you for sharing. You're not alone in this. Would you like to talk more about what you're going through, or would you like to connect with one of our counselors?"
    }), 200