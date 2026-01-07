"""
Phase 4: Graph Database Setup and Data Ingestion
YouTube Trending Videos Dataset - Neo4j Graph Database
"""

import pandas as pd
import numpy as np
from py2neo import Graph, Node, Relationship, Transaction
from py2neo.database import Transaction as Tx
import ast
import os
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Configuration
# Neo4j Aura Cloud Database (EXAMPLE - DO NOT USE REAL CREDENTIALS)
NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j+s://xxxxx.databases.neo4j.io')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'your_password_here')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'neo4j')
BATCH_SIZE = 1000  # Number of rows to process per batch

# Country name mapping
COUNTRY_NAMES = {
    'US': 'United States',
    'GB': 'Great Britain',
    'CA': 'Canada',
    'IN': 'India'
}

print("=" * 80)
print("PHASE 4: GRAPH DATABASE SETUP AND DATA INGESTION")
print("=" * 80)

# ============================================================================
# STEP 1: Database Setup and Connection
# ============================================================================

print("\n[1] Setting up Neo4j Connection...")
print("-" * 80)

def connect_to_neo4j(uri, user, password):
    """Connect to Neo4j database"""
    try:
        graph = Graph(uri, auth=(user, password))
        # Test connection
        graph.run("RETURN 1 as test")
        print(f"✓ Connected to Neo4j at {uri}")
        return graph
    except Exception as e:
        print(f"✗ Failed to connect to Neo4j: {e}")
        print("\nPlease ensure:")
        print("  1. Neo4j Aura instance is running (check https://console.neo4j.io)")
        print("  2. Wait 60 seconds after instance creation if recently created")
        print("  3. Credentials are correct (URI, username, password)")
        print("  4. Internet connection is available (for Aura cloud database)")
        print("\nTo change connection settings, modify NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD in the script")
        return None

graph = connect_to_neo4j(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

if graph is None:
    print("\n⚠️  Cannot proceed without database connection.")
    print("   Please set up Neo4j and update connection credentials.")
    exit(1)

# ============================================================================
# STEP 2: Clear Existing Data (Optional - for fresh start)
# ============================================================================

print("\n[2] Clearing Existing Data (if any)...")
print("-" * 80)

try:
    # Delete all nodes and relationships
    graph.run("MATCH (n) DETACH DELETE n")
    print("✓ Cleared existing data from database")
except Exception as e:
    print(f"⚠️  Error clearing data: {e}")

# ============================================================================
# STEP 3: Load and Prepare Data
# ============================================================================

print("\n[3] Loading Cleaned Dataset...")
print("-" * 80)

try:
    df = pd.read_csv('youtube_trending_cleaned.csv')
    print(f"✓ Loaded dataset: {len(df):,} rows, {len(df.columns)} columns")
except FileNotFoundError:
    print("✗ Error: youtube_trending_cleaned.csv not found. Please run Phase 2 first.")
    exit(1)

# Parse dates
df['trending_date'] = pd.to_datetime(df['trending_date'])
df['publish_time'] = pd.to_datetime(df['publish_time'])

# Parse tags_list
def parse_tags_safe(x):
    if pd.isna(x) or x == '' or x == '[]':
        return []
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        try:
            if x.startswith('[') and x.endswith(']'):
                return ast.literal_eval(x)
            else:
                return [x]
        except:
            return []
    return []

if df['tags_list'].dtype == 'object':
    df['tags_list'] = df['tags_list'].apply(parse_tags_safe)

# Clean tag names (remove extra quotes and normalize)
def clean_tag(tag):
    if isinstance(tag, str):
        # Remove extra quotes
        tag = tag.strip('"\'')
        # Remove empty strings
        if tag == '' or tag == '""':
            return None
        return tag.strip()
    return None

print(f"✓ Data prepared for ingestion")

# ============================================================================
# STEP 4: Create Indexes
# ============================================================================

print("\n[4] Creating Indexes...")
print("-" * 80)

indexes = [
    # Video indexes
    "CREATE INDEX video_id_index IF NOT EXISTS FOR (v:Video) ON (v.video_id)",
    "CREATE INDEX video_trending_date_index IF NOT EXISTS FOR (v:Video) ON (v.trending_date)",
    "CREATE INDEX video_views_index IF NOT EXISTS FOR (v:Video) ON (v.views)",
    "CREATE INDEX video_engagement_index IF NOT EXISTS FOR (v:Video) ON (v.engagement_ratio)",
    
    # Channel indexes
    "CREATE INDEX channel_title_index IF NOT EXISTS FOR (ch:Channel) ON (ch.channel_title)",
    "CREATE INDEX channel_total_views_index IF NOT EXISTS FOR (ch:Channel) ON (ch.total_views)",
    
    # Category indexes
    "CREATE INDEX category_name_index IF NOT EXISTS FOR (c:Category) ON (c.category_name)",
    
    # Country indexes
    "CREATE INDEX country_code_index IF NOT EXISTS FOR (co:Country) ON (co.country_code)",
    
    # Tag indexes
    "CREATE INDEX tag_name_index IF NOT EXISTS FOR (t:Tag) ON (t.tag_name)",
    
    # Day indexes
    "CREATE INDEX day_name_index IF NOT EXISTS FOR (d:Day) ON (d.day_name)",
]

for index_query in indexes:
    try:
        graph.run(index_query)
        index_name = index_query.split("INDEX")[1].split("IF")[0].strip()
        print(f"✓ Created index: {index_name}")
    except Exception as e:
        print(f"⚠️  Index creation warning: {e}")

# ============================================================================
# STEP 5: Create Nodes - Countries
# ============================================================================

print("\n[5] Creating Country Nodes...")
print("-" * 80)

countries = df['country'].unique()
country_nodes = {}

for country_code in countries:
    country_name = COUNTRY_NAMES.get(country_code, country_code)
    # Use Cypher MERGE for better performance
    graph.run("""
        MERGE (co:Country {country_code: $country_code})
        SET co.country_name = $country_name
    """, country_code=country_code, country_name=country_name)
    country_nodes[country_code] = country_code  # Store code for reference
    print(f"✓ Created Country node: {country_code} ({country_name})")

print(f"✓ Created {len(country_nodes)} Country nodes")

# ============================================================================
# STEP 6: Create Nodes - Categories
# ============================================================================

print("\n[6] Creating Category Nodes...")
print("-" * 80)

categories = df[['category_id', 'category_name']].drop_duplicates()
category_nodes = {}

for _, row in categories.iterrows():
    category_id = int(row['category_id'])
    category_name = str(row['category_name'])
    # Use Cypher MERGE for better performance
    graph.run("""
        MERGE (c:Category {category_id: $category_id})
        SET c.category_name = $category_name
    """, category_id=category_id, category_name=category_name)
    category_nodes[category_id] = category_id  # Store ID for reference
    print(f"✓ Created Category node: {category_id} ({category_name})")

print(f"✓ Created {len(category_nodes)} Category nodes")

# ============================================================================
# STEP 7: Create Nodes - Channels (with aggregated stats)
# ============================================================================

print("\n[7] Creating Channel Nodes...")
print("-" * 80)

channel_stats = df.groupby('channel_title').agg({
    'views': 'sum',
    'engagement_ratio': 'mean',
    'video_id': 'count'
}).reset_index()
channel_stats.columns = ['channel_title', 'total_views', 'avg_engagement_ratio', 'video_count']

channel_nodes = {}
# Batch create channel nodes for better performance
for _, row in channel_stats.iterrows():
    channel_title = str(row['channel_title'])
    graph.run("""
        MERGE (ch:Channel {channel_title: $channel_title})
        SET ch.total_views = $total_views,
            ch.avg_engagement_ratio = $avg_engagement_ratio,
            ch.video_count = $video_count
    """, channel_title=channel_title,
        total_views=int(row['total_views']),
        avg_engagement_ratio=float(row['avg_engagement_ratio']),
        video_count=int(row['video_count']))
    channel_nodes[channel_title] = channel_title  # Store title for reference

print(f"✓ Created {len(channel_nodes):,} Channel nodes")

# ============================================================================
# STEP 8: Create Nodes - Tags
# ============================================================================

print("\n[8] Creating Tag Nodes...")
print("-" * 80)

all_tags = set()
for tags_list in df['tags_list']:
    if isinstance(tags_list, list):
        for tag in tags_list:
            cleaned_tag = clean_tag(tag)
            if cleaned_tag and len(cleaned_tag) > 0:
                all_tags.add(cleaned_tag)

tag_nodes = {}
# Batch create tag nodes for better performance
batch_tags = list(all_tags)
for i in range(0, len(batch_tags), 1000):
    batch = batch_tags[i:i+1000]
    for tag_name in batch:
        graph.run("MERGE (t:Tag {tag_name: $tag_name})", tag_name=tag_name)
        tag_nodes[tag_name] = tag_name  # Store name for reference

print(f"✓ Created {len(tag_nodes):,} Tag nodes")

# ============================================================================
# STEP 9: Create Nodes - Days of Week
# ============================================================================

print("\n[9] Creating Day-of-Week Nodes...")
print("-" * 80)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_nodes = {}

for day_name in days:
    graph.run("MERGE (d:Day {day_name: $day_name})", day_name=day_name)
    day_nodes[day_name] = day_name  # Store name for reference
    print(f"✓ Created Day node: {day_name}")

print(f"✓ Created {len(day_nodes)} Day nodes")

# ============================================================================
# STEP 10: Create Video Nodes and Relationships (Batch Processing)
# ============================================================================

print("\n[10] Creating Video Nodes and Relationships (Batch Processing)...")
print("-" * 80)

def create_video_batch(batch_rows, graph, country_nodes, category_nodes, 
                       channel_nodes, tag_nodes, day_nodes):
    """Create video nodes and relationships in batch for better performance"""
    
    batch_data = []
    for _, row in batch_rows.iterrows():
        # Prepare video properties
        video_id = str(row['video_id'])
        title = str(row['title']) if pd.notna(row['title']) else ""
        # Limit title length (parameterized queries handle special characters automatically)
        title = title[:200]
        views = int(row['views']) if pd.notna(row['views']) else 0
        likes = float(row['likes']) if pd.notna(row['likes']) else 0.0
        dislikes = float(row['dislikes']) if pd.notna(row['dislikes']) else 0.0
        comment_count = int(row['comment_count']) if pd.notna(row['comment_count']) else 0
        engagement_ratio = float(row['engagement_ratio']) if pd.notna(row['engagement_ratio']) else 0.0
        like_dislike_ratio = float(row['like_dislike_ratio']) if pd.notna(row['like_dislike_ratio']) else 0.0
        trending_date = row['trending_date'].strftime('%Y-%m-%d') if pd.notna(row['trending_date']) else ""
        publish_time = row['publish_time'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['publish_time']) else ""
        days_to_trend = int(row['days_to_trend']) if pd.notna(row['days_to_trend']) else 0
        
        country_code = str(row['country'])
        video_unique_id = f"{video_id}_{country_code}"
        category_id = int(row['category_id'])
        channel_title = str(row['channel_title'])
        trending_day = str(row['trending_day_of_week']) if pd.notna(row['trending_day_of_week']) else None
        
        # Get cleaned tags
        tags_list = row['tags_list']
        cleaned_tags = []
        if isinstance(tags_list, list):
            for tag in tags_list:
                cleaned_tag = clean_tag(tag)
                if cleaned_tag and cleaned_tag in tag_nodes:
                    cleaned_tags.append(cleaned_tag)
        
        batch_data.append({
            'video_unique_id': video_unique_id,
            'video_id': video_id,
            'title': title,
            'views': views,
            'likes': likes,
            'dislikes': dislikes,
            'comment_count': comment_count,
            'engagement_ratio': engagement_ratio,
            'like_dislike_ratio': like_dislike_ratio,
            'trending_date': trending_date,
            'publish_time': publish_time,
            'days_to_trend': days_to_trend,
            'country_code': country_code,
            'category_id': category_id,
            'channel_title': channel_title,
            'trending_day': trending_day,
            'tags': cleaned_tags
        })
    
    # Batch create videos and relationships
    success_count = 0
    for data in batch_data:
        try:
            # Create video node and all relationships in one transaction
            query = """
            MERGE (v:Video {video_unique_id: $video_unique_id})
            SET v.video_id = $video_id,
                v.title = $title,
                v.views = $views,
                v.likes = $likes,
                v.dislikes = $dislikes,
                v.comment_count = $comment_count,
                v.engagement_ratio = $engagement_ratio,
                v.like_dislike_ratio = $like_dislike_ratio,
                v.trending_date = $trending_date,
                v.publish_time = $publish_time,
                v.days_to_trend = $days_to_trend,
                v.country = $country_code
            WITH v
            MATCH (c:Category {category_id: $category_id})
            MERGE (v)-[:VIDEO_BELONGS_TO_CATEGORY]->(c)
            WITH v
            MATCH (ch:Channel {channel_title: $channel_title})
            MERGE (v)-[:VIDEO_PUBLISHED_BY_CHANNEL]->(ch)
            MERGE (ch)-[:CHANNEL_HAS_VIDEO]->(v)
            WITH v
            MATCH (co:Country {country_code: $country_code})
            MERGE (v)-[:VIDEO_TRENDING_IN_COUNTRY]->(co)
            """
            
            params = {
                'video_unique_id': data['video_unique_id'],
                'video_id': data['video_id'],
                'title': data['title'],
                'views': data['views'],
                'likes': data['likes'],
                'dislikes': data['dislikes'],
                'comment_count': data['comment_count'],
                'engagement_ratio': data['engagement_ratio'],
                'like_dislike_ratio': data['like_dislike_ratio'],
                'trending_date': data['trending_date'],
                'publish_time': data['publish_time'],
                'days_to_trend': data['days_to_trend'],
                'country_code': data['country_code'],
                'category_id': data['category_id'],
                'channel_title': data['channel_title']
            }
            
            graph.run(query, **params)
            
            # Add day relationship if available
            if data['trending_day'] and data['trending_day'] in day_nodes:
                graph.run("""
                    MATCH (v:Video {video_unique_id: $video_unique_id})
                    MATCH (d:Day {day_name: $day_name})
                    MERGE (v)-[:VIDEO_TRENDING_ON]->(d)
                """, video_unique_id=data['video_unique_id'], day_name=data['trending_day'])
            
            # Add tag relationships
            for tag_name in data['tags']:
                graph.run("""
                    MATCH (v:Video {video_unique_id: $video_unique_id})
                    MATCH (t:Tag {tag_name: $tag_name})
                    MERGE (v)-[:VIDEO_HAS_TAG]->(t)
                """, video_unique_id=data['video_unique_id'], tag_name=tag_name)
            
            success_count += 1
        except Exception as e:
            # Silently skip errors for individual videos to continue processing
            continue
    
    return success_count

# Process videos in batches
total_videos = len(df)
num_batches = (total_videos + BATCH_SIZE - 1) // BATCH_SIZE
videos_created = 0

print(f"Processing {total_videos:,} videos in {num_batches} batches of {BATCH_SIZE}...")

for batch_num in range(num_batches):
    start_idx = batch_num * BATCH_SIZE
    end_idx = min((batch_num + 1) * BATCH_SIZE, total_videos)
    batch_df = df.iloc[start_idx:end_idx]
    
    batch_created = create_video_batch(batch_df, graph, country_nodes, 
                                       category_nodes, channel_nodes, 
                                       tag_nodes, day_nodes)
    videos_created += batch_created
    
    progress = (batch_num + 1) / num_batches * 100
    batch_errors = len(batch_df) - batch_created
    print(f"  Batch {batch_num + 1}/{num_batches} ({progress:.1f}%): "
          f"Created {batch_created}/{len(batch_df)} videos")
    
    if batch_errors > 0:
        print(f"    ⚠️  {batch_errors} videos skipped due to errors")

print(f"\n✓ Created {videos_created:,} Video nodes")
errors = total_videos - videos_created
if errors > 0:
    print(f"⚠️  {errors} videos were not created (may be due to data issues)")

# ============================================================================
# STEP 11: Create Additional Relationships (Category -> Video)
# ============================================================================

print("\n[11] Creating Additional Relationships...")
print("-" * 80)

# CATEGORY_CONTAINS_VIDEO relationships are created implicitly through VIDEO_BELONGS_TO_CATEGORY
# But we can verify they exist
print("✓ Relationships created during video node creation")

# ============================================================================
# STEP 12: Data Validation
# ============================================================================

print("\n[12] Validating Data...")
print("-" * 80)

validation_results = {}

# Count nodes
node_counts = {
    'Video': graph.run("MATCH (v:Video) RETURN COUNT(v) as count").data()[0]['count'],
    'Channel': graph.run("MATCH (ch:Channel) RETURN COUNT(ch) as count").data()[0]['count'],
    'Category': graph.run("MATCH (c:Category) RETURN COUNT(c) as count").data()[0]['count'],
    'Country': graph.run("MATCH (co:Country) RETURN COUNT(co) as count").data()[0]['count'],
    'Tag': graph.run("MATCH (t:Tag) RETURN COUNT(t) as count").data()[0]['count'],
    'Day': graph.run("MATCH (d:Day) RETURN COUNT(d) as count").data()[0]['count'],
}

validation_results['node_counts'] = node_counts

print("\nNode Counts:")
for node_type, count in node_counts.items():
    print(f"  {node_type}: {count:,}")

# Count relationships
relationship_counts = {
    'VIDEO_BELONGS_TO_CATEGORY': graph.run("MATCH ()-[r:VIDEO_BELONGS_TO_CATEGORY]->() RETURN COUNT(r) as count").data()[0]['count'],
    'VIDEO_PUBLISHED_BY_CHANNEL': graph.run("MATCH ()-[r:VIDEO_PUBLISHED_BY_CHANNEL]->() RETURN COUNT(r) as count").data()[0]['count'],
    'VIDEO_TRENDING_IN_COUNTRY': graph.run("MATCH ()-[r:VIDEO_TRENDING_IN_COUNTRY]->() RETURN COUNT(r) as count").data()[0]['count'],
    'VIDEO_HAS_TAG': graph.run("MATCH ()-[r:VIDEO_HAS_TAG]->() RETURN COUNT(r) as count").data()[0]['count'],
    'VIDEO_TRENDING_ON': graph.run("MATCH ()-[r:VIDEO_TRENDING_ON]->() RETURN COUNT(r) as count").data()[0]['count'],
    'CHANNEL_HAS_VIDEO': graph.run("MATCH ()-[r:CHANNEL_HAS_VIDEO]->() RETURN COUNT(r) as count").data()[0]['count'],
}

validation_results['relationship_counts'] = relationship_counts

print("\nRelationship Counts:")
for rel_type, count in relationship_counts.items():
    print(f"  {rel_type}: {count:,}")

# Validate expected video count
expected_videos = len(df)
actual_videos = node_counts['Video']
if actual_videos == expected_videos:
    print(f"\n✓ Video count validation: Expected {expected_videos:,}, Got {actual_videos:,}")
    validation_results['video_count_match'] = True
else:
    print(f"\n⚠️  Video count mismatch: Expected {expected_videos:,}, Got {actual_videos:,}")
    validation_results['video_count_match'] = False

# Sample validation: Check 5 random videos per country
print("\n[13] Sampling Validation (5 videos per country)...")
print("-" * 80)

sample_results = {}
for country in ['US', 'GB', 'CA', 'IN']:
    country_df = df[df['country'] == country].sample(min(5, len(df[df['country'] == country])))
    country_samples = []
    
    for _, row in country_df.iterrows():
        video_id = str(row['video_id'])
        country_code = str(row['country'])
        video_unique_id = f"{video_id}_{country_code}"
        
        # Check if video exists
        video_check = graph.run(
            "MATCH (v:Video {video_unique_id: $video_unique_id}) RETURN v",
            video_unique_id=video_unique_id
        ).data()
        
        if len(video_check) > 0:
            # Check relationships
            rel_check = graph.run("""
                MATCH (v:Video {video_unique_id: $video_unique_id})
                OPTIONAL MATCH (v)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category)
                OPTIONAL MATCH (v)-[:VIDEO_PUBLISHED_BY_CHANNEL]->(ch:Channel)
                OPTIONAL MATCH (v)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
                OPTIONAL MATCH (v)-[:VIDEO_TRENDING_ON]->(d:Day)
                OPTIONAL MATCH (v)-[:VIDEO_HAS_TAG]->(t:Tag)
                RETURN 
                    v.video_id as video_id,
                    v.title as title,
                    c.category_name as category,
                    ch.channel_title as channel,
                    co.country_code as country,
                    d.day_name as day,
                    COUNT(DISTINCT t) as tag_count
            """, video_unique_id=video_unique_id).data()[0]
            
            country_samples.append({
                'video_id': rel_check['video_id'],
                'title': rel_check['title'][:50] if rel_check['title'] else '',
                'category': rel_check['category'],
                'channel': rel_check['channel'],
                'country': rel_check['country'],
                'day': rel_check['day'],
                'tag_count': rel_check['tag_count']
            })
        else:
            country_samples.append({
                'video_id': video_id,
                'status': 'NOT FOUND'
            })
    
    sample_results[country] = country_samples
    print(f"\n{country} Samples:")
    for sample in country_samples:
        if 'status' in sample:
            print(f"  ⚠️  {sample['video_id']}: {sample['status']}")
        else:
            print(f"  ✓ {sample['video_id']}: {sample['title']}")
            print(f"    Category: {sample['category']}, Channel: {sample['channel']}")
            print(f"    Country: {sample['country']}, Day: {sample['day']}, Tags: {sample['tag_count']}")

validation_results['sample_validation'] = sample_results

# Check for duplicate videos
print("\n[14] Checking for Duplicates...")
print("-" * 80)

duplicate_check = graph.run("""
    MATCH (v:Video)
    WITH v.video_id as video_id, v.country as country, COUNT(*) as count
    WHERE count > 1
    RETURN video_id, country, count
    ORDER BY count DESC
    LIMIT 10
""").data()

if len(duplicate_check) > 0:
    print(f"⚠️  Found {len(duplicate_check)} potential duplicate video entries:")
    for dup in duplicate_check:
        print(f"  Video ID: {dup['video_id']}, Country: {dup['country']}, Count: {dup['count']}")
    validation_results['duplicates_found'] = True
else:
    print("✓ No duplicates found (each video_id + country combination is unique)")
    validation_results['duplicates_found'] = False

# ============================================================================
# STEP 15: Save Ingestion Logs and Query Examples
# ============================================================================

print("\n[15] Saving Ingestion Logs and Query Examples...")
print("-" * 80)

# Save ingestion log
ingestion_log = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'node_counts': node_counts,
    'relationship_counts': relationship_counts,
    'validation': validation_results,
    'batch_size': BATCH_SIZE,
    'total_videos_processed': videos_created,
    'total_videos_expected': total_videos,
    'errors': errors,
    'success_rate': f"{(videos_created / total_videos * 100):.2f}%" if total_videos > 0 else "0%"
}

with open('phase4_ingestion_log.json', 'w', encoding='utf-8') as f:
    json.dump(ingestion_log, f, indent=2, default=str)

print("✓ Saved ingestion log to phase4_ingestion_log.json")

# Save query examples
query_examples = {
    'simple_queries': [
        {
            'name': 'Top Categories by Video Count',
            'query': 'MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category) RETURN c.category_name, COUNT(v) as video_count ORDER BY video_count DESC LIMIT 10'
        },
        {
            'name': 'Top Channels by Average Engagement',
            'query': 'MATCH (ch:Channel)-[:CHANNEL_HAS_VIDEO]->(v:Video) RETURN ch.channel_title, AVG(v.engagement_ratio) as avg_engagement ORDER BY avg_engagement DESC LIMIT 10'
        },
        {
            'name': 'Videos by Country',
            'query': 'MATCH (v:Video)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country) RETURN co.country_code, COUNT(v) as video_count ORDER BY video_count DESC'
        },
        {
            'name': 'Top Videos by Views',
            'query': 'MATCH (v:Video) RETURN v.video_id, v.title, v.views, v.country ORDER BY v.views DESC LIMIT 10'
        },
        {
            'name': 'Most Tagged Videos',
            'query': 'MATCH (v:Video)-[:VIDEO_HAS_TAG]->(t:Tag) RETURN v.video_id, v.title, COUNT(t) as tag_count ORDER BY tag_count DESC LIMIT 10'
        }
    ],
    'complex_queries': [
        {
            'name': 'Channels with High Engagement Videos',
            'query': '''
                MATCH (ch:Channel)-[:CHANNEL_HAS_VIDEO]->(v:Video)
                WHERE v.engagement_ratio > 0.1
                RETURN ch.channel_title, 
                       COUNT(v) as high_engagement_videos,
                       AVG(v.engagement_ratio) as avg_engagement,
                       AVG(v.views) as avg_views
                ORDER BY high_engagement_videos DESC
                LIMIT 10
            '''
        },
        {
            'name': 'Category Performance by Country',
            'query': '''
                MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category),
                      (v)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
                RETURN co.country_code, 
                       c.category_name,
                       COUNT(v) as video_count,
                       AVG(v.views) as avg_views,
                       AVG(v.engagement_ratio) as avg_engagement
                ORDER BY co.country_code, video_count DESC
            '''
        },
        {
            'name': 'Tag Co-occurrence with Categories',
            'query': '''
                MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category),
                      (v)-[:VIDEO_HAS_TAG]->(t:Tag)
                WITH c.category_name as category, t.tag_name as tag, COUNT(v) as co_count
                WHERE co_count > 10
                RETURN category, tag, co_count
                ORDER BY category, co_count DESC
                LIMIT 50
            '''
        },
        {
            'name': 'Day-of-Week Trending Patterns',
            'query': '''
                MATCH (v:Video)-[:VIDEO_TRENDING_ON]->(d:Day)
                RETURN d.day_name, 
                       COUNT(v) as video_count,
                       AVG(v.views) as avg_views,
                       AVG(v.engagement_ratio) as avg_engagement
                ORDER BY video_count DESC
            '''
        },
        {
            'name': 'Cross-Country Video Analysis',
            'query': '''
                MATCH (v:Video)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
                WITH v.video_id as video_id, COLLECT(co.country_code) as countries
                WHERE SIZE(countries) > 1
                RETURN video_id, countries, SIZE(countries) as country_count
                ORDER BY country_count DESC
                LIMIT 20
            '''
        }
    ]
}

with open('phase4_query_examples.json', 'w', encoding='utf-8') as f:
    json.dump(query_examples, f, indent=2)

print("✓ Saved query examples to phase4_query_examples.json")

# Create a readable query examples file
with open('phase4_query_examples.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("PHASE 4: NEO4J QUERY EXAMPLES\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("SIMPLE QUERIES\n")
    f.write("-" * 80 + "\n\n")
    for i, query_info in enumerate(query_examples['simple_queries'], 1):
        f.write(f"{i}. {query_info['name']}\n")
        f.write(f"Query:\n{query_info['query']}\n\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("COMPLEX QUERIES\n")
    f.write("-" * 80 + "\n\n")
    for i, query_info in enumerate(query_examples['complex_queries'], 1):
        f.write(f"{i}. {query_info['name']}\n")
        f.write(f"Query:\n{query_info['query']}\n\n")

print("✓ Saved query examples to phase4_query_examples.txt")

# ============================================================================
# STEP 16: Generate Summary Report
# ============================================================================

print("\n[16] Generating Summary Report...")
print("-" * 80)

report = f"""
# Phase 4: Graph Database Setup and Data Ingestion Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. Database Setup

- **Database**: Neo4j
- **URI**: {NEO4J_URI}
- **User**: {NEO4J_USER}
- **Connection Status**: ✓ Connected

---

## 2. Graph Schema

### Nodes Created

- **Video**: {node_counts['Video']:,} nodes
  - Properties: video_id, title, views, likes, dislikes, comment_count, engagement_ratio, like_dislike_ratio, trending_date, publish_time, days_to_trend
  
- **Channel**: {node_counts['Channel']:,} nodes
  - Properties: channel_title, total_views, avg_engagement_ratio, video_count
  
- **Category**: {node_counts['Category']} nodes
  - Properties: category_id, category_name
  
- **Country**: {node_counts['Country']} nodes
  - Properties: country_code, country_name
  
- **Tag**: {node_counts['Tag']:,} nodes
  - Properties: tag_name
  
- **Day**: {node_counts['Day']} nodes
  - Properties: day_name

### Relationships Created

- **VIDEO_BELONGS_TO_CATEGORY**: {relationship_counts['VIDEO_BELONGS_TO_CATEGORY']:,}
- **VIDEO_PUBLISHED_BY_CHANNEL**: {relationship_counts['VIDEO_PUBLISHED_BY_CHANNEL']:,}
- **VIDEO_TRENDING_IN_COUNTRY**: {relationship_counts['VIDEO_TRENDING_IN_COUNTRY']:,}
- **VIDEO_HAS_TAG**: {relationship_counts['VIDEO_HAS_TAG']:,}
- **VIDEO_TRENDING_ON**: {relationship_counts['VIDEO_TRENDING_ON']:,}
- **CHANNEL_HAS_VIDEO**: {relationship_counts['CHANNEL_HAS_VIDEO']:,}

---

## 3. Indexes Created

- Video: video_id, trending_date, views, engagement_ratio
- Channel: channel_title, total_views
- Category: category_name
- Country: country_code
- Tag: tag_name
- Day: day_name

---

## 4. Data Validation

### Node Counts
{chr(10).join([f"- {node_type}: {count:,}" for node_type, count in node_counts.items()])}

### Relationship Counts
{chr(10).join([f"- {rel_type}: {count:,}" for rel_type, count in relationship_counts.items()])}

### Video Count Validation
- Expected: {expected_videos:,}
- Actual: {actual_videos:,}
- Status: {'✓ PASSED' if validation_results['video_count_match'] else '✗ FAILED'}

### Duplicate Check
- Status: {'⚠️ Duplicates Found' if validation_results['duplicates_found'] else '✓ No Duplicates'}

---

## 5. Ingestion Statistics

- **Total Videos Processed**: {videos_created:,}
- **Batch Size**: {BATCH_SIZE}
- **Errors**: {errors}
- **Success Rate**: {(videos_created / total_videos * 100):.2f}%

---

## 6. Sample Validation Results

"""

for country, samples in sample_results.items():
    report += f"\n### {country}\n\n"
    for sample in samples:
        if 'status' in sample:
            report += f"- ⚠️ {sample['video_id']}: {sample['status']}\n"
        else:
            report += f"- ✓ {sample['video_id']}: {sample['title']}\n"
            report += f"  - Category: {sample['category']}\n"
            report += f"  - Channel: {sample['channel']}\n"
            report += f"  - Country: {sample['country']}\n"
            report += f"  - Day: {sample['day']}\n"
            report += f"  - Tags: {sample['tag_count']}\n"

report += f"""

---

## 7. Query Examples

See `phase4_query_examples.txt` for detailed query examples.

### Simple Queries
{chr(10).join([f"- {q['name']}" for q in query_examples['simple_queries']])}

### Complex Queries
{chr(10).join([f"- {q['name']}" for q in query_examples['complex_queries']])}

---

## 8. Next Steps

1. Test queries using Neo4j Browser or Cypher shell
2. Proceed to Phase 5: Query Execution and Visualization
3. Analyze graph patterns and relationships
4. Create custom queries based on analysis needs

---

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

with open('phase4_ingestion_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✓ Saved ingestion report to phase4_ingestion_report.md")

# ============================================================================
# STEP 17: Test Queries
# ============================================================================

print("\n[17] Testing Sample Queries...")
print("-" * 80)

# Test query 1: Top categories
print("\nTest Query 1: Top Categories by Video Count")
try:
    result = graph.run("""
        MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category)
        RETURN c.category_name, COUNT(v) as video_count
        ORDER BY video_count DESC
        LIMIT 5
    """).data()
    for row in result:
        print(f"  {row['category_name']}: {row['video_count']:,} videos")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# Test query 2: Top channels by engagement
print("\nTest Query 2: Top Channels by Average Engagement")
try:
    result = graph.run("""
        MATCH (ch:Channel)-[:CHANNEL_HAS_VIDEO]->(v:Video)
        RETURN ch.channel_title, AVG(v.engagement_ratio) as avg_engagement
        ORDER BY avg_engagement DESC
        LIMIT 5
    """).data()
    for row in result:
        print(f"  {row['channel_title']}: {row['avg_engagement']:.4f}")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print("\n" + "=" * 80)
print("PHASE 4 COMPLETED SUCCESSFULLY!")
print("=" * 80)
print(f"\nSummary:")
print(f"  - Nodes Created: {sum(node_counts.values()):,}")
print(f"  - Relationships Created: {sum(relationship_counts.values()):,}")
print(f"  - Videos Processed: {videos_created:,}")
print(f"\nOutput Files:")
print(f"  1. phase4_ingestion_log.json")
print(f"  2. phase4_ingestion_report.md")
print(f"  3. phase4_query_examples.json")
print(f"  4. phase4_query_examples.txt")
print(f"  5. phase4_graph_ingestion.py (this script)")

print("\n" + "=" * 80)
print("NEXT STEPS:")
print("=" * 80)
print("1. Verify database connection and data in Neo4j Browser")
print("2. Test queries from phase4_query_examples.txt")
print("3. Proceed to Phase 5: Query Execution and Visualization")

