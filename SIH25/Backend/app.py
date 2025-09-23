# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from bson.json_util import dumps # For serializing MongoDB ObjectId to JSON
from dotenv import load_dotenv
import os

load_dotenv()

# Import functions from our utils modules
from utils.rule_based_recommendation import rule_based_recommend
from utils.preprocess import process_json_data
from utils.ml_based_recommendation import ml_based_recommend_mongo
from utils.db_utils import get_mongo_collection # Renamed to reflect MongoDB

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}}) # Enable CORS for all routes

# --- Flask API Endpoint ---

@app.route('/')
def home():
    return 'App is running'

@app.route('/recommend', methods=['POST'])
def recommend_internships():
    return jsonify({"message": "Test OK"})
        
if __name__ == '__main__':
    print("Starting Flask application with MongoDB...")
    app.run(host="0.0.0.0", port=os.environ.get("PORT",5000))