from bson import ObjectId  # Import ObjectId for conversion
from config import db

def get_course_collection():
    return db["courses"]

def save_course(user_id, course_data):
    course_collection = get_course_collection()
    course_data["user_id"] = user_id
    return str(course_collection.insert_one(course_data).inserted_id)  # Convert ObjectId to string

def get_courses_by_user(user_id):
    course_collection = get_course_collection()
    courses = course_collection.find({"user_id": user_id}, {"_id": 1, "course_name": 1})

    # Convert ObjectId to string for JSON serialization
    return [{"_id": str(course["_id"]), "course_name": course["course_name"]} for course in courses]

def get_course_by_id(course_id):
    course_collection = get_course_collection()
    
    # Convert string ID to ObjectId before querying
    course = course_collection.find_one({"_id": ObjectId(course_id)})

    if course:
        course["_id"] = str(course["_id"])  # Convert ObjectId to string
    return course
