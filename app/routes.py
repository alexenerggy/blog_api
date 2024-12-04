from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__)

# Хранилище данных
users = []
posts = []

# CRUD для пользователей
@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = {"id": len(users) + 1, "username": data['username'], "email": data['email']}
    users.append(user)
    return jsonify(user), 201

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# CRUD для постов
@api_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    user_id = data['user_id']
    if not any(u["id"] == user_id for u in users):
        return jsonify({"error": "User not found"}), 404
    post = {"id": len(posts) + 1, "title": data['title'], "content": data['content'], "user_id": user_id}
    posts.append(post)
    return jsonify(post), 201

@api_bp.route('/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if request.method == 'GET':
        return jsonify(post)

    if request.method == 'PUT':
        data = request.json
        post['title'] = data.get('title', post['title'])
        post['content'] = data.get('content', post['content'])
        return jsonify(post)

    if request.method == 'DELETE':
        posts.remove(post)
        return '', 204