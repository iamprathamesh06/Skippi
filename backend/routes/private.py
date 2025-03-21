from flask import Blueprint, jsonify
from middlewares.auth_middleware import auth_required, get_current_user

private_bp = Blueprint('private', __name__, url_prefix='/api/v1/private')

@private_bp.route('/dashboard', methods=['GET'])
@auth_required
def dashboard():
    user = get_current_user()
    return jsonify({"message": "Welcome to the dashboard!", "user": user}), 200
