<< 'EOF'
# 🎬 Intelligent Movie/TV/Documentary Recommender System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-red.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📌 Live Demo

🔗 **Live Demo**: [https://movie-recommender.onrender.com](https://movie-recommender.onrender.com)

## 📌 Overview

An **intelligent recommendation system** that suggests Movies, TV Series, and Documentaries with **human-readable explanations**. Built as a Master's-level portfolio project.

### 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Smart Recommendations** | Finds highest-rated content based on real user ratings |
| 💬 **Explanations** | "This critically acclaimed masterpiece has 9.5/10 from 1.8M viewers" |
| 📺 **Multi-type Support** | Movies (3,650+), TV Series (15), Documentaries (10) |
| 🎭 **Genre Filtering** | Comedy, Drama, Action, Crime, etc. |
| 📅 **Year Filtering** | Best of 1994, 2019, or any year |
| 📊 **Decade Analysis** | Top movies from 90s, 2000s, etc. |
| 🔍 **Keyword Search** | Find any movie/series by name |
| 🌐 **Web Interface** | Beautiful, responsive web UI |

## 🚀 Quick Start

### Local Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/movie-recommender.git
cd movie-recommender

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download MovieLens dataset
cd data
curl -O https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
unzip ml-latest-small.zip
mv ml-latest-small/* .
rmdir ml-latest-small
cd ..

# Run the web app
python src/app.py
