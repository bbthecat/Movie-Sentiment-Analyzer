# 🎬 Movie Sentiment Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**AI-powered movie sentiment analysis with beautiful web interface**

</div>

---

## ✨ Features

### 🎯 Core Functionality
- **🔍 Movie Search** - Find movies using OMDb API
- **📊 Sentiment Analysis** - AI-powered review analysis using Hugging Face models
- **📈 Beautiful Dashboard** - Interactive charts and statistics
- **💾 Data Persistence** - JSON-based storage system
- **🔄 Multiple Data Sources** - Upload, generate, or import from TMDb

### 🛠️ Technical Features
- **⚡ FastAPI Backend** - High-performance async API
- **🎨 Modern Frontend** - Responsive web interface
- **🐳 Docker Support** - Easy deployment with containers
- **🧪 Comprehensive Testing** - Unit tests with pytest
- **📱 Mobile Friendly** - Responsive design for all devices

### 🌐 API Integrations
- **OMDb API** - Movie metadata and search
- **TMDb API** - Real movie reviews import
- **Hugging Face** - State-of-the-art sentiment analysis models (supports lightweight mode for low-memory deploys)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- API keys for OMDb and TMDb (optional but recommended)

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/movie-sentiment-analyzer.git
cd movie-sentiment-analyzer
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
cp env.example .env
# Edit .env and add your API keys:
# OMDB_API_KEY=your_omdb_key_here
# TMDB_API_KEY=your_tmdb_key_here
```

### 3. Run the Application
```bash
# Development server
uvicorn app:app --reload

# Or using Docker
docker-compose up --build
```

### 4. Open Your Browser
Navigate to [http://localhost:8000](http://localhost:8000) and start analyzing! 🎉

---

## 🎮 How to Use

### 1. **Search for a Movie**
- Enter a movie title in the search box
- Select from the dropdown results

### 2. **Add Reviews**
Choose one of these options:
- **📁 Upload CSV/JSON** - Upload your own review files
- **🎲 Generate Mock Data** - Create sample reviews for testing
- **🌐 Import from TMDb** - Fetch real reviews from The Movie Database

### 3. **Analyze Sentiment**
- Click "Analyze Reviews" to run AI sentiment analysis
- View results with beautiful charts and statistics

### 4. **Export Results**
- Download analysis as CSV
- View detailed breakdown of each review

---

## 📊 API Endpoints

### 🎬 Movie Operations
```http
GET  /api/movies/search?query={title}     # Search movies
GET  /api/movies/{imdb_id}                # Get movie details
```

### 📝 Review Management
```http
POST /api/reviews/{imdb_id}/upload        # Upload CSV/JSON reviews
POST /api/reviews/{imdb_id}/use-sample    # Use sample data
POST /api/reviews/{imdb_id}/generate      # Generate mock reviews
POST /api/reviews/{imdb_id}/import/tmdb   # Import from TMDb
```

### 🧠 Analysis & Results
```http
POST /api/analyze/{imdb_id}               # Run sentiment analysis
GET  /api/summary/{imdb_id}               # Get analysis summary
GET  /api/analysis/{imdb_id}              # Get detailed results
GET  /api/export/{imdb_id}.csv            # Export as CSV
POST /api/analyze-text                    # Analyze single text
```

### 🔧 System
```http
GET  /api/health                          # Health check
GET  /docs                               # API documentation
```

---

## 🏗️ Project Structure

```
movie-sentiment-analyzer/
├── 🎬 app.py                    # Main FastAPI application
├── 📁 backend/                  # Backend modules
│   ├── app.py                   # Alternative app entry point
│   ├── config.py                # Configuration settings
│   ├── models.py                # Pydantic models
│   ├── omdb_client.py           # OMDb API client
│   ├── tmdb_client.py           # TMDb API client
│   ├── sentiment_hf.py          # Hugging Face sentiment
│   ├── persistence_json.py      # JSON data persistence
│   └── data/                    # Data storage
│       ├── movies/              # Movie metadata
│       ├── reviews/             # Review data
│       ├── analysis/            # Analysis results
│       └── samples/             # Sample data
├── 🎨 frontend/                 # Frontend files
│   ├── index.html               # Main HTML page
│   ├── styles.css               # Styling
│   └── app.js                   # JavaScript logic
├── 🧪 tests/                    # Test files
│   ├── test_analyze.py          # Analysis tests
│   └── test_fetch.py            # API tests
├── 🐳 Dockerfile                # Docker configuration
├── 🐳 docker-compose.yml        # Docker Compose setup
├── 🧾 render.yaml               # Render blueprint (Docker-based deploy)
├── 📋 requirements.txt          # Python dependencies
└── 📄 env.example               # Environment variables template
```

---

## 🚀 Deployment

### 🟣 Render (Docker, using render.yaml)
Option A — One‑click via Blueprint:
1. Push this repo to GitHub
2. In Render, click "New +" → "Blueprint" and point to your repo
3. Render will detect `render.yaml` and create a Web Service
4. Set environment variables (see below). The blueprint sets `LIGHTWEIGHT_MODE=1` by default to fit 512MB plan
5. Deploy. Health check path: `/api/health`

Option B — Manual Web Service from Dockerfile:
1. New → Web Service → Build from Dockerfile (root)
2. Set `PORT=8000` and any API keys
3. Start command (if overriding): `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`

### 🐳 Docker (local)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t movie-sentiment-analyzer .
docker run -p 8000:8000 movie-sentiment-analyzer
```

---

## ⚙️ Configuration

### Environment Variables
```bash
# Required API Keys
OMDB_API_KEY=your_omdb_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here

# Optional Settings
HF_MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
DATA_DIR=backend/data
PORT=8000

# Memory-saving mode (recommended for Render free tier 512MB)
LIGHTWEIGHT_MODE=1
```

### API Keys Setup
1. **OMDb API**: Get free key at [omdbapi.com](http://www.omdbapi.com/apikey.aspx)
2. **TMDb API**: Get free key at [themoviedb.org](https://www.themoviedb.org/settings/api)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_analyze.py
```

---

## 📈 Performance

- **⚡ Fast Response Times** - Optimized FastAPI backend
- **🧠 Efficient AI Models** - Lightweight sentiment analysis (fallback mode for low RAM)
- **💾 Smart Caching** - Reduces API calls and improves speed
- **📱 Responsive Design** - Works on all devices

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/movie-sentiment-analyzer.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Start development server
uvicorn app:app --reload
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OMDb** - For providing free movie data API
- **TMDb** - For comprehensive movie database
- **Hugging Face** - For state-of-the-art NLP models
- **FastAPI** - For the amazing web framework
- **Contributors** - Thank you for your contributions!

---


<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>
