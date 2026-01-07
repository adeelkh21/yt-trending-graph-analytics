# Phase 4: Graph Database Setup and Data Ingestion - Summary

## ✅ Phase 4 Script Created Successfully!

**Date**: November 9, 2025  
**Script**: `phase4_graph_ingestion.py`  
**Test Script**: `test_neo4j_connection.py`

---

## 📋 Overview

Phase 4 sets up a Neo4j graph database and ingests the cleaned YouTube Trending Videos dataset into a graph structure with nodes and relationships.

---

## 🗄️ Graph Schema Design

### Nodes Created

1. **Video** (~50,357 nodes)
   - Properties: video_id, video_unique_id, title, views, likes, dislikes, comment_count, engagement_ratio, like_dislike_ratio, trending_date, publish_time, days_to_trend, country

2. **Channel** (~8,000+ nodes)
   - Properties: channel_title, total_views, avg_engagement_ratio, video_count

3. **Category** (~18 nodes)
   - Properties: category_id, category_name

4. **Country** (4 nodes)
   - Properties: country_code, country_name

5. **Tag** (Thousands of nodes)
   - Properties: tag_name

6. **Day** (7 nodes)
   - Properties: day_name (Monday-Sunday)

### Relationships Created

1. **VIDEO_BELONGS_TO_CATEGORY**: Video → Category
2. **VIDEO_PUBLISHED_BY_CHANNEL**: Video → Channel
3. **VIDEO_TRENDING_IN_COUNTRY**: Video → Country
4. **VIDEO_HAS_TAG**: Video → Tag (for each tag in tags_list)
5. **VIDEO_TRENDING_ON**: Video → Day
6. **CHANNEL_HAS_VIDEO**: Channel → Video (bidirectional)

---

## 🔧 Setup Instructions

### 1. Install Neo4j

See `README_Phase4.md` for detailed installation instructions.

**Quick Setup (Neo4j Desktop)**:
1. Download Neo4j Desktop from https://neo4j.com/download/
2. Create a new project: "YouTube Trending"
3. Create a new database: `youtube_trending_graph`
4. Set password (remember this!)
5. Start the database

### 2. Configure Connection

Edit `phase4_graph_ingestion.py` and update:
```python
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"  # Change this!
```

### 3. Test Connection

```bash
python test_neo4j_connection.py
```

### 4. Run Ingestion

```bash
python phase4_graph_ingestion.py
```

---

## 📊 Features

### 1. Database Setup
- ✅ Connects to Neo4j database
- ✅ Validates connection
- ✅ Clears existing data (optional)

### 2. Index Creation
- ✅ Creates indexes on all key properties
- ✅ Indexes created before data ingestion
- ✅ Optimizes query performance

### 3. Batch Processing
- ✅ Processes videos in batches (1,000 per batch)
- ✅ Memory-efficient processing
- ✅ Progress tracking

### 4. Data Validation
- ✅ Verifies node counts
- ✅ Verifies relationship counts
- ✅ Validates video count matches expected
- ✅ Checks for duplicates
- ✅ Samples random videos per country

### 5. Error Handling
- ✅ Handles data quality issues gracefully
- ✅ Continues processing on individual video errors
- ✅ Logs errors for review

### 6. Output & Reporting
- ✅ Saves ingestion logs (JSON)
- ✅ Saves query examples (JSON and TXT)
- ✅ Generates ingestion report (Markdown)
- ✅ Test queries for validation

---

## 📁 Generated Files

### 1. Scripts
- **phase4_graph_ingestion.py** - Main ingestion script
- **test_neo4j_connection.py** - Connection test script

### 2. Output Files (Generated after running)
- **phase4_ingestion_log.json** - Detailed ingestion logs
- **phase4_ingestion_report.md** - Comprehensive ingestion report
- **phase4_query_examples.json** - Query examples (JSON format)
- **phase4_query_examples.txt** - Query examples (readable format)

### 3. Documentation
- **README_Phase4.md** - Setup and usage instructions
- **PHASE4_SUMMARY.md** - This summary document

---

## 🔍 Query Examples

### Simple Queries

1. **Top Categories by Video Count**
```cypher
MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category)
RETURN c.category_name, COUNT(v) as video_count
ORDER BY video_count DESC
LIMIT 10
```

2. **Top Channels by Average Engagement**
```cypher
MATCH (ch:Channel)-[:CHANNEL_HAS_VIDEO]->(v:Video)
RETURN ch.channel_title, AVG(v.engagement_ratio) as avg_engagement
ORDER BY avg_engagement DESC
LIMIT 10
```

3. **Videos by Country**
```cypher
MATCH (v:Video)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
RETURN co.country_code, COUNT(v) as video_count
ORDER BY video_count DESC
```

### Complex Queries

1. **Channels with High Engagement Videos**
```cypher
MATCH (ch:Channel)-[:CHANNEL_HAS_VIDEO]->(v:Video)
WHERE v.engagement_ratio > 0.1
RETURN ch.channel_title, 
       COUNT(v) as high_engagement_videos,
       AVG(v.engagement_ratio) as avg_engagement,
       AVG(v.views) as avg_views
ORDER BY high_engagement_videos DESC
LIMIT 10
```

2. **Category Performance by Country**
```cypher
MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category),
      (v)-[:VIDEO_TRENDING_IN_COUNTRY]->(co:Country)
RETURN co.country_code, 
       c.category_name,
       COUNT(v) as video_count,
       AVG(v.views) as avg_views,
       AVG(v.engagement_ratio) as avg_engagement
ORDER BY co.country_code, video_count DESC
```

3. **Tag Co-occurrence with Categories**
```cypher
MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category),
      (v)-[:VIDEO_HAS_TAG]->(t:Tag)
WITH c.category_name as category, t.tag_name as tag, COUNT(v) as co_count
WHERE co_count > 10
RETURN category, tag, co_count
ORDER BY category, co_count DESC
LIMIT 50
```

See `phase4_query_examples.txt` for more examples.

---

## ⚙️ Performance Optimization

### Batch Processing
- Processes 1,000 videos per batch
- Reduces memory usage
- Improves performance

### Indexing
- Indexes created on all key properties
- Faster query execution
- Optimized relationship traversal

### Cypher Queries
- Uses parameterized queries
- Prevents SQL injection
- Optimizes query execution

---

## 🔍 Validation

### Node Counts
- Video: ~50,357 nodes
- Channel: ~8,000+ nodes
- Category: ~18 nodes
- Country: 4 nodes
- Tag: Thousands of nodes
- Day: 7 nodes

### Relationship Counts
- VIDEO_BELONGS_TO_CATEGORY: ~50,357
- VIDEO_PUBLISHED_BY_CHANNEL: ~50,357
- VIDEO_TRENDING_IN_COUNTRY: ~50,357
- VIDEO_HAS_TAG: ~500,000+ (varies by tags)
- VIDEO_TRENDING_ON: ~50,357
- CHANNEL_HAS_VIDEO: ~50,357

### Sample Validation
- Randomly samples 5 videos per country
- Verifies all properties exist
- Verifies all relationships exist
- Checks tag counts

---

## 🚨 Troubleshooting

### Common Issues

1. **Connection Error**
   - Ensure Neo4j is running
   - Check URI, username, and password
   - Verify firewall settings

2. **Memory Issues**
   - Reduce BATCH_SIZE (default: 1000)
   - Increase Neo4j heap size
   - Process data in smaller chunks

3. **Slow Performance**
   - Ensure indexes are created
   - Increase Neo4j memory settings
   - Use batch processing (already implemented)

4. **Duplicate Nodes**
   - Script uses merge operations
   - Check video_unique_id (video_id + country)

5. **Missing Relationships**
   - Check data quality in cleaned dataset
   - Verify tags_list parsing
   - Check for null values

---

## ✅ Next Steps

After completing Phase 4, proceed to:

1. **Verify Database**
   - Open Neo4j Browser (http://localhost:7474)
   - Run test queries
   - Verify node and relationship counts

2. **Phase 5: Query Execution and Visualization**
   - Execute simple queries (5 queries)
   - Execute complex queries (5 queries)
   - Visualize query results
   - Create statistical analysis

3. **Custom Analysis**
   - Create custom queries
   - Analyze graph patterns
   - Explore relationships

---

## 📈 Expected Results

### After Running Phase 4

- ✅ Fully populated graph database
- ✅ All nodes created with properties
- ✅ All relationships established
- ✅ Indexes created for performance
- ✅ Data validated and verified
- ✅ Ready for Phase 5 queries

### Performance Metrics

- **Processing Time**: ~10-30 minutes (depending on system)
- **Memory Usage**: ~2-4GB (depending on batch size)
- **Success Rate**: >99% (handles data quality issues)

---

## 📝 Notes

- The script processes data in batches for memory efficiency
- Each video creates multiple relationships (category, channel, country, tags, day)
- Video nodes are uniquely identified by video_id + country
- All relationships are bidirectional where appropriate
- Indexes are created before data ingestion for performance
- Error handling ensures processing continues on individual video errors

---

**Phase 4 Status**: ✅ **SCRIPT READY**  
**Next Step**: Install Neo4j and run the ingestion script  
**Generated**: November 9, 2025

