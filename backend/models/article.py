from config import db


def get_article_collection():
    return db["articles"]

def save_article(course_id, module_id, article_data):
    """ Save article to DB if it doesn't already exist """
    article_collection = get_article_collection()
    
    existing_article = article_collection.find_one({"course_id": course_id, "module_id": module_id})
    if existing_article:
        return str(existing_article["_id"])  # Return existing article ID

    article_data["course_id"] = course_id
    article_data["module_id"] = module_id
    return str(article_collection.insert_one(article_data).inserted_id)  # Insert new article

def get_article_by_module(course_id, module_id):
    """ Retrieve article if it exists """
    article_collection = get_article_collection()
    article = article_collection.find_one({"course_id": course_id, "module_id": module_id})
    
    if article:
        article["_id"] = str(article["_id"])
    return article

