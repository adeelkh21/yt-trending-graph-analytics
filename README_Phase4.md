# Phase 4: Graph Database Setup and Data Ingestion

## Overview
This phase sets up a Neo4j graph database and ingests the cleaned YouTube Trending Videos dataset.

## Prerequisites
- Phase 2 and Phase 3 completed
- `youtube_trending_cleaned.csv` must be present
- Neo4j installed and running

## Neo4j Installation and Setup

### Option 0: Neo4j Aura (Cloud - Already Configured! ✅)

**Your Neo4j Aura instance is already configured in the scripts!**

1. **Wait 60 seconds** after instance creation (or verify at https://console.neo4j.io)
2. **Connection Details** (already set in scripts):
   - URI: `neo4j+s://bc0353c7.databases.neo4j.io`
   - Username: `neo4j`
   - Database: `neo4j`
   - Instance: Free instance (bc0353c7)

3. **Test Connection**:
   ```bash
   python test_neo4j_connection.py
   ```

4. **Run Phase 4**:
   ```bash
   python phase4_graph_ingestion.py
   ```


### Option 1: Neo4j Desktop (Local Installation - Alternative)

1. **Download Neo4j Desktop**
   - Visit: https://neo4j.com/download/
   - Download Neo4j Desktop for your operating system
   - Install and launch Neo4j Desktop

2. **Create a New Project**
   - Click "New Project"
   - Name it "YouTube Trending"

3. **Create a New Database**
   - Click "Add Database" → "Create a Local Database"
   - Name: `youtube_trending_graph`
   - Password: Set a password (remember this!)
   - Version: Use the latest stable version

4. **Start the Database**
   - Click "Start" on your database
   - Wait for it to start (green status)

5. **Get Connection Details**
   - Click "Open" to open Neo4j Browser
   - Note the connection URI (usually `bolt://localhost:7687`)
   - Default username: `neo4j`
   - Password: The one you set during database creation

### Option 2: Neo4j Community Edition (Linux/Advanced)

1. **Install Neo4j**
   ```bash
   # Ubuntu/Debian
   wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
   echo 'deb https://debian.neo4j.com stable 5' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
   sudo apt-get update
   sudo apt-get install neo4j

   # Start Neo4j
   sudo systemctl start neo4j
   ```

2. **Configure Neo4j**
   - Edit `/etc/neo4j/neo4j.conf`
   - Set `dbms.default_database=youtube_trending_graph`
   - Set `dbms.security.auth_enabled=true`
   - Set password: `neo4j-admin set-initial-password yourpassword`

3. **Start Neo4j**
   ```bash
   sudo systemctl start neo4j
   sudo systemctl enable neo4j
   ```


## Configuration

### Connection Settings

**✅ Already Configured for Neo4j Aura!**

The scripts are pre-configured with your Neo4j Aura credentials:
- URI: `neo4j+s://bc0353c7.databases.neo4j.io`
- Username: `neo4j`
- Database: `neo4j`

**If using a local Neo4j instance instead**, update the connection settings in `phase4_graph_ingestion.py`:

```python
NEO4J_URI = "bolt://localhost:7687"  # Change if different
NEO4J_USER = "neo4j"                  # Change if different
NEO4J_PASSWORD = "your_password"      # Change to your password
```

## Setup Instructions

### 1. Verify Neo4j Connection
```bash
# Test connection (optional)
python -c "from py2neo import Graph; g = Graph('bolt://localhost:7687', auth=('neo4j', 'password')); print('Connected!' if g else 'Failed')"
```

### 2. Run Phase 4 Ingestion
```bash
python phase4_graph_ingestion.py
```

## What Phase 4 Does

### 1. Database Setup
- Connects to Neo4j database
- Validates connection
- Clears existing data (optional)

### 2. Graph Schema Design
Creates the following nodes:
- **Video**: Video properties (views, likes, engagement, etc.)
- **Channel**: Channel properties (total views, avg engagement, etc.)
- **Category**: Category properties (category_id, category_name)
- **Country**: Country properties (country_code, country_name)
- **Tag**: Tag properties (tag_name)
- **Day**: Day-of-week properties (day_name)

Creates the following relationships:
- **VIDEO_BELONGS_TO_CATEGORY**: Video → Category
- **VIDEO_PUBLISHED_BY_CHANNEL**: Video → Channel
- **VIDEO_TRENDING_IN_COUNTRY**: Video → Country
- **VIDEO_HAS_TAG**: Video → Tag (for each tag)
- **VIDEO_TRENDING_ON**: Video → Day
- **CHANNEL_HAS_VIDEO**: Channel → Video

### 3. Node Creation
- Creates nodes in order: Country → Category → Channel → Tag → Day → Video
- Uses batch processing (1,000 rows per batch)
- Creates relationships for each video

### 4. Indexing
Creates indexes on:
- Video: video_id, trending_date, views, engagement_ratio
- Channel: channel_title, total_views
- Category: category_name
- Country: country_code
- Tag: tag_name
- Day: day_name

### 5. Data Validation
- Verifies node counts
- Verifies relationship counts
- Validates video count matches expected
- Checks for duplicates
- Samples random videos per country

### 6. Output & Reporting
- Saves ingestion logs (JSON)
- Saves query examples (JSON and TXT)
- Generates ingestion report (Markdown)

## Expected Output Files

1. **phase4_ingestion_log.json** - Detailed ingestion logs
2. **phase4_ingestion_report.md** - Comprehensive ingestion report
3. **phase4_query_examples.json** - Query examples (JSON format)
4. **phase4_query_examples.txt** - Query examples (readable format)
5. **phase4_graph_ingestion.py** - Ingestion script

## Expected Results

- **Video Nodes**: ~50,357 nodes
- **Channel Nodes**: ~8,000+ nodes
- **Category Nodes**: ~18 nodes
- **Country Nodes**: 4 nodes
- **Tag Nodes**: Thousands of unique tags
- **Day Nodes**: 7 nodes
- **Relationships**: Millions of relationships

## Troubleshooting

### Common Issues

1. **Connection Error**
   - Ensure Neo4j is running
   - Check URI, username, and password
   - Verify firewall settings

2. **Memory Issues**
   - Reduce BATCH_SIZE in script (default: 1000)
   - Increase Neo4j heap size in neo4j.conf
   - Process data in smaller chunks

3. **Slow Performance**
   - Ensure indexes are created
   - Increase Neo4j memory settings
   - Use batch processing (already implemented)

4. **Duplicate Nodes**
   - Script uses merge operations to prevent duplicates
   - Check video_unique_id (video_id + country) for uniqueness

5. **Missing Relationships**
   - Check data quality in cleaned dataset
   - Verify tags_list parsing
   - Check for null values

### Performance Optimization

1. **Increase Neo4j Memory**
   - Edit `neo4j.conf`
   - Set `dbms.memory.heap.initial_size=2g`
   - Set `dbms.memory.heap.max_size=4g`

2. **Batch Size Tuning**
   - Smaller batches (500): More memory efficient
   - Larger batches (2000): Faster but more memory intensive

3. **Index Creation**
   - Indexes are created before data ingestion
   - This ensures fast query performance

## Verification

### Check Database in Neo4j Browser

1. Open Neo4j Browser (usually at http://localhost:7474)
2. Run test queries:
   ```cypher
   MATCH (v:Video) RETURN COUNT(v) as video_count
   MATCH (ch:Channel) RETURN COUNT(ch) as channel_count
   MATCH ()-[r]->() RETURN COUNT(r) as relationship_count
   ```

### Sample Queries

See `phase4_query_examples.txt` for detailed query examples.

## Notes

- The script processes data in batches for memory efficiency
- Each video creates multiple relationships (category, channel, country, tags, day)
- Video nodes are uniquely identified by video_id + country
- All relationships are bidirectional where appropriate
- Indexes are created before data ingestion for performance