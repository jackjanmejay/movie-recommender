"""
Recommender that handles Movies, TV Series, and Documentaries
With explanations for each type
"""

import pandas as pd
from unified_loader import UnifiedDataLoader

class EnhancedRecommender:
    def __init__(self):
        self.loader = UnifiedDataLoader()
        self.content = None
        
    def initialize(self, min_ratings=5):
        """Load all data"""
        print("🎬 INITIALIZING ENHANCED RECOMMENDER")
        print("=" * 50)
        
        self.loader.load_movielens_data()
        self.loader.load_imdb_data_streaming()
        self.content = self.loader.combine_all(min_ratings=min_ratings)
        
        print(f"\n✅ Initialization complete! Loaded {len(self.content)} total titles")
        return self.content
        
    def recommend(self, content_type=None, genre=None, n=5, min_ratings=10):
        """Get recommendations with filters"""
        if self.content is None:
            print("❌ Please run initialize() first")
            return []
        
        filtered = self.content[self.content['rating_count'] >= min_ratings].copy()
        
        if len(filtered) == 0:
            print(f"⚠️ No content found with at least {min_ratings} ratings")
            return []
        
        if content_type:
            filtered = filtered[filtered['type'] == content_type]
            type_label = content_type
            if len(filtered) == 0:
                print(f"⚠️ No {content_type} found")
                return []
        else:
            type_label = "All Content"
            
        if genre and genre != 'All':
            genre_filtered = filtered[filtered['genres'].str.contains(genre, case=False, na=False)]
            if len(genre_filtered) == 0:
                print(f"⚠️ No {type_label} found in genre '{genre}'")
                return []
            filtered = genre_filtered
            genre_label = genre
        else:
            genre_label = "All Genres"
        
        filtered = filtered.sort_values('avg_rating', ascending=False)
        recommendations = filtered.head(n)
        
        print(f"\n🎯 {type_label} RECOMMENDATIONS - {genre_label}")
        print("=" * 70)
        
        results = []
        for idx, (_, row) in enumerate(recommendations.iterrows(), 1):
            explanation = self._generate_explanation(row)
            
            display_title = row['display_title']
            if pd.notna(row.get('year')) and row['year']:
                display_title = f"{display_title} ({int(row['year'])})"
            
            print(f"\n{idx}. {display_title}")
            print(f"   📺 {row['type']}")
            print(f"   ⭐ Rating: {row['avg_rating']:.1f}/10")
            print(f"   📊 {int(row['rating_count']):,} user ratings")
            print(f"   🏷️  Genres: {str(row['genres'])[:60]}")
            print(f"   💡 {explanation}")
            
            results.append({
                'title': row['display_title'],
                'year': int(row['year']) if pd.notna(row.get('year')) and row['year'] else None,
                'type': row['type'],
                'rating': round(row['avg_rating'], 1),
                'num_ratings': int(row['rating_count']),
                'genres': row['genres'],
                'explanation': explanation
            })
            
        return results
    
    def _generate_explanation(self, row):
        """Create human-readable explanation based on content type"""
        rating = row['avg_rating']
        num_ratings = int(row['rating_count'])
        
        if rating >= 9.0:
            rating_desc = "critically acclaimed masterpiece"
        elif rating >= 8.0:
            rating_desc = "highly rated"
        elif rating >= 7.0:
            rating_desc = "solid"
        else:
            rating_desc = "decent"
            
        if row['type'] == 'Movie':
            return f"This {rating_desc} film has earned {rating:.1f}/10 from {num_ratings:,} viewers"
        elif row['type'] == 'TV Series':
            return f"This {rating_desc} series has {num_ratings:,} ratings — perfect for binge-watching"
        else:
            return f"This {rating_desc} documentary is educational and compelling ({rating:.1f}/10 from {num_ratings:,} viewers)"
    
    def recommend_by_year(self, year, content_type=None, n=10, min_ratings=10):
        """Get best content from a specific year"""
        if self.content is None:
            print("❌ Please run initialize() first")
            return []
        
        filtered = self.content[self.content['rating_count'] >= min_ratings]
        filtered = filtered[filtered['year'] == year]
        
        if content_type and content_type != 'All':
            filtered = filtered[filtered['type'] == content_type]
            type_label = content_type
        else:
            type_label = "All Content"
        
        if len(filtered) == 0:
            print(f"\n⚠️ No {type_label} found from {year} with at least {min_ratings} ratings")
            return []
        
        filtered = filtered.sort_values('avg_rating', ascending=False).head(n)
        
        print(f"\n🎬 TOP {type_label.upper()} FROM {year}")
        print("=" * 60)
        
        results = []
        for idx, (_, row) in enumerate(filtered.iterrows(), 1):
            print(f"{idx}. {row['display_title']} ({row['type']})")
            print(f"   ⭐ {row['avg_rating']:.1f}/10 | 📊 {int(row['rating_count']):,} ratings")
            results.append(row['display_title'])
        
        return results
    
    def recommend_by_decade(self, decade, n=10, min_ratings=10):
        """Get best movies from a specific decade"""
        if self.content is None:
            print("❌ Please run initialize() first")
            return []
        
        decade_movies = self.content[
            (self.content['type'] == 'Movie') &
            (self.content['rating_count'] >= min_ratings) &
            (self.content['year'] >= decade) &
            (self.content['year'] < decade + 10)
        ].sort_values('avg_rating', ascending=False).head(n)
        
        if len(decade_movies) == 0:
            print(f"\n⚠️ No movies found from the {decade}s with at least {min_ratings} ratings")
            return []
        
        print(f"\n🎬 TOP MOVIES FROM THE {decade}s")
        print("=" * 60)
        
        results = []
        for idx, (_, row) in enumerate(decade_movies.iterrows(), 1):
            year_display = int(row['year']) if row['year'] else '?'
            print(f"{idx}. {row['display_title']} ({year_display})")
            print(f"   ⭐ {row['avg_rating']:.1f}/10 | 📊 {int(row['rating_count']):,} ratings")
            results.append(row['display_title'])
        
        return results
    
    def compare_types(self, min_ratings=10):
        """Compare average ratings across content types"""
        if self.content is None:
            print("❌ Please run initialize() first")
            return None
        
        filtered = self.content[self.content['rating_count'] >= min_ratings]
        
        print(f"\n📊 CONTENT TYPE COMPARISON (min {min_ratings} ratings)")
        print("=" * 60)
        
        comparison = filtered.groupby('type').agg({
            'avg_rating': 'mean',
            'rating_count': 'mean',
            'title': 'count'
        }).round(1)
        comparison.columns = ['Avg Rating (1-10)', 'Avg Votes', 'Total Titles']
        
        type_order = ['Movie', 'TV Series', 'Documentary']
        comparison = comparison.reindex([t for t in type_order if t in comparison.index])
        
        print(comparison.to_string())
        return comparison
    
    def search(self, keyword, n=10, min_ratings=10):
        """Search for content by title keyword"""
        if self.content is None:
            print("❌ Please run initialize() first")
            return []
        
        filtered = self.content[self.content['rating_count'] >= min_ratings]
        results = filtered[filtered['display_title'].str.contains(keyword, case=False, na=False)]
        
        if len(results) == 0:
            print(f"\n⚠️ No results found for '{keyword}' with at least {min_ratings} ratings")
            return []
        
        results = results.sort_values('avg_rating', ascending=False).head(n)
        
        print(f"\n🔍 SEARCH RESULTS: '{keyword}'")
        print("=" * 60)
        
        result_list = []
        for idx, (_, row) in enumerate(results.iterrows(), 1):
            year_str = f" ({int(row['year'])})" if pd.notna(row.get('year')) and row['year'] else ""
            print(f"{idx}. {row['display_title']}{year_str} ({row['type']})")
            print(f"   ⭐ {row['avg_rating']:.1f}/10 | 📊 {int(row['rating_count']):,} ratings")
            result_list.append(row['display_title'])
        
        return result_list
    
    def get_statistics(self):
        """Get overall statistics about the dataset"""
        if self.content is None:
            print("❌ Please run initialize() first")
            return
        
        print("\n📊 DATASET STATISTICS")
        print("=" * 60)
        print(f"Total titles: {len(self.content):,}")
        print(f"Average rating: {self.content['avg_rating'].mean():.2f}/10")
        print(f"Total ratings collected: {self.content['rating_count'].sum():,.0f}")
        
        years = self.content['year'].dropna()
        if len(years) > 0:
            print(f"Year range: {int(years.min())} - {int(years.max())}")
        
        print(f"\nContent breakdown:")
        for content_type in ['Movie', 'TV Series', 'Documentary']:
            if content_type in self.content['type'].values:
                count = len(self.content[self.content['type'] == content_type])
                percentage = (count / len(self.content)) * 100
                print(f"   • {content_type}: {count:,} ({percentage:.1f}%)")


def main():
    print("\n" + "="*70)
    print("🎬 INTELLIGENT MOVIE/TV/DOCUMENTARY RECOMMENDER SYSTEM")
    print("="*70)
    
    recommender = EnhancedRecommender()
    recommender.initialize(min_ratings=5)
    
    recommender.get_statistics()
    
    print("\n" + "="*70)
    recommender.recommend(content_type='Movie', n=5, min_ratings=50)
    
    print("\n" + "="*70)
    recommender.recommend(content_type='TV Series', n=5, min_ratings=10000)
    
    print("\n" + "="*70)
    recommender.recommend(content_type='Documentary', n=5, min_ratings=5000)
    
    print("\n" + "="*70)
    recommender.recommend(content_type='Movie', genre='Comedy', n=5, min_ratings=50)
    
    recommender.compare_types(min_ratings=50)
    
    recommender.search('Matrix', n=5, min_ratings=50)
    
    recommender.recommend_by_year(1994, content_type='Movie', n=5, min_ratings=50)
    
    recommender.recommend_by_year(2019, n=5, min_ratings=10000)
    
    recommender.recommend_by_decade(1990, n=5, min_ratings=50)
    
    print("\n" + "="*70)
    print("✅ All recommendations generated successfully!")
    print("="*70)


if __name__ == "__main__":
    main()
