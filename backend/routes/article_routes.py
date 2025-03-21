from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import auth_required, get_current_user
from models.article import save_article, get_article_by_id
from models.course import get_course_by_id
from utils.course_generator import CourseGenerator

article_bp = Blueprint('article', __name__, url_prefix='/api/v1')

generator = CourseGenerator()

@article_bp.route('/generate-article', methods=['POST'])
@auth_required
def generate_article():
    data = request.json
    topics = data.get("query")

    if not topics:
        return jsonify({"error": "Topics query is required"}), 400

    article_content = generator.generate_module_article({"Module Name": "Custom Module", "Topics Covered": topics})
    article_id = save_article(None, {"content": article_content})  

    return jsonify({"message": "Article generated successfully", "article_id": str(article_id)}), 201

@article_bp.route('/course/<course_id>/article/<article_id>', methods=['GET'])
@auth_required
def get_article(course_id, article_id):
    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    article = get_article_by_id(article_id)
    if not article:
        return jsonify({"error": "Article not found"}), 404

    return jsonify(article), 200
