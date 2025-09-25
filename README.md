# STRUCTURE

## Project Structure

- **backend/**
  - `app.py` – Main Flask application
  - `setup_DB.py` – Script to populate MongoDB
  - `requirements.txt` – Python dependencies
  - **utils/**
    - `utils.py` – MongoDB connection helper
    - `preprocess.py` – Data preprocessing functions
    - `rule_recommendation.py` – Rule-based recommendation logic
    - `ml_recommendation.py` – ML-based recommendation logic

- **frontend/**
  - `package.json` – NPM dependencies
  - `tsconfig.json` – TypeScript configuration
  - **src/**
    - `App.tsx` – Main React component
    - `index.tsx` – React entry point
    - **components/** – React components folder

- **Data/**
  - `dataset.json` – Sample internship listings
