"""
Load and explore movie ratings data
"""

import pandas as pd
import os

def load_movies():
    """Load movies.csv into a DataFrame"""
    file_path = os.path.join('data', 'movies.csv')
    df = pd.read_csv(file_path)
    print(f"✅ Loaded {len(df)} movies")
    return df

def load_ratings():
    """Load ratings.csv into a DataFrame"""
    file_path = os.path.join('data', 'ratings.csv')
    df = pd.read_csv(file_path)
    print(f"✅ Loaded {len(df)} ratings from {df['userId'].nunique()} users")
    return df

def explore_data():
    """Print basic statistics about the dataset"""
    movies = load_movies()
    ratings = load_ratings()
    
    print("\n📊 Data Overview:")
    print(f"  - Movies: {len(movies)}")
    print(f"  - Ratings: {len(ratings)}")
    print(f"  - Users: {ratings['userId'].nunique()}")
    print(f"  - Rating range: {ratings['rating'].min()} to {ratings['rating'].max()}")
    print(f"  - Average rating: {ratings['rating'].mean():.2f}")
    
    # Show first 5 movies
    print("\n🎬 First 5 movies:")
    print(movies.head())
    
    return movies, ratings

if __name__ == "__main__":
    explore_data()
