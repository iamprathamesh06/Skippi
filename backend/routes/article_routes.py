from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import auth_required, get_current_user
from models.article import save_article, get_article_by_module
from models.course import get_course_by_id
from utils.course_generator import CourseGenerator
from models.course import get_course_by_id, get_course_by_user
from models.article import get_article_collection


article_bp = Blueprint('article', __name__, url_prefix='/api/v1')

generator = CourseGenerator()

@article_bp.route('/course/<course_id>/module/<module_id>/generate-article', methods=['GET'])
@auth_required
def generate_or_get_article(course_id, module_id):
    """ Generate and save an article if it doesn't exist, else return the stored article """

    user_id = get_current_user()

    # Verify that the course exists and belongs to the user
    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    if course["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    # Check if article already exists
    existing_article = get_article_by_module(course_id, module_id)
    if existing_article:
        return jsonify({"message": "Article retrieved successfully", "article": existing_article}), 200

    # Find the module details from the course
    module = next((m for m in course["modules"] if m["module_id"] == module_id), None)
    if not module:
        return jsonify({"error": "Module not found in the course"}), 404

    # Generate article using LLM
    article_content = generator.generate_module_article(module)

    # Save article in DB
    article_id = save_article(course_id, module_id, {"content": article_content})

    return jsonify({"message": "Article generated successfully", "article_id": article_id, "article": article_content}), 201

@article_bp.route('/course/<course_id>/module/<module_id>/article', methods=['GET'])
@auth_required
def get_article(course_id, module_id):
    """ Retrieve an existing article by module_id """

    user_id = get_current_user()

    # Verify that the course exists and belongs to the user
    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    if course["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    # Get the stored article
    article = get_article_by_module(course_id, module_id)
    if not article:
        return jsonify({"error": "Article not found"}), 404

    return jsonify({"message": "Article retrieved successfully", "article": article}), 200

@article_bp.route('/articles', methods=['GET'])
@auth_required
def get_all_articles():
    """ Fetch all articles linked to the logged-in user """

    user_id = get_current_user()
    
    # Fetch all courses of the user
    courses = get_course_by_user(user_id)

    if not courses:
        return jsonify({"message": "No courses found for the user"}), 200

    # Extract all articles from the courses
    articles = []
    for course in courses:
        course_articles = get_article_collection().find({"course_id": course["_id"]})
        for article in course_articles:
            article["_id"] = str(article["_id"])
            articles.append(article)

    return jsonify({"message": "Articles retrieved successfully", "articles": articles}), 200


