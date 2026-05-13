"""
Simple popularity-based movie recommender
Recommends highest-rated movies with explanations
"""

import pandas as pd
import os

class PopularityRecommender:
    def __init__(self):
        self.movies = None
        self.ratings = None
        self.popular_movies = None
        
    def load_data(self):
        """Load movie and rating data"""
        print("📂 Loading data...")
        
        # Load movies
        movies_path = os.path.join('data', 'movies.csv')
        self.movies = pd.read_csv(movies_path)
        
        # Load ratings
        ratings_path = os.path.join('data', 'ratings.csv')
        self.ratings = pd.read_csv(ratings_path)
        
        print(f"   ✅ Loaded {len(self.movies)} movies")
        print(f"   ✅ Loaded {len(self.ratings)} ratings")
        
    def build_popularity_list(self, min_ratings=10):
        """
        Find most popular movies based on:
        - High average rating
        - At least 'min_ratings' number of ratings
        """
        print(f"📊 Building popularity list (min {min_ratings} ratings)...")
        
        # Calculate average rating per movie
        movie_ratings = self.ratings.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        
        # Flatten column names
        movie_ratings.columns = ['movieId', 'avg_rating', 'rating_count']
        
        # Filter movies with enough ratings
        popular = movie_ratings[movie_ratings['rating_count'] >= min_ratings]
        
        # Sort by average rating (highest first)
        popular = popular.sort_values('avg_rating', ascending=False)
        
        # Add movie titles
        self.popular_movies = popular.merge(
            self.movies[['movieId', 'title']], 
            on='movieId'
        )
        
        print(f"   ✅ Found {len(self.popular_movies)} popular movies")
        
    def recommend(self, user_id=None, n=5):
        """
        Recommend top N movies
        If user_id is provided, also show what they've watched
        """
        if self.popular_movies is None:
            self.build_popularity_list()
            
        print(f"\n🎬 Top {n} Movie Recommendations:")
        print("=" * 50)
        
        recommendations = []
        for idx, row in self.popular_movies.head(n).iterrows():
            # Create explanation
            explanation = f"⭐ {row['avg_rating']:.1f}/5 stars from {row['rating_count']:,} users"
            
            print(f"\n{idx+1}. {row['title']}")
            print(f"   → {explanation}")
            
            recommendations.append({
                'title': row['title'],
                'rating': round(row['avg_rating'], 1),
                'num_ratings': row['rating_count'],
                'explanation': explanation
            })
            
        # If user ID provided, show what they've already seen
        if user_id:
            self._show_user_history(user_id)
            
        return recommendations
    
    def _show_user_history(self, user_id):
        """Show movies this user has already rated"""
        user_ratings = self.ratings[self.ratings['userId'] == user_id]
        user_movies = user_ratings.merge(self.movies, on='movieId')
        
        print(f"\n📺 You've rated {len(user_movies)} movies")
        if len(user_movies) > 0:
            print("   Recently rated:")
            for _, row in user_movies.head(3).iterrows():
                print(f"   • {row['title']} ({row['rating']}★)")
                
    def get_top_by_genre(self, genre, n=5):
        """Bonus: Recommend top movies in a specific genre"""
        genre_movies = self.movies[self.movies['genres'].str.contains(genre, case=False)]
        genre_movies = genre_movies.merge(
            self.popular_movies[['movieId', 'avg_rating', 'rating_count']], 
            on='movieId'
        )
        genre_movies = genre_movies.sort_values('avg_rating', ascending=False)
        
        print(f"\n🎬 Top {genre} Movies:")
        print("=" * 40)
        
        for idx, row in genre_movies.head(n).iterrows():
            print(f"{idx+1}. {row['title']}")
            print(f"   ⭐ {row['avg_rating']:.1f}/5 ({row['rating_count']} ratings)")

def main():
    """Run the recommender"""
    print("🎬 MOVIE RECOMMENDER SYSTEM")
    print("=" * 40)
    
    # Create recommender
    recommender = PopularityRecommender()
    
    # Load data
    recommender.load_data()
    
    # Build popularity list
    recommender.build_popularity_list(min_ratings=50)
    
    # Get recommendations (with test user ID 1)
    recommendations = recommender.recommend(user_id=1, n=5)
    
    # Bonus: Show genre recommendations
    print("\n" + "=" * 40)
    recommender.get_top_by_genre("Comedy", n=3)

if __name__ == "__main__":
    main()
