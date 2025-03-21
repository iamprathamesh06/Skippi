from flask import Blueprint, request, jsonify
from models.user import get_user_collection
from utils.hash_utils import hash_password, check_password
from utils.jwt_utils import generate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
users = get_user_collection()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    if not fullname or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = hash_password(password)
    users.insert_one({
        "fullname": fullname,
        "email": email,
        "password": hashed_password,
        "role": role,
        "is_active": True
    })

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users.find_one({"email": email})
    if not user or not check_password(user['password'], password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(email)
    return jsonify({"message": "Login successful", "token": token}), 200
