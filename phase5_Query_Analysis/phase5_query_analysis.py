"""
Phase 5: Query Execution and Analysis
YouTube Trending Videos Dataset - Neo4j Graph Database
Run all query groups with checkpoints
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from py2neo import Graph
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import zipfile
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        plt.style.use('default')
sns.set_palette("husl")

# ============================================================================
# CONFIGURATION
# ============================================================================

# Read from environment variables or use defaults
NEO4J_URI = os.getenv('NEO4J_URI', 'AddYour_Bolt_URI_Here')  # e.g., "bolt://
NEO4J_USER = os.getenv('NEO4J_USER', 'AddYour_Username_Here')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'AddYour_Password_Here')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'AddYour_Database_Name_Here')

# Execution parameters
QUERY_TIMEOUT = 60
BATCH_SIZE = 1000
SAMPLE_LIMIT = 1000

# Directories - All outputs go to a separate repository
BASE_DIR = Path('.')
OUTPUT_REPO_DIR = BASE_DIR / 'phase5_output'
RESULTS_DIR = OUTPUT_REPO_DIR / 'query_results'
VISUALIZATIONS_DIR = OUTPUT_REPO_DIR / 'visualizations'
REPORTS_DIR = OUTPUT_REPO_DIR / 'reports'

# Execution log
execution_log = {
    'start_time': datetime.now().isoformat(),
    'queries': [],
    'errors': [],
    'checkpoints': []
}

# ============================================================================
# SETUP FUNCTIONS
# ============================================================================

def setup_directories():
    """Create necessary directories in the output repository"""
    # Create main output repository directory
    OUTPUT_REPO_DIR.mkdir(exist_ok=True)
    print(f"✓ Created output repository: {OUTPUT_REPO_DIR}")
    
    # Create subdirectories
    for dir_path in [RESULTS_DIR, VISUALIZATIONS_DIR, REPORTS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def connect_to_neo4j():
    """Connect to Neo4j database"""
    try:
        graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        graph.run("RETURN 1 as test")
        print(f"✓ Connected to Neo4j at {NEO4J_URI}")
        return graph
    except Exception as e:
        print(f"✗ Failed to connect to Neo4j: {e}")
        execution_log['errors'].append({
            'time': datetime.now().isoformat(),
            'error': str(e),
            'context': 'connection'
        })
        sys.exit(1)

def ensure_indexes(graph):
    """Ensure all necessary indexes exist"""
    indexes = [
        "CREATE INDEX IF NOT EXISTS FOR (v:Video) ON (v.video_id)",
        "CREATE INDEX IF NOT EXISTS FOR (ch:Channel) ON (ch.channel_title)",
        "CREATE INDEX IF NOT EXISTS FOR (c:Category) ON (c.category_name)",
        "CREATE INDEX IF NOT EXISTS FOR (t:Tag) ON (t.tag_name)",
        "CREATE INDEX IF NOT EXISTS FOR (co:Country) ON (co.country_code)",
        "CREATE INDEX IF NOT EXISTS FOR (v:Video) ON (v.views)",
        "CREATE INDEX IF NOT EXISTS FOR (v:Video) ON (v.engagement_ratio)",
    ]
    
    for index_query in indexes:
        try:
            graph.run(index_query)
            index_name = index_query.split("FOR")[1].split("ON")[0].strip()
            print(f"✓ Index ensured: {index_name}")
        except Exception as e:
            print(f"⚠️  Index creation warning: {e}")

# ============================================================================
# QUERY EXECUTION FUNCTIONS
# ============================================================================

def execute_query(graph, query, params=None, description=""):
    """Execute a Cypher query and return results"""
    start_time = datetime.now()
    try:
        if params:
            result = graph.run(query, **params).data()
        else:
            result = graph.run(query).data()
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        execution_log['queries'].append({
            'time': start_time.isoformat(),
            'description': description,
            'status': 'success',
            'duration_seconds': duration,
            'rows_returned': len(result)
        })
        
        return result, duration
    except Exception as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        execution_log['queries'].append({
            'time': start_time.isoformat(),
            'description': description,
            'status': 'error',
            'duration_seconds': duration,
            'error': str(e)
        })
        
        execution_log['errors'].append({
            'time': datetime.now().isoformat(),
            'error': str(e),
            'context': description
        })
        
        print(f"✗ Query failed: {description}")
        print(f"  Error: {e}")
        return None, duration

def save_results_to_csv(results, filepath, batch_size=BATCH_SIZE):
    """Save query results to CSV with batching if needed"""
    if not results:
        return 0
    
    try:
        df = pd.DataFrame(results)
        
        if len(df) > batch_size:
            # Save in batches
            num_batches = (len(df) + batch_size - 1) // batch_size
            base_path = Path(filepath)
            base_name = base_path.stem
            base_dir = base_path.parent
            
            for i in range(num_batches):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, len(df))
                batch_df = df.iloc[start_idx:end_idx]
                batch_path = base_dir / f"{base_name}_batch_{i+1}.csv"
                batch_df.to_csv(batch_path, index=False)
            
            print(f"  ✓ Saved {len(df)} rows in {num_batches} batches to {base_dir}")
            return len(df)
        else:
            df.to_csv(filepath, index=False)
            print(f"  ✓ Saved {len(df)} rows to {filepath}")
            return len(df)
    except Exception as e:
        print(f"  ✗ Failed to save CSV: {e}")
        return 0

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_bar_chart(data, x_col, y_col, title, filepath, xlabel=None, ylabel=None, top_n=10):
    """Create a bar chart visualization"""
    try:
        df = pd.DataFrame(data)
        if len(df) > top_n:
            df = df.head(top_n)
        
        plt.figure(figsize=(12, 6))
        plt.barh(range(len(df)), df[y_col].values)
        plt.yticks(range(len(df)), df[x_col].values)
        plt.xlabel(ylabel or y_col)
        plt.ylabel(xlabel or x_col)
        plt.title(title)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Created visualization: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create visualization: {e}")
        return False

def create_line_chart(data, x_col, y_col, title, filepath, xlabel=None, ylabel=None):
    """Create a line chart visualization"""
    try:
        df = pd.DataFrame(data)
        plt.figure(figsize=(12, 6))
        plt.plot(df[x_col], df[y_col], marker='o')
        plt.xlabel(xlabel or x_col)
        plt.ylabel(ylabel or y_col)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Created visualization: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create visualization: {e}")
        return False

def create_heatmap(data, title, filepath, x_col=None, y_col=None, value_col=None):
    """Create a heatmap visualization"""
    try:
        df = pd.DataFrame(data)
        
        if x_col and y_col and value_col:
            pivot_df = df.pivot_table(values=value_col, index=y_col, columns=x_col, aggfunc='mean')
        else:
            # Assume numeric columns
            pivot_df = df.select_dtypes(include=[np.number])
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_df, annot=True, fmt='.2f', cmap='YlOrRd', cbar_kws={'label': value_col or 'Value'})
        plt.title(title)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Created visualization: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create visualization: {e}")
        return False

def create_scatter_plot(data, x_col, y_col, title, filepath, xlabel=None, ylabel=None):
    """Create a scatter plot visualization"""
    try:
        df = pd.DataFrame(data)
        plt.figure(figsize=(10, 6))
        plt.scatter(df[x_col], df[y_col], alpha=0.5)
        plt.xlabel(xlabel or x_col)
        plt.ylabel(ylabel or y_col)
        plt.title(title)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Created visualization: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create visualization: {e}")
        return False

# ============================================================================
# GROUP A: SIMPLE QUERIES
# ============================================================================

def run_group_a_queries(graph):
    """Run Group A: Simple Queries"""
    print("\n" + "=" * 80)
    print("GROUP A: SIMPLE QUERIES")
    print("=" * 80)
    
    group_a_files = []
    summary_content = "# Group A: Simple Queries Summary\n\n"
    
    # A.1: Top Categories by Video Count
    print("\n[A.1] Top Categories by Video Count")
    query_a1 = """
    MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category)
    RETURN c.category_name as category_name, COUNT(v) as video_count
    ORDER BY video_count DESC
    """
    results_a1, duration_a1 = execute_query(graph, query_a1, description="A.1: Top Categories")
    if results_a1:
        csv_path = RESULTS_DIR / 'groupA_A1_top_categories.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupA_A1_top_categories.png'
        save_results_to_csv(results_a1, csv_path)
        create_bar_chart(results_a1, 'category_name', 'video_count', 
                        'Top Categories by Video Count', viz_path,
                        xlabel='Category', ylabel='Video Count')
        group_a_files.append({'query': 'A.1', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## A.1: Top Categories by Video Count\n\n"
        summary_content += f"This query identifies the most popular video categories by counting videos in each category. "
        summary_content += f"The results show {len(results_a1)} categories, with the top category having {results_a1[0]['video_count']} videos. "
        summary_content += "This helps understand content distribution across categories.\n\n"
    
    # A.2: Top Channels by Total Views
    print("\n[A.2] Top Channels by Total Views")
    query_a2 = """
    MATCH (ch:Channel)-[:CHANNEL_HAS_VIDEO]->(v:Video)
    RETURN ch.channel_title as channel_title, SUM(v.views) as total_views, COUNT(v) as video_count
    ORDER BY total_views DESC
    LIMIT 20
    """
    results_a2, duration_a2 = execute_query(graph, query_a2, description="A.2: Top Channels")
    if results_a2:
        csv_path = RESULTS_DIR / 'groupA_A2_top_channels.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupA_A2_top_channels.png'
        save_results_to_csv(results_a2, csv_path)
        create_bar_chart(results_a2, 'channel_title', 'total_views', 
                        'Top Channels by Total Views', viz_path,
                        xlabel='Channel', ylabel='Total Views', top_n=15)
        group_a_files.append({'query': 'A.2', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## A.2: Top Channels by Total Views\n\n"
        summary_content += f"This query identifies the most successful channels by aggregating total views across all their videos. "
        summary_content += f"The top channel has {results_a2[0]['total_views']:,} total views across {results_a2[0]['video_count']} videos. "
        summary_content += "This reveals which channels have the strongest audience reach.\n\n"
    
    # A.3: Videos by Country
    print("\n[A.3] Videos by Country")
    query_a3 = """
    MATCH (v:Video)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
    RETURN co.country_code as country_code, co.country_name as country_name, COUNT(v) as video_count
    ORDER BY video_count DESC
    """
    results_a3, duration_a3 = execute_query(graph, query_a3, description="A.3: Videos by Country")
    if results_a3:
        csv_path = RESULTS_DIR / 'groupA_A3_videos_by_country.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupA_A3_videos_by_country.png'
        save_results_to_csv(results_a3, csv_path)
        create_bar_chart(results_a3, 'country_code', 'video_count', 
                        'Videos by Country', viz_path,
                        xlabel='Country', ylabel='Video Count')
        group_a_files.append({'query': 'A.3', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## A.3: Videos by Country\n\n"
        summary_content += f"This query shows the distribution of trending videos across different countries. "
        summary_content += f"The results reveal {len(results_a3)} countries with {sum(r['video_count'] for r in results_a3):,} total videos. "
        summary_content += "This helps understand regional content trends.\n\n"
    
    # A.4: Top Videos by Views
    print("\n[A.4] Top Videos by Views")
    query_a4 = """
    MATCH (v:Video)
    RETURN v.video_id as video_id, v.title as title, v.views as views, v.country as country
    ORDER BY v.views DESC
    LIMIT 50
    """
    results_a4, duration_a4 = execute_query(graph, query_a4, description="A.4: Top Videos")
    if results_a4:
        csv_path = RESULTS_DIR / 'groupA_A4_top_videos.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupA_A4_top_videos.png'
        save_results_to_csv(results_a4, csv_path)
        # Truncate titles for visualization
        viz_data = [{'title': r['title'][:50] + '...' if len(r['title']) > 50 else r['title'], 
                    'views': r['views']} for r in results_a4[:20]]
        create_bar_chart(viz_data, 'title', 'views', 
                        'Top Videos by Views', viz_path,
                        xlabel='Video Title', ylabel='Views', top_n=20)
        group_a_files.append({'query': 'A.4', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## A.4: Top Videos by Views\n\n"
        summary_content += f"This query identifies the most viewed trending videos. "
        summary_content += f"The top video has {results_a4[0]['views']:,} views. "
        summary_content += "This reveals which individual videos gained the most traction.\n\n"
    
    # A.5: Average Engagement by Category
    print("\n[A.5] Average Engagement by Category")
    query_a5 = """
    MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category)
    RETURN c.category_name as category_name, 
           AVG(v.engagement_ratio) as avg_engagement,
           AVG(v.views) as avg_views,
           COUNT(v) as video_count
    ORDER BY avg_engagement DESC
    """
    results_a5, duration_a5 = execute_query(graph, query_a5, description="A.5: Engagement by Category")
    if results_a5:
        csv_path = RESULTS_DIR / 'groupA_A5_engagement_by_category.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupA_A5_engagement_by_category.png'
        save_results_to_csv(results_a5, csv_path)
        create_bar_chart(results_a5, 'category_name', 'avg_engagement', 
                        'Average Engagement by Category', viz_path,
                        xlabel='Category', ylabel='Average Engagement Ratio')
        group_a_files.append({'query': 'A.5', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## A.5: Average Engagement by Category\n\n"
        summary_content += f"This query analyzes engagement rates across different categories. "
        summary_content += f"The category with highest engagement has an average ratio of {results_a5[0]['avg_engagement']:.4f}. "
        summary_content += "This helps identify which content types generate the most audience interaction.\n\n"
    
    # A.6: Day-of-Week Trending Patterns
    print("\n[A.6] Day-of-Week Trending Patterns")
    query_a6 = """
    MATCH (v:Video)-[:VIDEO_TRENDING_ON]->(d:Day)
    RETURN d.day_name as day_name, 
           COUNT(v) as video_count,
           AVG(v.views) as avg_views,
           AVG(v.engagement_ratio) as avg_engagement
    ORDER BY video_count DESC
    """
    results_a6, duration_a6 = execute_query(graph, query_a6, description="A.6: Day Patterns")
    if results_a6:
        csv_path = RESULTS_DIR / 'groupA_A6_day_patterns.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupA_A6_day_patterns.png'
        save_results_to_csv(results_a6, csv_path)
        # Order by day of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ordered_results = sorted(results_a6, key=lambda x: day_order.index(x['day_name']))
        create_line_chart(ordered_results, 'day_name', 'video_count', 
                         'Trending Videos by Day of Week', viz_path,
                         xlabel='Day of Week', ylabel='Video Count')
        group_a_files.append({'query': 'A.6', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## A.6: Day-of-Week Trending Patterns\n\n"
        summary_content += f"This query reveals patterns in when videos trend throughout the week. "
        summary_content += f"The busiest day has {max(r['video_count'] for r in results_a6)} trending videos. "
        summary_content += "This helps understand weekly content distribution patterns.\n\n"
    
    # Save Group A index
    index_path = RESULTS_DIR / 'groupA_index.json'
    with open(index_path, 'w') as f:
        json.dump({'files': group_a_files, 'timestamp': datetime.now().isoformat()}, f, indent=2)
    print(f"\n✓ Saved Group A index to {index_path}")
    
    # Save Group A summary
    summary_path = REPORTS_DIR / 'phase5_groupA_summary.md'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    print(f"✓ Saved Group A summary to {summary_path}")
    
    execution_log['checkpoints'].append({
        'checkpoint': 'Group A Complete',
        'time': datetime.now().isoformat(),
        'files_generated': len(group_a_files)
    })
    
    return group_a_files

# ============================================================================
# GROUP B: COMPLEX QUERIES
# ============================================================================

def run_group_b_queries(graph):
    """Run Group B: Complex Queries"""
    print("\n" + "=" * 80)
    print("GROUP B: COMPLEX QUERIES")
    print("=" * 80)
    
    group_b_files = []
    summary_content = "# Group B: Complex Queries Summary\n\n"
    statistical_tests = []
    
    # B.1: Channels with High Engagement Videos
    print("\n[B.1] Channels with High Engagement Videos")
    query_b1 = """
    MATCH (ch:Channel)-[:CHANNEL_HAS_VIDEO]->(v:Video)
    WHERE v.engagement_ratio > 0.1
    RETURN ch.channel_title as channel_title, 
           COUNT(v) as high_engagement_videos,
           AVG(v.engagement_ratio) as avg_engagement,
           AVG(v.views) as avg_views,
           SUM(v.views) as total_views
    ORDER BY high_engagement_videos DESC
    LIMIT 20
    """
    results_b1, duration_b1 = execute_query(graph, query_b1, description="B.1: High Engagement Channels")
    if results_b1:
        csv_path = RESULTS_DIR / 'groupB_B1_high_engagement_channels.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupB_B1_high_engagement_channels.png'
        save_results_to_csv(results_b1, csv_path)
        create_scatter_plot(results_b1, 'high_engagement_videos', 'avg_engagement', 
                           'Channels: High Engagement Videos vs Avg Engagement', viz_path,
                           xlabel='High Engagement Videos Count', ylabel='Average Engagement Ratio')
        group_b_files.append({'query': 'B.1', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## B.1: Channels with High Engagement Videos\n\n"
        summary_content += f"This query identifies channels that consistently produce high-engagement content. "
        summary_content += f"{len(results_b1)} channels have videos with engagement ratios above 0.1. "
        summary_content += "This reveals which creators build strong audience connections.\n\n"
    
    # B.2: Category Performance by Country
    print("\n[B.2] Category Performance by Country")
    query_b2 = """
    MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category),
          (v)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
    RETURN co.country_code as country_code, 
           c.category_name as category_name,
           COUNT(v) as video_count,
           AVG(v.views) as avg_views,
           AVG(v.engagement_ratio) as avg_engagement
    ORDER BY co.country_code, video_count DESC
    """
    results_b2, duration_b2 = execute_query(graph, query_b2, description="B.2: Category by Country")
    if results_b2:
        csv_path = RESULTS_DIR / 'groupB_B2_category_by_country.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupB_B2_category_by_country.png'
        save_results_to_csv(results_b2, csv_path)
        create_heatmap(results_b2, 'Category Performance by Country (Video Count)', viz_path,
                      x_col='category_name', y_col='country_code', value_col='video_count')
        group_b_files.append({'query': 'B.2', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## B.2: Category Performance by Country\n\n"
        summary_content += f"This query analyzes how different categories perform across countries. "
        summary_content += f"The results show {len(set(r['country_code'] for r in results_b2))} countries and {len(set(r['category_name'] for r in results_b2))} categories. "
        summary_content += "This reveals regional content preferences and cultural differences.\n\n"
    
    # B.3: Tag Co-occurrence with Categories
    print("\n[B.3] Tag Co-occurrence with Categories")
    query_b3 = """
    MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category),
          (v)-[:VIDEO_HAS_TAG]->(t:Tag)
    WITH c.category_name as category, t.tag_name as tag, COUNT(v) as co_count
    WHERE co_count > 10
    RETURN category, tag, co_count
    ORDER BY category, co_count DESC
    LIMIT 100
    """
    results_b3, duration_b3 = execute_query(graph, query_b3, description="B.3: Tag Co-occurrence")
    if results_b3:
        csv_path = RESULTS_DIR / 'groupB_B3_tag_cooccurrence.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupB_B3_tag_cooccurrence.png'
        save_results_to_csv(results_b3, csv_path)
        # Create pivot table for heatmap
        pivot_data = pd.DataFrame(results_b3).pivot_table(
            values='co_count', index='category', columns='tag', aggfunc='sum', fill_value=0
        )
        # Take top tags by frequency
        top_tags = pivot_data.sum().nlargest(15).index
        pivot_subset = pivot_data[top_tags]
        plt.figure(figsize=(14, 8))
        sns.heatmap(pivot_subset, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Co-occurrence Count'})
        plt.title('Tag Co-occurrence with Categories (Top 15 Tags)')
        plt.tight_layout()
        plt.savefig(viz_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Created visualization: {viz_path}")
        group_b_files.append({'query': 'B.3', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## B.3: Tag Co-occurrence with Categories\n\n"
        summary_content += f"This query analyzes which tags frequently appear together with categories. "
        summary_content += f"The results show {len(results_b3)} tag-category pairs with co-occurrence > 10. "
        summary_content += "This reveals content tagging patterns and category associations.\n\n"
    
    # B.4: Cross-Country Video Analysis
    print("\n[B.4] Cross-Country Video Analysis")
    query_b4 = """
    MATCH (v:Video)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
    WITH v.video_id as video_id, COLLECT(co.country_code) as countries
    WHERE SIZE(countries) > 1
    RETURN video_id, countries, SIZE(countries) as country_count
    ORDER BY country_count DESC
    LIMIT 50
    """
    results_b4, duration_b4 = execute_query(graph, query_b4, description="B.4: Cross-Country Videos")
    if results_b4:
        csv_path = RESULTS_DIR / 'groupB_B4_cross_country_videos.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupB_B4_cross_country_videos.png'
        save_results_to_csv(results_b4, csv_path)
        # Create bar chart of country counts
        country_count_data = [{'country_count': r['country_count'], 'video_id': r['video_id'][:20]} 
                             for r in results_b4]
        create_bar_chart(country_count_data, 'video_id', 'country_count', 
                        'Videos Trending in Multiple Countries', viz_path,
                        xlabel='Video ID', ylabel='Number of Countries', top_n=20)
        group_b_files.append({'query': 'B.4', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## B.4: Cross-Country Video Analysis\n\n"
        summary_content += f"This query identifies videos that trended in multiple countries. "
        summary_content += f"{len(results_b4)} videos trended in more than one country, with the top video trending in {results_b4[0]['country_count']} countries. "
        summary_content += "This reveals globally appealing content.\n\n"
    
    # B.5: Channel Performance Analysis
    print("\n[B.5] Channel Performance Analysis")
    query_b5 = """
    MATCH (ch:Channel)-[:CHANNEL_HAS_VIDEO]->(v:Video)
    WITH ch.channel_title as channel_title,
         COUNT(v) as video_count,
         AVG(v.views) as avg_views,
         AVG(v.engagement_ratio) as avg_engagement,
         MAX(v.views) as max_views,
         MIN(v.views) as min_views
    WHERE video_count >= 5
    RETURN channel_title, video_count, avg_views, avg_engagement, max_views, min_views
    ORDER BY avg_engagement DESC
    LIMIT 30
    """
    results_b5, duration_b5 = execute_query(graph, query_b5, description="B.5: Channel Performance")
    if results_b5:
        csv_path = RESULTS_DIR / 'groupB_B5_channel_performance.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupB_B5_channel_performance.png'
        save_results_to_csv(results_b5, csv_path)
        create_scatter_plot(results_b5, 'avg_views', 'avg_engagement', 
                           'Channel Performance: Avg Views vs Avg Engagement', viz_path,
                           xlabel='Average Views', ylabel='Average Engagement Ratio')
        group_b_files.append({'query': 'B.5', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## B.5: Channel Performance Analysis\n\n"
        summary_content += f"This query analyzes channel performance metrics for channels with at least 5 videos. "
        summary_content += f"{len(results_b5)} channels meet this criteria. "
        summary_content += "This reveals which channels balance viewership and engagement effectively.\n\n"
        
        # Statistical test: Correlation between views and engagement
        df_b5 = pd.DataFrame(results_b5)
        correlation = df_b5['avg_views'].corr(df_b5['avg_engagement'])
        statistical_tests.append({
            'test': 'B.5: Views vs Engagement Correlation',
            'correlation': correlation,
            'p_value': 'N/A',
            'interpretation': f"Correlation of {correlation:.4f} between average views and engagement ratio"
        })
    
    # Save statistical tests
    if statistical_tests:
        stats_path = REPORTS_DIR / 'statistical_tests.csv'
        pd.DataFrame(statistical_tests).to_csv(stats_path, index=False)
        print(f"\n✓ Saved statistical tests to {stats_path}")
    
    # Save Group B index
    index_path = RESULTS_DIR / 'groupB_index.json'
    with open(index_path, 'w') as f:
        json.dump({'files': group_b_files, 'timestamp': datetime.now().isoformat()}, f, indent=2)
    print(f"\n✓ Saved Group B index to {index_path}")
    
    # Save Group B summary
    summary_path = REPORTS_DIR / 'phase5_groupB_summary.md'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    print(f"✓ Saved Group B summary to {summary_path}")
    
    execution_log['checkpoints'].append({
        'checkpoint': 'Group B Complete',
        'time': datetime.now().isoformat(),
        'files_generated': len(group_b_files)
    })
    
    return group_b_files

# ============================================================================
# GROUP C: VISUALIZATION & STATISTICAL ANALYSIS
# ============================================================================

def run_group_c_analysis(graph):
    """Run Group C: Visualization & Statistical Analysis"""
    print("\n" + "=" * 80)
    print("GROUP C: VISUALIZATION & STATISTICAL ANALYSIS")
    print("=" * 80)
    
    group_c_files = []
    summary_content = "# Group C: Visualization & Statistical Analysis Summary\n\n"
    
    # C.1: Correlation Analysis
    print("\n[C.1] Correlation Analysis")
    query_c1 = """
    MATCH (v:Video)
    RETURN v.views as views, 
           v.likes as likes,
           v.dislikes as dislikes,
           v.comment_count as comment_count,
           v.engagement_ratio as engagement_ratio,
           v.like_dislike_ratio as like_dislike_ratio
    LIMIT 10000
    """
    results_c1, duration_c1 = execute_query(graph, query_c1, description="C.1: Correlation Data")
    if results_c1:
        df_c1 = pd.DataFrame(results_c1)
        correlation_matrix = df_c1.corr()
        
        csv_path = RESULTS_DIR / 'groupC_C1_correlation_matrix.csv'
        viz_path = VISUALIZATIONS_DIR / 'groupC_C1_correlation_heatmap.png'
        correlation_matrix.to_csv(csv_path)
        print(f"  ✓ Saved correlation matrix to {csv_path}")
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={'label': 'Correlation Coefficient'})
        plt.title('Video Metrics Correlation Matrix')
        plt.tight_layout()
        plt.savefig(viz_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Created visualization: {viz_path}")
        
        group_c_files.append({'analysis': 'C.1', 'csv': str(csv_path), 'viz': str(viz_path)})
        summary_content += "## C.1: Correlation Analysis\n\n"
        summary_content += f"This analysis examines relationships between video metrics. "
        summary_content += f"Key correlations reveal how views, engagement, and interactions relate to each other. "
        summary_content += "This helps understand which metrics drive video performance.\n\n"
    
    # C.2: Engagement Distribution Analysis
    print("\n[C.2] Engagement Distribution Analysis")
    query_c2 = """
    MATCH (v:Video)
    RETURN v.engagement_ratio as engagement_ratio,
           v.views as views,
           v.country as country
    """
    results_c2, duration_c2 = execute_query(graph, query_c2, description="C.2: Engagement Distribution")
    if results_c2:
        df_c2 = pd.DataFrame(results_c2)
        
        # Distribution plot
        viz_path = VISUALIZATIONS_DIR / 'groupC_C2_engagement_distribution.png'
        plt.figure(figsize=(12, 6))
        plt.hist(df_c2['engagement_ratio'], bins=50, edgecolor='black')
        plt.xlabel('Engagement Ratio')
        plt.ylabel('Frequency')
        plt.title('Distribution of Engagement Ratios')
        plt.tight_layout()
        plt.savefig(viz_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Created visualization: {viz_path}")
        
        group_c_files.append({'analysis': 'C.2', 'viz': str(viz_path)})
        summary_content += "## C.2: Engagement Distribution Analysis\n\n"
        summary_content += f"This analysis examines the distribution of engagement ratios across all videos. "
        summary_content += f"The mean engagement ratio is {df_c2['engagement_ratio'].mean():.4f} with a standard deviation of {df_c2['engagement_ratio'].std():.4f}. "
        summary_content += "This reveals the overall engagement patterns in the dataset.\n\n"
    
    # C.3: Category-Country Network Analysis
    print("\n[C.3] Category-Country Network Analysis")
    query_c3 = """
    MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category),
          (v)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
    WITH c.category_name as category, co.country_code as country, COUNT(v) as video_count
    RETURN category, country, video_count
    ORDER BY video_count DESC
    """
    results_c3, duration_c3 = execute_query(graph, query_c3, description="C.3: Category-Country Network")
    if results_c3:
        csv_path = RESULTS_DIR / 'groupC_C3_category_country_network.csv'
        save_results_to_csv(results_c3, csv_path)
        group_c_files.append({'analysis': 'C.3', 'csv': str(csv_path)})
        summary_content += "## C.3: Category-Country Network Analysis\n\n"
        summary_content += f"This analysis examines the network of relationships between categories and countries. "
        summary_content += f"The results show {len(results_c3)} category-country connections. "
        summary_content += "This reveals content preferences across different regions.\n\n"
    
    # Save Group C summary
    summary_path = REPORTS_DIR / 'phase5_groupC_summary.md'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    print(f"✓ Saved Group C summary to {summary_path}")
    
    execution_log['checkpoints'].append({
        'checkpoint': 'Group C Complete',
        'time': datetime.now().isoformat(),
        'files_generated': len(group_c_files)
    })
    
    return group_c_files

# ============================================================================
# FINAL REPORT GENERATION
# ============================================================================

def create_final_report(group_a_files, group_b_files, group_c_files):
    """Create final comprehensive report"""
    print("\n" + "=" * 80)
    print("GENERATING FINAL REPORT")
    print("=" * 80)
    
    report_content = f"""# Phase 5: Query Execution and Analysis Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report presents a comprehensive analysis of the YouTube Trending Videos dataset using Neo4j graph database queries. The analysis is organized into three major groups:

- **Group A: Simple Queries** - Basic aggregations and statistics
- **Group B: Complex Queries** - Advanced pattern analysis and correlations
- **Group C: Visualization & Statistical Analysis** - Deep statistical insights

---

## Group A: Simple Queries

Group A executed {len(group_a_files)} simple queries focusing on:
- Top categories, channels, and videos
- Country distribution
- Engagement patterns
- Day-of-week trends

### Files Generated:
"""
    
    for file_info in group_a_files:
        report_content += f"- **{file_info['query']}**: {file_info['csv']}, {file_info['viz']}\n"
    
    report_content += f"""

---

## Group B: Complex Queries

Group B executed {len(group_b_files)} complex queries focusing on:
- High-engagement channels
- Category-country performance
- Tag co-occurrence patterns
- Cross-country video analysis
- Channel performance metrics

### Files Generated:
"""
    
    for file_info in group_b_files:
        report_content += f"- **{file_info['query']}**: {file_info['csv']}, {file_info['viz']}\n"
    
    report_content += f"""

---

## Group C: Visualization & Statistical Analysis

Group C performed {len(group_c_files)} advanced analyses:
- Correlation analysis between metrics
- Engagement distribution
- Category-country network analysis

### Files Generated:
"""
    
    for file_info in group_c_files:
        if 'csv' in file_info:
            report_content += f"- **{file_info['analysis']}**: {file_info['csv']}, {file_info.get('viz', 'N/A')}\n"
        else:
            report_content += f"- **{file_info['analysis']}**: {file_info.get('viz', 'N/A')}\n"
    
    report_content += f"""

---

## Execution Statistics

- **Total Queries Executed**: {len(execution_log['queries'])}
- **Successful Queries**: {len([q for q in execution_log['queries'] if q['status'] == 'success'])}
- **Failed Queries**: {len([q for q in execution_log['queries'] if q['status'] == 'error'])}
- **Total Execution Time**: {(datetime.now() - datetime.fromisoformat(execution_log['start_time'])).total_seconds():.2f} seconds

---

## Key Insights

1. **Content Distribution**: The dataset shows diverse content across multiple categories and countries.
2. **Engagement Patterns**: Engagement ratios vary significantly across categories and channels.
3. **Regional Preferences**: Different countries show distinct content preferences.
4. **Tag Associations**: Tags exhibit strong co-occurrence patterns with specific categories.

---

## Recommendations

1. Focus on high-engagement categories for content strategy
2. Analyze successful channels for best practices
3. Consider regional preferences when targeting audiences
4. Leverage tag patterns for content optimization

---

## Next Steps

1. Review individual query results in detail
2. Perform additional statistical tests if needed
3. Create custom visualizations for specific insights
4. Export data for further analysis in other tools

---

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    report_path = REPORTS_DIR / 'phase5_query_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"✓ Saved final report to {report_path}")
    
    return report_path

def create_zip_archive():
    """Create zip archive of all Phase 5 results"""
    print("\n" + "=" * 80)
    print("CREATING ZIP ARCHIVE")
    print("=" * 80)
    
    zip_path = OUTPUT_REPO_DIR / 'phase5_results_full.zip'
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all results
        for file_path in RESULTS_DIR.rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(OUTPUT_REPO_DIR))
        
        # Add all visualizations
        for file_path in VISUALIZATIONS_DIR.rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(OUTPUT_REPO_DIR))
        
        # Add all reports
        for file_path in REPORTS_DIR.rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(OUTPUT_REPO_DIR))
        
        # Add execution log
        log_path = OUTPUT_REPO_DIR / 'phase5_execution_log.json'
        if log_path.exists():
            zipf.write(log_path, log_path.relative_to(OUTPUT_REPO_DIR))
    
    print(f"✓ Created zip archive: {zip_path}")
    return zip_path

# ============================================================================
# CHECKPOINT FUNCTION
# ============================================================================

def checkpoint(group_name, files_generated):
    """Pause execution and wait for user confirmation"""
    print("\n" + "=" * 80)
    print(f"CHECKPOINT: {group_name} COMPLETE")
    print("=" * 80)
    print(f"✓ Generated {files_generated} files")
    print(f"✓ Output Repository: {OUTPUT_REPO_DIR}")
    print(f"✓ Results saved to: {RESULTS_DIR}")
    print(f"✓ Visualizations saved to: {VISUALIZATIONS_DIR}")
    print(f"✓ Reports saved to: {REPORTS_DIR}")
    print("\n" + "=" * 80)
    print("PAUSING FOR USER CONFIRMATION")
    print("=" * 80)
    response = input(f"\n{group_name} completed. Proceed to next group? (yes/no): ").strip().lower()
    return response == 'yes'

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("=" * 80)
    print("PHASE 5: QUERY EXECUTION AND ANALYSIS")
    print("=" * 80)
    
    # Setup
    print("\n[SETUP] Initializing...")
    setup_directories()
    graph = connect_to_neo4j()
    ensure_indexes(graph)
    
    # Save execution log to output repository
    log_path = OUTPUT_REPO_DIR / 'phase5_execution_log.json'
    
    try:
        # Group A: Simple Queries
        group_a_files = run_group_a_queries(graph)
        execution_log['end_time'] = datetime.now().isoformat()
        with open(log_path, 'w') as f:
            json.dump(execution_log, f, indent=2)
        
        if not checkpoint('GROUP A', len(group_a_files)):
            print("\n⚠️  User chose to stop. Exiting.")
            return
        
        # Group B: Complex Queries
        group_b_files = run_group_b_queries(graph)
        execution_log['end_time'] = datetime.now().isoformat()
        with open(log_path, 'w') as f:
            json.dump(execution_log, f, indent=2)
        
        if not checkpoint('GROUP B', len(group_b_files)):
            print("\n⚠️  User chose to stop. Exiting.")
            return
        
        # Group C: Visualization & Statistical Analysis
        group_c_files = run_group_c_analysis(graph)
        
        # Final Report
        create_final_report(group_a_files, group_b_files, group_c_files)
        
        # Create Zip Archive
        create_zip_archive()
        
        # Final execution log
        execution_log['end_time'] = datetime.now().isoformat()
        execution_log['status'] = 'complete'
        with open(log_path, 'w') as f:
            json.dump(execution_log, f, indent=2)
        
        print("\n" + "=" * 80)
        print("PHASE 5 COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\nSummary:")
        print(f"  - Group A Files: {len(group_a_files)}")
        print(f"  - Group B Files: {len(group_b_files)}")
        print(f"  - Group C Files: {len(group_c_files)}")
        print(f"  - Execution Log: {log_path}")
        print(f"\nAll outputs saved to separate repository:")
        print(f"  - Output Repository: {OUTPUT_REPO_DIR}")
        print(f"  - Results: {RESULTS_DIR}")
        print(f"  - Visualizations: {VISUALIZATIONS_DIR}")
        print(f"  - Reports: {REPORTS_DIR}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        execution_log['status'] = 'interrupted'
        execution_log['end_time'] = datetime.now().isoformat()
        with open(log_path, 'w') as f:
            json.dump(execution_log, f, indent=2)
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
        execution_log['status'] = 'error'
        execution_log['end_time'] = datetime.now().isoformat()
        execution_log['fatal_error'] = str(e)
        with open(log_path, 'w') as f:
            json.dump(execution_log, f, indent=2)
        raise

if __name__ == "__main__":
    main()

