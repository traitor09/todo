import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk


# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

def preprocess_degree(degree_str):
    degree_str = degree_str.lower().replace('.', '').strip()
    parts = re.split(r'[/,]', degree_str)
    processed = []
    for part in parts:
        part = re.sub(r'\(.*?\)', '', part).strip()
        if part:
            processed.append(part)
    return list(set(processed))



#change
def normalize_eligibility(value: str) -> str: #eligibility_year_preprocessing
    value = value.lower().strip()

    mapping = {
        # Undergraduate variations
        "1st year": "1", "first year": "1", "1 year": "1", "1": "1",
        "2nd year": "2", "second year": "2", "2 year": "2", "2": "2",
        "3rd year": "3", "third year": "3", "3 year": "3", "3": "3",
        "4th year": "4", "fourth year": "4", "4 year": "4", "4": "4",

        # Postgraduate variations
        "postgraduate": "PG", "pg": "PG",
        # "pg-1": "1", "pg 1st year": "1", "pg first year": "1",
        # "pg-2": "2", "pg 2nd year": "2", "pg second year": "2",
        
        # Undergraduate shorthand
        "undergraduate": "UG", "ug": "UG"
    }

    return mapping.get(value, value)  # if not found, keep original


def preprocess_internship_data(internship_data):
    preprocessed_data = internship_data.copy()
        
    if "Description" in preprocessed_data and isinstance(preprocessed_data["Description"], str):
        description = re.sub(r'[^\w\s]', '', preprocessed_data["Description"].lower())
        preprocessed_data["Description_as_string"] = description

    if "Eligibility Degree" in preprocessed_data and isinstance(preprocessed_data["Eligibility Degree"], str):
        preprocessed_data["Eligibility Degree_processed"] = preprocess_degree(preprocessed_data["Eligibility Degree"])

    if "Sector" in preprocessed_data and isinstance(preprocessed_data["Sector"], str):
        sector_lower = preprocessed_data["Sector"].lower()
        root_word_sector = lemmatizer.lemmatize(sector_lower)
        preprocessed_data["Sector_processed"] = preprocessed_data.get("Sector", "").lower().strip()

        
    if "Required Skills" in preprocessed_data and isinstance(preprocessed_data["Required Skills"], list):
        preprocessed_data["Required Skills_processed"] = [
            skill.lower().strip() for skill in preprocessed_data["Required Skills"]
        ]
    
    if "Location" in preprocessed_data and isinstance(preprocessed_data["Location"], str):
        locations = [loc.strip().lower() for loc in preprocessed_data["Location"].split(',')]
        preprocessed_data["Location_processed"] = locations

    combined_text = [
        preprocessed_data.get("Title", ""), 
        preprocessed_data.get("Description_as_string", ""),
        preprocessed_data.get("Sector_processed", ""),
        ' '.join(preprocessed_data.get("Eligibility Degree_processed", [])) if isinstance(preprocessed_data.get("Eligibility Degree_processed"), list) else preprocessed_data.get("Eligibility Degree_processed", ""),
        ' '.join(preprocessed_data.get("Required Skills_processed", [])),
        ' '.join(preprocessed_data.get("Location_processed", [])),
    ]
    preprocessed_data["combined_text"] = ' '.join(filter(None, combined_text))

    return preprocessed_data

def process_json_data(internships):
    processed_internships = []
    try:
        if not isinstance(internships, list):
            print("Error: The JSON file does not contain a list of objects.")
            return []
        for internship in internships:
            processed_internship = preprocess_internship_data(internship)
            processed_internships.append(processed_internship)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return processed_internships

