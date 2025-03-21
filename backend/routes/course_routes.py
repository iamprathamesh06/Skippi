from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import auth_required, get_current_user
from models.course import save_course, get_courses_by_user, get_course_by_id
from utils.course_generator import CourseGenerator

course_bp = Blueprint('course', __name__, url_prefix='/api/v1')

generator = CourseGenerator()

@course_bp.route('/generate-course', methods=['POST'])
@auth_required
def generate_course():
    user_id = get_current_user()
    data = request.json
    skill = data.get("query")

    if not skill:
        return jsonify({"error": "Skill query is required"}), 400

    course_blueprint = generator.generate_course_blueprint(skill)
    course_id = save_course(user_id, course_blueprint)

    return jsonify({"message": "Course generated successfully", "course_id": str(course_id)}), 201

@course_bp.route('/courses', methods=['GET'])
@auth_required
def get_courses():
    user_id = get_current_user()
    courses = get_courses_by_user(user_id)
    return jsonify({"courses": courses}), 200

@course_bp.route('/course/<course_id>', methods=['GET'])
@auth_required
def get_course(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course), 200
