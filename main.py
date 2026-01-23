from fastapi import FastAPI
from pymongo import MongoClient
from user_auth import UserAuth

app = FastAPI()

# Connect once when app starts
uri = "mongodb+srv://projectssayo_db_user:gEgSg9ug08WTP6NA@cluster0.pd254jn.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["suyognegi1_projects_sayo"]
users = db["users"]

def serialize_doc(doc):
    """Convert ObjectId to string for JSON serialization"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

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

@app.get("/view-all/")
def all_data():
    all_users = users.find()

    data = []
    for user in all_users:
        data.append({
            "email": user["_id"],
            "user_name": user.get("user_name"),
            "password": user.get("plain_password")  # return plain password as "password"
        })

    return {"data": data}


@app.get("/delete-user/")
def delete_user(email: str):
    auth = UserAuth()
    result = auth.delete_user(email)
    return {
        "email": email,
        **result
    }


@app.get("/if-email-exist/")
def check_email_exist(email: str):
    """Check if email already exists in the database. Returns {"found": true/false}"""
    try:
        
        user = users.find_one({"_id": email})
        return {"found": user is not None}  
    except Exception:
        return {"found": False}  

@app.get("/update-user/")
def update_user(email: str, user_name: str, password: str):
    """Update existing user's name and password"""
    auth = UserAuth()
    result = auth.update_user(email, user_name, password)

    return {
        "email": email,
        "user_name": user_name,
        **result
    }




@app.get("/info")
def get_info():
    return {
        "verify": "https://mongodb-api-9kpz.onrender.com/verify-user/?email=a@gmail.com&password=1234",
        "insert": "https://mongodb-api-9kpz.onrender.com/create-user/?email=a@gmail.com&user_name=alex&password=1234",
        "update": "https://mongodb-api-9kpz.onrender.com/update-user/?email=a@gmail.com&user_name=alex_new&password=12345",
        "view_all": "https://mongodb-api-9kpz.onrender.com/view-all/",
        "delete": "https://mongodb-api-9kpz.onrender.com/delete-user/?email=a@gmail.com",
        "check_email": "https://mongodb-api-9kpz.onrender.com/if-email-exist/?email=a@gmail.com",
        "docs": "https://mongodb-api-9kpz.onrender.com/docs",
        "schema": "https://mongodb-api-9kpz.onrender.com/openapi.json"
    }



