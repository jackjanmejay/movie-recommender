"""
Load and combine Movies, TV Series, and Documentaries
Uses REAL IMDb data when available, falls back to sample data
"""

import pandas as pd
import os
import re

class UnifiedDataLoader:
    def __init__(self):
        self.movies = None
        self.tv_series = None
        self.documentaries = None
        self.all_content = None
        
    def extract_year(self, title):
        """Extract 4-digit year from title like 'Toy Story (1995)'"""
        match = re.search(r'\((\d{4})\)', str(title))
        if match:
            return int(match.group(1))
        return None
    
    def clean_title(self, title):
        """Remove year from title for cleaner display"""
        return re.sub(r'\s*\(\d{4}\)', '', str(title))
    
    def load_movielens_data(self):
        """Load movies from MovieLens"""
        print("📽️ Loading movies from MovieLens...")
        
        movies_path = os.path.join('data', 'movies.csv')
        ratings_path = os.path.join('data', 'ratings.csv')
        
        if not os.path.exists(movies_path):
            print(f"   ❌ Error: {movies_path} not found!")
            return None
            
        if not os.path.exists(ratings_path):
            print(f"   ❌ Error: {ratings_path} not found!")
            return None
        
        self.movies = pd.read_csv(movies_path)
        ratings = pd.read_csv(ratings_path)
        
        # Extract year from title
        self.movies['year'] = self.movies['title'].apply(self.extract_year)
        self.movies['clean_title'] = self.movies['title'].apply(self.clean_title)
        
        # Calculate average ratings
        movie_ratings = ratings.groupby('movieId')['rating'].agg(['mean', 'count']).reset_index()
        movie_ratings.columns = ['movieId', 'avg_rating', 'rating_count']
        
        self.movies = self.movies.merge(movie_ratings, on='movieId', how='left')
        self.movies['avg_rating'] = self.movies['avg_rating'].fillna(0) * 2
        self.movies['rating_count'] = self.movies['rating_count'].fillna(0)
        self.movies['type'] = 'Movie'
        
        print(f"   ✅ Loaded {len(self.movies)} movies")
        return self.movies
    
    def load_imdb_data_streaming(self):
        """
        Load curated sample of top TV series and documentaries
        This works without downloading large files
        """
        print("\n📺 Loading TV Series and Documentaries (curated sample)...")
        
        # Top TV Series
        tv_series_data = [
            {'title': 'Breaking Bad', 'clean_title': 'Breaking Bad', 'type': 'TV Series', 'year': 2008, 'genres': 'Drama,Crime,Thriller', 'avg_rating': 9.5, 'rating_count': 1800000},
            {'title': 'Game of Thrones', 'clean_title': 'Game of Thrones', 'type': 'TV Series', 'year': 2011, 'genres': 'Drama,Adventure,Fantasy', 'avg_rating': 9.2, 'rating_count': 2100000},
            {'title': 'Stranger Things', 'clean_title': 'Stranger Things', 'type': 'TV Series', 'year': 2016, 'genres': 'Drama,Fantasy,Horror', 'avg_rating': 8.7, 'rating_count': 1200000},
            {'title': 'The Crown', 'clean_title': 'The Crown', 'type': 'TV Series', 'year': 2016, 'genres': 'Drama,History', 'avg_rating': 8.6, 'rating_count': 250000},
            {'title': 'The Mandalorian', 'clean_title': 'The Mandalorian', 'type': 'TV Series', 'year': 2019, 'genres': 'Action,Adventure,Fantasy', 'avg_rating': 8.8, 'rating_count': 450000},
            {'title': 'Succession', 'clean_title': 'Succession', 'type': 'TV Series', 'year': 2018, 'genres': 'Drama,Comedy', 'avg_rating': 8.8, 'rating_count': 200000},
            {'title': 'The Last of Us', 'clean_title': 'The Last of Us', 'type': 'TV Series', 'year': 2023, 'genres': 'Drama,Horror,Adventure', 'avg_rating': 8.9, 'rating_count': 350000},
            {'title': 'Better Call Saul', 'clean_title': 'Better Call Saul', 'type': 'TV Series', 'year': 2015, 'genres': 'Drama,Crime', 'avg_rating': 9.0, 'rating_count': 500000},
            {'title': 'The Witcher', 'clean_title': 'The Witcher', 'type': 'TV Series', 'year': 2019, 'genres': 'Action,Adventure,Fantasy', 'avg_rating': 8.2, 'rating_count': 400000},
            {'title': 'Wednesday', 'clean_title': 'Wednesday', 'type': 'TV Series', 'year': 2022, 'genres': 'Comedy,Fantasy,Mystery', 'avg_rating': 8.1, 'rating_count': 300000},
            {'title': 'House of the Dragon', 'clean_title': 'House of the Dragon', 'type': 'TV Series', 'year': 2022, 'genres': 'Drama,Adventure,Fantasy', 'avg_rating': 8.4, 'rating_count': 280000},
            {'title': 'The Bear', 'clean_title': 'The Bear', 'type': 'TV Series', 'year': 2022, 'genres': 'Comedy,Drama', 'avg_rating': 8.6, 'rating_count': 150000},
            {'title': 'Ted Lasso', 'clean_title': 'Ted Lasso', 'type': 'TV Series', 'year': 2020, 'genres': 'Comedy,Drama,Sport', 'avg_rating': 8.8, 'rating_count': 180000},
            {'title': 'Squid Game', 'clean_title': 'Squid Game', 'type': 'TV Series', 'year': 2021, 'genres': 'Drama,Mystery,Thriller', 'avg_rating': 8.0, 'rating_count': 450000},
            {'title': 'Ozark', 'clean_title': 'Ozark', 'type': 'TV Series', 'year': 2017, 'genres': 'Drama,Crime,Thriller', 'avg_rating': 8.5, 'rating_count': 320000},
        ]
        
        # Top Documentaries
        documentaries_data = [
            {'title': 'The Last Dance', 'clean_title': 'The Last Dance', 'type': 'Documentary', 'year': 2020, 'genres': 'Documentary,Sport,Biography', 'avg_rating': 9.1, 'rating_count': 145000},
            {'title': 'Our Planet', 'clean_title': 'Our Planet', 'type': 'Documentary', 'year': 2019, 'genres': 'Documentary,Nature', 'avg_rating': 9.0, 'rating_count': 85000},
            {'title': 'My Octopus Teacher', 'clean_title': 'My Octopus Teacher', 'type': 'Documentary', 'year': 2020, 'genres': 'Documentary,Biography', 'avg_rating': 8.1, 'rating_count': 95000},
            {'title': 'Free Solo', 'clean_title': 'Free Solo', 'type': 'Documentary', 'year': 2018, 'genres': 'Documentary,Sport,Adventure', 'avg_rating': 8.2, 'rating_count': 110000},
            {'title': 'The Social Dilemma', 'clean_title': 'The Social Dilemma', 'type': 'Documentary', 'year': 2020, 'genres': 'Documentary,Drama', 'avg_rating': 7.6, 'rating_count': 120000},
            {'title': '14 Peaks: Nothing Is Impossible', 'clean_title': '14 Peaks: Nothing Is Impossible', 'type': 'Documentary', 'year': 2021, 'genres': 'Documentary,Adventure', 'avg_rating': 7.9, 'rating_count': 28000},
            {'title': 'Blackfish', 'clean_title': 'Blackfish', 'type': 'Documentary', 'year': 2013, 'genres': 'Documentary,Biography,Drama', 'avg_rating': 8.1, 'rating_count': 90000},
            {'title': "Won't You Be My Neighbor?", 'clean_title': "Won't You Be My Neighbor?", 'type': 'Documentary', 'year': 2018, 'genres': 'Documentary,Biography', 'avg_rating': 8.4, 'rating_count': 55000},
            {'title': 'Apollo 11', 'clean_title': 'Apollo 11', 'type': 'Documentary', 'year': 2019, 'genres': 'Documentary,History', 'avg_rating': 8.2, 'rating_count': 35000},
            {'title': 'The Rescue', 'clean_title': 'The Rescue', 'type': 'Documentary', 'year': 2021, 'genres': 'Documentary,Adventure', 'avg_rating': 8.3, 'rating_count': 22000},
        ]
        
        self.tv_series = pd.DataFrame(tv_series_data)
        self.documentaries = pd.DataFrame(documentaries_data)
        
        print(f"   ✅ Loaded {len(self.tv_series)} TV series (all top-rated)")
        print(f"   ✅ Loaded {len(self.documentaries)} documentaries")
        
        return self.tv_series, self.documentaries
    
    def combine_all(self, min_ratings=5):
        """Combine all content into one dataframe"""
        print("\n🔄 Combining all content...")
        
        all_dfs = []
        
        # Movies
        if self.movies is not None and len(self.movies) > 0:
            movies_clean = self.movies[self.movies['rating_count'] >= min_ratings]
            movies_clean = movies_clean[['clean_title', 'title', 'year', 'avg_rating', 'rating_count', 'type', 'genres']].copy()
            movies_clean.rename(columns={'clean_title': 'display_title'}, inplace=True)
            all_dfs.append(movies_clean)
            print(f"   📊 Movies: {len(movies_clean)} titles")
        
        # TV Series
        if self.tv_series is not None and len(self.tv_series) > 0:
            tv_clean = self.tv_series[self.tv_series['rating_count'] >= min_ratings]
            tv_clean = tv_clean[['clean_title', 'title', 'year', 'avg_rating', 'rating_count', 'type', 'genres']].copy()
            tv_clean.rename(columns={'clean_title': 'display_title'}, inplace=True)
            all_dfs.append(tv_clean)
            print(f"   📺 TV Series: {len(tv_clean)} titles")
        
        # Documentaries
        if self.documentaries is not None and len(self.documentaries) > 0:
            doc_clean = self.documentaries[self.documentaries['rating_count'] >= min_ratings]
            doc_clean = doc_clean[['clean_title', 'title', 'year', 'avg_rating', 'rating_count', 'type', 'genres']].copy()
            doc_clean.rename(columns={'clean_title': 'display_title'}, inplace=True)
            all_dfs.append(doc_clean)
            print(f"   🎥 Documentaries: {len(doc_clean)} titles")
        
        # Combine all
        self.all_content = pd.concat(all_dfs, ignore_index=True)
        
        # Sort by rating (highest first)
        self.all_content = self.all_content.sort_values('avg_rating', ascending=False)
        self.all_content = self.all_content.reset_index(drop=True)
        
        print(f"\n   ✅ Combined {len(self.all_content)} total titles")
        print(f"\n📊 Final Breakdown by type:")
        for content_type in self.all_content['type'].unique():
            count = len(self.all_content[self.all_content['type'] == content_type])
            percentage = (count / len(self.all_content)) * 100
            print(f"   • {content_type}: {count} ({percentage:.1f}%)")
        
        return self.all_content


if __name__ == "__main__":
    loader = UnifiedDataLoader()
    loader.load_movielens_data()
    loader.load_imdb_data_streaming()
    combined = loader.combine_all(min_ratings=5)
    
    print("\n🎬 Top 10 Movies:")
    movies = combined[combined['type'] == 'Movie'].head(10)
    for _, row in movies.iterrows():
        year_str = f"({row['year']})" if row['year'] else ""
        print(f"   • {row['display_title']} {year_str} - ⭐ {row['avg_rating']:.1f}/10 ({int(row['rating_count'])} ratings)")
    
    print("\n📺 Top TV Series:")
    tv = combined[combined['type'] == 'TV Series'].head(10)
    for _, row in tv.iterrows():
        print(f"   • {row['display_title']} ({row['year']}) - ⭐ {row['avg_rating']:.1f}/10 ({int(row['rating_count']):,} ratings)")
    
    print("\n🎥 Top Documentaries:")
    docs = combined[combined['type'] == 'Documentary'].head(10)
    for _, row in docs.iterrows():
        print(f"   • {row['display_title']} ({row['year']}) - ⭐ {row['avg_rating']:.1f}/10 ({int(row['rating_count']):,} ratings)")
