# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import ObjectId
from utils.rule_based_recommendation import rule_based_recommend
from utils.preprocess import process_json_data
from utils.ml_based_recommendation import ml_based_recommend_mongo
from utils.exceptions import ConfigurationError, ValidationError, DatabaseError, RecommendationError
from utils.validation import validate_candidate_profile, validate_top_n
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Any

# ---------------------------
# Logging Configuration
# ---------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------------------
# MongoDB Connection
# ---------------------------

load_dotenv()

MONGO_URI = os.getenv("MONGO_CONNECTION_STRING") 
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME") 

if not MONGO_URI:
    raise ConfigurationError("❌ The environment variable MONGO_CONNECTION_STRING is not set.")

if not MONGO_DB_NAME:
    raise ConfigurationError("❌ The environment variable MONGO_DB_NAME is not set.")

client = None  # global client

def get_mongo_collection(collection_name: str):
    """
    Get a MongoDB collection with connection pooling.
    
    Args:
        collection_name: Name of the collection to retrieve
        
    Returns:
        MongoDB collection object
        
    Raises:
        DatabaseError: If connection fails
    """
    global client
    if client is None:
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            logger.info("✅ Connected to MongoDB Atlas")
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise DatabaseError(f"Could not connect to MongoDB: {e}")
    
    db = client[MONGO_DB_NAME]
    return db[collection_name]

# ---------------------------
# Flask App
# ---------------------------
app = Flask(__name__)

# Configure CORS with environment-based origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080,http://localhost:5173").split(",")
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

@app.route('/')
def home():
    """Health check endpoint."""
    return jsonify({
        "status": "running",
        "message": "Internship Recommendation System API",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    """
    Health check endpoint with database connectivity status.
    """
    try:
        # Check database connection
        get_mongo_collection('InternshipListing')
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 503

@app.route('/recommend', methods=['POST'])
def recommend_internships():
    """
    Recommend internships based on candidate profile.
    
    Request Body:
        {
            "Skills": ["Python", "Flask", "MongoDB"],
            "Location": "Remote" (optional),
            "Eligibility": "3rd year" (optional),
            "Degree": "B.Tech" (optional),
            "Sector": "Technology" (optional)
        }
    
    Query Parameters:
        top_n: Number of recommendations to return (default: 10, max: 100)
    
    Returns:
        JSON array of recommended internships with match scores
    """
    try:
        # Get and validate request data
        candidate_profile = request.get_json()
        
        if not candidate_profile:
            logger.warning("Empty or invalid JSON received")
            return jsonify({
                "error": "Invalid JSON or empty request body",
                "message": "Please provide a valid candidate profile"
            }), 400

        # Validate candidate profile
        try:
            validated_profile = validate_candidate_profile(candidate_profile)
            logger.info(f"Received candidate profile with {len(validated_profile.get('Skills', []))} skills")
        except ValidationError as ve:
            logger.warning(f"Validation error: {ve}")
            return jsonify({
                "error": "Validation error",
                "message": str(ve)
            }), 400

        # Get and validate top_n parameter
        try:
            top_n = validate_top_n(request.args.get('top_n', type=int))
        except ValidationError as ve:
            logger.warning(f"Invalid top_n parameter: {ve}")
            return jsonify({
                "error": "Invalid parameter",
                "message": str(ve)
            }), 400

        # Get the InternshipListing collection
        try:
            internship_collection = get_mongo_collection('InternshipListing')
        except DatabaseError as de:
            logger.error(f"Database connection error: {de}")
            return jsonify({
                "error": "Database connection error",
                "message": "Unable to connect to the database. Please try again later."
            }), 503
        
        # Fetch all internship documents
        try:
            internships_cursor = internship_collection.find({}, {
                "_id": 1,
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
            
            logger.info(f"Fetched {len(internships_list)} internships from database")
            
            if not internships_list:
                logger.warning("No internships found in database")
                return jsonify({
                    "message": "No internships available at the moment",
                    "recommendations": []
                }), 200
                
        except Exception as e:
            logger.error(f"Error fetching internships: {e}")
            return jsonify({
                "error": "Database query error",
                "message": "Failed to fetch internships from database"
            }), 500

        # Rule-based recommendation
        try:
            recommendations = rule_based_recommend(
                validated_profile, 
                internships_list, 
                top_n=top_n
            )
            logger.info(f"Generated {len(recommendations)} recommendations")
            
            # Optional: ML-based recommendation (uncomment when ready)
            # recommendations = ml_based_recommend_mongo(validated_profile, recommendations)
            
            return jsonify({
                "count": len(recommendations),
                "recommendations": recommendations
            }), 200
            
        except Exception as e:
            logger.error(f"Recommendation error: {e}")
            return jsonify({
                "error": "Recommendation engine error",
                "message": "Failed to generate recommendations"
            }), 500

    except Exception as e:
        logger.error(f"Unexpected error in /recommend endpoint: {e}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "error": "Method not allowed",
        "message": "The HTTP method is not allowed for this endpoint"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    logger.info("Starting Flask application with MongoDB...")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )
