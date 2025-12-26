# ai-based-food-recommendations

## Backend Setup (Windows)

FastAPI + scikit-learn  
Python 3.12 required (scikit-learn does NOT support Python 3.14)

### 1. Install Python 3.12

Download: https://www.python.org/downloads/  
During install: check "Add Python to PATH"

Verify:

```bash
py -0
```

### 2. Clone repository

```bash
git clone <REPO_URL>
cd backend
```

### 3. Create virtual environment

```bash
py -3.12 -m venv .venv
```

### 4. Activate virtual environment

```bash
# Git Bash
source .venv/Scripts/activate

# PowerShell
.\.venv\Scripts\Activate.ps1
```

### 5. Verify Python version

```bash
python --version
```

### 6. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 7. Run backend server

```bash
python -m uvicorn main:app --reload
```

### 8. Open API docs

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Vite + Node.js

### 1. Install Node.js (LTS)

Download: https://nodejs.org/

Verify:

```bash
node -v
npm -v
```

### 2. Go to frontend directory

```bash
cd frontend
```

### 3. Install dependencies

```bash
npm install
```

### 4. Start frontend server

```bash
npm run dev
```

### 5. Open app

```text
http://localhost:5174
```
