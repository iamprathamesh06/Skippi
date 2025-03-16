from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from model import mongo, create_user, find_user_by_email

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ('fullname', 'email', 'password', 'role')):
        return jsonify({'message': 'Missing fields'}), 400

    # Check if user already exists
    if find_user_by_email(data['email']):
        return jsonify({'message': 'User already exists'}), 400

    # Hash the password before storing
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Insert user into MongoDB
    create_user(data['fullname'], data['email'], hashed_password, data['role'])
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'message': 'Missing fields'}), 400

    user = find_user_by_email(data['email'])
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity={'email': user['email'], 'role': user['role']}, expires_delta=timedelta(days=1))
        return jsonify({'message': 'Login successful', 'token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
