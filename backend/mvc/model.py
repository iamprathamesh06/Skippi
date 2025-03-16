from flask_pymongo import PyMongo

mongo = PyMongo()

def create_user(fullname, email, password, role):
    user = {
        "fullname": fullname,
        "email": email,
        "password": password,  # Hashed password will be stored
        "role": role
    }
    return mongo.db.users.insert_one(user)

def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})
