---
sidebar_position: 1
---

# Installation

Get Arc Flash Studio running on your local machine.

## Prerequisites

- **Python 3.9+** (for backend)
- **Node.js 18+** (for frontend)
- **Git** (for version control)

## Backend Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/arc-flash-studio.git
cd arc-flash-studio/backend
```

### 2. Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Backend
```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`

Interactive API docs at `http://localhost:8000/docs`

## Frontend Setup

### 1. Navigate to Frontend
```bash
cd ../frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Run Development Server
```bash
npm run dev
```

Application will open at `http://localhost:5173`

## Verify Installation

### Test Backend
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### Test Frontend

Open `http://localhost:5173` in your browser. You should see the Arc Flash Studio interface.

## Troubleshooting

### Backend won't start

- Verify Python version: `python --version` (must be 3.9+)
- Check virtual environment is activated: you should see `(venv)` in terminal
- Try reinstalling dependencies: `pip install -r requirements.txt --force-reinstall`

### Frontend won't start

- Verify Node version: `node --version` (must be 18+)
- Clear cache: `rm -rf node_modules && npm install`
- Check port 5173 is not in use

### Import errors

Make sure you're in the correct directory and virtual environment is activated.

## Next Steps

- [Quick Start Tutorial](./quick-start.md)
- [Architecture Overview](../architecture/overview.md)
- [API Reference](../api/overview.md)