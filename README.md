# ai-based-food-recommendations

## Backend Setup (Windows)

# Uses FastAPI + scikit-learn

# Requires Python 3.12 (scikit-learn does NOT support 3.14)

# 1. Install Python 3.12

# Download: https://www.python.org/downloads/

# During install: check "Add Python to PATH"

# Verify installation:

py -0

# 2. Clone the repository

git clone <REPO_URL>
cd backend

# 3. Create virtual environment (Python 3.12)

py -3.12 -m venv .venv

# 4. Activate virtual environment

# Git Bash:

source .venv/Scripts/activate

# PowerShell:

# .\.venv\Scripts\Activate.ps1

# 5. Verify Python version

python --version

# 6. Install dependencies

python -m pip install --upgrade pip
pip install -r requirements.txt

# 7. Run the server

uvicorn main:app --reload

# 8. Open API docs

# http://127.0.0.1:8000/docs
