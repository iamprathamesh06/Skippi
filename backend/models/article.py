from config import db

def get_article_collection():
    return db["articles"]

def save_article(course_id, article_data):
    article_collection = get_article_collection()
    article_data["course_id"] = course_id
    return article_collection.insert_one(article_data).inserted_id

def get_article_by_id(article_id):
    article_collection = get_article_collection()
    return article_collection.find_one({"_id": article_id})
