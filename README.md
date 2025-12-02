# ⚡ Arc Flash Studio

> Modern web-based arc flash calculator compliant with IEEE 1584-2018 standard

## 📁 Project Structure
```
arc-flash-studio/
├── docs-site/          # Docusaurus documentation website
├── backend/            # FastAPI + calculation engine
├── frontend/           # React + Vite web application
├── docs/               # Technical documentation & diagrams
│   ├── diagrams/       # D2 architecture diagrams
│   └── *.md            # Design documents
├── README.md           # This file
└── .gitignore
```

## 🚀 Quick Start

### Documentation Site
```bash
cd docs-site
npm install
npm start
# Opens http://localhost:3000
```

### Backend API
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
# Opens http://localhost:8000
```

### Frontend Application
```bash
cd frontend
npm install
npm run dev
# Opens http://localhost:5173
```

## 📚 Documentation

See [docs-site/](docs-site/) for full documentation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-61DAFB.svg)](https://reactjs.org/)

## 🎯 Features

- IEEE 1584-2018 compliant arc flash calculations
- Modern, intuitive web interface
- Support for radial power systems
- Equipment library management
- Printable arc flash labels
- Project save/load functionality


## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](LICENSE)

## ⚠️ Disclaimer

This software is for educational and reference purposes. Always consult with qualified electrical engineers for safety-critical calculations.
