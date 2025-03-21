import uuid
from config import db
from bson import ObjectId

def get_course_collection():
    return db["courses"]

def save_course(user_id, course_data):
    """ Save a course and assign unique module IDs """
    course_collection = get_course_collection()
    
    # Assign a unique ID to each module
    for module in course_data.get("modules", []):
        module["module_id"] = str(uuid.uuid4())  # Generate unique module ID
    
    course_data["user_id"] = user_id
    return str(course_collection.insert_one(course_data).inserted_id)

def get_courses_by_user(user_id):
    """ Retrieve courses belonging to a specific user """
    course_collection = get_course_collection()
    courses = course_collection.find({"user_id": user_id}, {"_id": 1, "course_name": 1})

    return [{"_id": str(course["_id"]), "course_name": course["course_name"]} for course in courses]

def get_course_by_id(course_id):
    """ Retrieve a course by ID and convert ObjectId to string """
    course_collection = get_course_collection()
    course = course_collection.find_one({"_id": ObjectId(course_id)})

    if course:
        course["_id"] = str(course["_id"])
        for module in course.get("modules", []):
            module["module_id"] = str(module["module_id"])  # Ensure module_id is string
    return course
def get_course_by_user(user_id):
    """ Retrieve all courses for a specific user """
    course_collection = get_course_collection()
    courses = course_collection.find({"user_id": user_id}, {"_id": 1, "course_name": 1})

    return [{"_id": str(course["_id"]), "course_name": course["course_name"]} for course in courses]