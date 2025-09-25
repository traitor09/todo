# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import ObjectId
from utils.rule_based_recommendation import rule_based_recommend
from utils.preprocess import process_json_data
from utils.ml_based_recommendation import ml_based_recommend_mongo
from pymongo import MongoClient
import os

# ---------------------------
# MongoDB Direct Connection
# ---------------------------
MONGO_URI = "mongodb+srv://myUser1:myUser1@cluster0.mrprgj8.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME = "internship_recommendation_db"

client = None  # global client

def get_mongo_collection(collection_name):
    global client
    if client is None:
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            print("✅ Connected to MongoDB Atlas")
        except Exception as e:
            print("❌ MongoDB connection failed:", e)
            raise ConnectionError(f"Could not connect to MongoDB: {e}")
    db = client[MONGO_DB_NAME]
    return db[collection_name]

# ---------------------------
# Flask App
# ---------------------------
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

@app.route('/')
def home():
    return 'App is running'

@app.route('/recommend', methods=['POST'])
def recommend_internships():
    try:
        candidate_profile = request.get_json()
        if not candidate_profile:
            return jsonify({"error": "Invalid JSON or empty request body"}), 400

        print(f"Received candidate profile: {candidate_profile}")

        # Get the InternshipListing collection
        internship_collection = get_mongo_collection('InternshipListing')
        
        # Fetch all internship documents
        internships_cursor = internship_collection.find({}, {
            "_id": 1,  # keep ObjectId
            "Title": 1,
            "Description": 1,


            "Sector": 1,
            "Stipend": 1,
            "Duration": 1,

            "Required Skills": 1,
            "Location": 1
        })
        # Convert ObjectId to string
        internships_list = []
        for doc in internships_cursor:
            doc['_id'] = str(doc['_id'])
            internships_list.append(doc)
        #skip
        # internships_processed = process_json_data(internships_list)
        # print("After preprocess:", len(internships_processed))
        # print(internships_processed[:2])


        # Debug: print all fetched internships
        for row in internships_list:
            print("Title:", row.get("Title"))
            print("Required Skills:", row.get("Required Skills"))  # <-- check the key


        # Rule-based recommendation
        recommendations = rule_based_recommend(candidate_profile, internships_list, top_n=10)
        print("Rule-based recommendations:", len(recommendations))

        # ML-based recommendation (optional)
        # recommended_internships = ml_based_recommend_mongo(candidate_profile, recommendations)

        return jsonify(recommendations)

    except ConnectionError as ce:
        return jsonify({"error": "Database connection error", "details": str(ce)}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask application with MongoDB...")
    app.run(host="0.0.0.0", port=os.environ.get("PORT",5000))
