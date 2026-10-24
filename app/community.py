from flask import Blueprint, request, jsonify
from app import db
from app.models import Post, Community
from flask_jwt_extended import jwt_required, get_jwt_identity

community_bp = Blueprint('community', __name__)

@community_bp.route('/', methods=['GET'])
def get_communities():
    communities = Community.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in communities])

@community_bp.route('/', methods=['POST'])
@jwt_required()
def create_community():
    data = request.get_json()
    community = Community(name=data['name'], description=data.get('description', ''))
    db.session.add(community)
    db.session.commit()
    return jsonify({'message': 'Community created', 'id': community.id}), 201

@community_bp.route('/<int:community_id>/posts', methods=['GET'])
def get_posts(community_id):
    posts = Post.query.filter_by(community_id=community_id).all()
    return jsonify([{'id': p.id, 'content': p.content, 'user_id': p.user_id} for p in posts])

@community_bp.route('/<int:community_id>/posts', methods=['POST'])
@jwt_required()
def create_post(community_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    post = Post(content=data['content'], user_id=user_id, community_id=community_id)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created', 'id': post.id}), 201