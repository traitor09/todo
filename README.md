# Internship Recommendation System -
A full-stack web application to collect, manage, and recommend internships.
# Contributing Guidelines 

Thank you for your interest in contributing! Join our [Discord Community](https://discord.gg/7YgmBhS3h) 💜  
This project welcomes developers of all skill levels, and this guide will help you get started smoothly.  
  
To recognize the amazing people who help grow this project, we award badges : [See here!](https://traitor09.github.io/todo/)
## Prerequisites 

Before contributing, please ensure you have:

- Git 

- Node.js (version 18+) and npm  

- Python 3 (version 3.8+) and pip  

- A MongoDB Atlas account (you'll need a connection string).  

- A Clerk account (you'll need a publishable key for the frontend).  

If you're new to any of these, don’t worry -the steps below walk you through everything.

## Local Setup Guide (Important)

To avoid cluttering the README, all setup steps — including environment variables, required keys, and where to get them — are documented separately.

👉 **Follow the full setup guide here:**  
**[SETUP_LOCAL.md](./my_app/SETUP_LOCAL.md)**

This includes:
- Creating your `.env.local`
- Required environment variables
- MongoDB & Clerk keys
- Running backend & frontend


# Setting up the Project Locally  
The system has a separate frontend (React/Vite) and backend (Flask). Both require specific environment variables to run.  

## Fork The Repository 

Click the [Fork](https://github.com/traitor09/todo/fork) button at the top of the repository.  
This creates your copy that you can safely experiment with.

## Clone Your Fork

```bash
git clone https://github.com/traitor09/todo.git
cd todo
```
## Create a new Branch
Always make changes in a separate branch instead of main.

```bash
git checkout -b feature/my-new-feature
```


Use clear branch names:

`feature/...` for new features  
`fix/...` for bug fixes  
`docs/...` for documentation  
`refactor/...` for improvements  
### Backend Setup (Flask & MongoDB)

Navigate to the backend folder:

```bash
cd backend
```
Create the local configuration file:  

```bash
cp .env.example .env
```
Open the newly created file and replace the placeholders with your actual credentials:  

`MONGO_CONNECTION_STRING`: Your URI from MongoDB Atlas.  
`MONGO_DB_NAME`: The name of the database you want to use (e.g., dev_db).  

[Need your credentials? Detailed instructions on where to find your keys [HERE](https://github.com/traitor09/todo/blob/main/docs/ENV_INSTRUCTIONS.md) ]

(Optional) It is highly recommended to use a Virtual Environment (venv) to keep project dependencies separate from your global Python installation:  

- **Linux/macOS**
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

- **Windows (PowerShell)**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

- **Windows (CMD)**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

## Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Set up the database:

```bash
python setup_database.py
```

## Run the server:

```bash
python app.py
```
`Verification`: The terminal should show a message indicating the Flask server is running, usually at http://127.0.0.1:5000.  Keep this terminal running!


### Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

## Install dependencies:

```bash
npm install
```
## Create the local configuration file:  

```bash
cp .env.example .env
```
Open the file and replace the placeholders:

`VITE_API_URL`: This should point to your running backend: http://127.0.0.1:5000  
`VITE_CLERK_PUBLISHABLE_KEY`: Your publishable key from the Clerk dashboard.  
[Need your credentials? Detailed instructions on where to find your keys [HERE](https://github.com/traitor09/todo/blob/main/docs/ENV_INSTRUCTIONS.md) ]

## Run the Frontend:

```bash
npm run dev
```
`Verification`: The terminal will show a local URL, typically http://localhost:5173 (or another port).  Open this URL in your browser to see the application!

## Ensure
While contributing, please:

- Keep code clean and well-commented
- Follow existing coding style
- Test your changes locally
- Make commits small and meaningful

Example commit message:

`Add skill preprocessing step to recommendation logic`

## Commit and Push
```bash
git add .
git commit -m "Clear and descriptive message"
git push origin feature/my-new-feature
```
## Open a Pull Request
Go to your fork on GitHub.
Click Compare & pull request.
Write a clear description of what you changed and why.
Submit the PR.

PR Tips:

- Be polite and collaborative
- Explain the reasoning behind your changes
- Screenshots are helpful if UI-related
- A maintainer will review your PR and give feedback or approve it.


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
