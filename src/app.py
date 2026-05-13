"""
Flask Web Application for Movie/TV/Documentary Recommender
Run with: python src/app.py
Then open browser to: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from enhanced_recommender import EnhancedRecommender
import pandas as pd

app = Flask(__name__)

# Initialize recommender once when app starts
print("🎬 Loading recommender system...")
recommender = EnhancedRecommender()
recommender.initialize(min_ratings=5)
print("✅ Recommender ready!")

# Store available genres (extracted from movies)
all_genres = [
    'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 
    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 
    'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 
    'Thriller', 'War', 'Western'
]

@app.route('/')
def home():
    """Home page with recommendation form"""
    return render_template('index.html', genres=all_genres)

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint to get recommendations"""
    try:
        # Get user input
        content_type = request.form.get('content_type', 'Movie')
        genre = request.form.get('genre', None)
        n = int(request.form.get('n', 5))
        
        # Get recommendations
        if genre and genre != 'All':
            results = recommender.recommend(
                content_type=content_type,
                genre=genre,
                n=n,
                min_ratings=50
            )
        else:
            results = recommender.recommend(
                content_type=content_type,
                n=n,
                min_ratings=50
            )
        
        # Return as JSON
        return jsonify({
            'success': True,
            'recommendations': results,
            'content_type': content_type,
            'genre': genre if genre != 'All' else 'All Genres'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/search', methods=['POST'])
def search():
    """API endpoint to search by keyword"""
    try:
        keyword = request.form.get('keyword', '')
        n = int(request.form.get('n', 10))
        
        results = recommender.search(keyword, n=n, min_ratings=10)
        
        return jsonify({
            'success': True,
            'keyword': keyword,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/by_year', methods=['POST'])
def by_year():
    """API endpoint to get recommendations by year"""
    try:
        year = int(request.form.get('year', 1994))
        content_type = request.form.get('content_type', 'Movie')
        n = int(request.form.get('n', 10))
        
        results = recommender.recommend_by_year(
            year=year,
            content_type=content_type,
            n=n,
            min_ratings=50
        )
        
        return jsonify({
            'success': True,
            'year': year,
            'content_type': content_type,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/stats')
def stats():
    """Get statistics about the dataset"""
    stats_data = {
        'total_titles': len(recommender.content),
        'avg_rating': round(recommender.content['avg_rating'].mean(), 2),
        'total_ratings': int(recommender.content['rating_count'].sum()),
        'movies': len(recommender.content[recommender.content['type'] == 'Movie']),
        'tv_series': len(recommender.content[recommender.content['type'] == 'TV Series']),
        'documentaries': len(recommender.content[recommender.content['type'] == 'Documentary'])
    }
    return jsonify(stats_data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
