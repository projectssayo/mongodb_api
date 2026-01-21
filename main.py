from fastapi import FastAPI
from pymongo import MongoClient
# main.py
from fastapi import FastAPI
from user_auth import UserAuth

app = FastAPI()
auth = UserAuth()


@app.get("/verify-user/")
def verify_user(email: str, password: str):
    auth = UserAuth()
    result = auth.verify_user(email, password)

    return {
        "email": email,
        **result
    }


@app.get("/create-user/")
def create_user(email: str, user_name: str, password: str):
    """GET endpoint to create new user"""
    auth = UserAuth()
    result = auth.create_user(email, user_name, password)

    return {
        "email": email,
        "user_name": user_name,
        **result
    }


# Connect once when app starts
uri = "mongodb+srv://projectssayo_db_user:gEgSg9ug08WTP6NA@cluster0.pd254jn.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["suyognegi1_projects_sayo"]
users = db["users"]

def serialize_doc(doc):
    """Convert ObjectId to string for JSON serialization"""
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/view-all/")
def all_data():
    all_users = users.find()
    data = [serialize_doc(user) for user in all_users]
    return {"data": data}

@app.get("/delete-user/")
def delete_user(email: str):
    auth = UserAuth()
    result = auth.delete_user(email)
    return {
        "email": email,
        **result
    }

@app.get("/info")
def get_info():
    return {
         "verify": "http://127.0.0.1:8000/verify-user/?email=a@gmail.com&password=1234",

         "insert": "http://127.0.0.1:8000/create-user/?email=a@gmail.com&user_name=alex&password=1234",

        "view_all": "http://127.0.0.1:8000/view-all/",

        "delete": "http://127.0.0.1:8000/delete-user/?email=a@gmail.com",

        "docs": "http://127.0.0.1:8000/docs",

        "schema": "http://127.0.0.1:8000/openapi.json"
    }
