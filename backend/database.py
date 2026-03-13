from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["abhimanyu_ai"]

users = db["users"]
interviews = db["interviews"]
resumes = db["resumes"]