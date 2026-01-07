
# Phase 4: Graph Database Setup and Data Ingestion Report

## Generated: 2025-11-09 22:55:49

---

## 1. Database Setup

- **Database**: Neo4j
- **URI**: bolt://127.0.0.1:7687
- **User**: neo4j
- **Connection Status**: ✓ Connected

---

## 2. Graph Schema

### Nodes Created

- **Video**: 50,357 nodes
  - Properties: video_id, title, views, likes, dislikes, comment_count, engagement_ratio, like_dislike_ratio, trending_date, publish_time, days_to_trend
  
- **Channel**: 8,053 nodes
  - Properties: channel_title, total_views, avg_engagement_ratio, video_count
  
- **Category**: 17 nodes
  - Properties: category_id, category_name
  
- **Country**: 4 nodes
  - Properties: country_code, country_name
  
- **Tag**: 268,050 nodes
  - Properties: tag_name
  
- **Day**: 7 nodes
  - Properties: day_name

### Relationships Created

- **VIDEO_BELONGS_TO_CATEGORY**: 50,357
- **VIDEO_PUBLISHED_BY_CHANNEL**: 50,357
- **VIDEO_TRENDING_IN_COUNTRY**: 50,357
- **VIDEO_HAS_TAG**: 963,063
- **VIDEO_TRENDING_ON**: 50,357
- **CHANNEL_HAS_VIDEO**: 50,357

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
- Video: 50,357
- Channel: 8,053
- Category: 17
- Country: 4
- Tag: 268,050
- Day: 7

### Relationship Counts
- VIDEO_BELONGS_TO_CATEGORY: 50,357
- VIDEO_PUBLISHED_BY_CHANNEL: 50,357
- VIDEO_TRENDING_IN_COUNTRY: 50,357
- VIDEO_HAS_TAG: 963,063
- VIDEO_TRENDING_ON: 50,357
- CHANNEL_HAS_VIDEO: 50,357

### Video Count Validation
- Expected: 50,357
- Actual: 50,357
- Status: ✓ PASSED

### Duplicate Check
- Status: ✓ No Duplicates

---

## 5. Ingestion Statistics

- **Total Videos Processed**: 50,357
- **Batch Size**: 1000
- **Errors**: 0
- **Success Rate**: 100.00%

---

## 6. Sample Validation Results


### US

- ✓ i04pYZGDHIc: How To Make a CHINESE FRIED RICE TAKEOUT CAKE and 
  - Category: Howto & Style
  - Channel: How To Cake It
  - Country: US
  - Day: Wednesday
  - Tags: 31
- ✓ btE8mDfEF34: Stephen A. on Cavaliers' NBA Finals Game 4: 'It wa
  - Category: Sports
  - Channel: ESPN
  - Country: US
  - Day: Monday
  - Tags: 27
- ✓ 8XBLuU_4Qgo: John Cena On His Split From Nikki Bella: ‘I Had My
  - Category: News & Politics
  - Channel: TODAY
  - Country: US
  - Day: Monday
  - Tags: 26
- ✓ ACHZrvF6mTA: Aubrey Plaza and Dan Stevens Hijack a Stranger's T
  - Category: Entertainment
  - Channel: Vanity Fair
  - Country: US
  - Day: Saturday
  - Tags: 24
- ✓ xe5tXZs-iWw: Pressing Non-Newtonian Fluid Through Small Holes w
  - Category: Science & Technology
  - Channel: Hydraulic Press Channel
  - Country: US
  - Day: Tuesday
  - Tags: 36

### GB

- ✓ QFfEtKvXMAs: Niall Horan - Too Much To Ask (Acoustic)
  - Category: Music
  - Channel: NiallHoranVEVO
  - Country: GB
  - Day: Thursday
  - Tags: 15
- ✓ icyhX6PjKjM: Calvin Harris, Dua Lipa - One Kiss (Behind the Sce
  - Category: Music
  - Channel: CalvinHarrisVEVO
  - Country: GB
  - Day: Sunday
  - Tags: 17
- ✓ 6EHbZKLkeMg: Laura Govan Addresses Rumors Of Pregnancy & Affair
  - Category: Entertainment
  - Channel: Breakfast Club Power 105.1 FM
  - Country: GB
  - Day: Friday
  - Tags: 12
- ✓ IUmdcd_8Vwc: Clear Lemon Meringue Pie
  - Category: Howto & Style
  - Channel: My Virgin Kitchen
  - Country: GB
  - Day: Wednesday
  - Tags: 33
- ✓ T4FAg5A4wQk: Ariana Grande - No Tears Left To Cry (BTS - Part 1
  - Category: Music
  - Channel: Ariana Grande`
  - Country: GB
  - Day: Tuesday
  - Tags: 6

### CA

- ✓ F4wFZgjdCyw: 2018 CPU Nationals: Thursday (Session 3, Platform 
  - Category: Sports
  - Channel: MyStrengthBook
  - Country: CA
  - Day: Friday
  - Tags: 0
- ✓ qgcenfc6Qbc: Superhero Movies (2017) - IHE
  - Category: Comedy
  - Channel: I Hate Everything
  - Country: CA
  - Day: Sunday
  - Tags: 7
- ✓ jhylspIBy8E: Is Something About To Happen?
  - Category: Science & Technology
  - Channel: secureteam10
  - Country: CA
  - Day: Sunday
  - Tags: 20
- ✓ 2Nlo2ekTRvI: Everything Wrong With Cars 3 In 14 Minutes Or Less
  - Category: Film & Animation
  - Channel: CinemaSins
  - Country: CA
  - Day: Saturday
  - Tags: 10
- ✓ PgqHq6WjD8s: Here’s a Tour of a Perfect 1990 Mitsubishi Eclipse
  - Category: Autos & Vehicles
  - Channel: Doug DeMuro
  - Country: CA
  - Day: Thursday
  - Tags: 16

### IN

- ✓ EzPoyn0hHlk: Impatient Aashiq (2018) Telugu Film Dubbed Into Hi
  - Category: Film & Animation
  - Channel: Goldmines Premiere
  - Country: IN
  - Day: Tuesday
  - Tags: 13
- ✓ yeRAwhtyD3g: Aa Gattununtaava Full Video Song - Rangasthalam Vi
  - Category: Music
  - Channel: Lahari Music | T-Series
  - Country: IN
  - Day: Thursday
  - Tags: 20
- ✓ 4q8PPFep6MA: Your Favorite Character | Jethalal Writes Shayari 
  - Category: Entertainment
  - Channel: Sony PAL
  - Country: IN
  - Day: Friday
  - Tags: 25
- ✓ suURKEjmV94: Komal Prajapati | MERA KYA THA KUSHUR | New Bewafa
  - Category: Music
  - Channel: Studio Saraswati Official
  - Country: IN
  - Day: Sunday
  - Tags: 23
- ✓ 8TA464uwEi4: Veer Bhagat Singh|Kumar V|Arijit S,Sonu N,Mika,Pal
  - Category: Music
  - Channel: Zee Music Company
  - Country: IN
  - Day: Tuesday
  - Tags: 22


---

## 7. Query Examples

See `phase4_query_examples.txt` for detailed query examples.

### Simple Queries
- Top Categories by Video Count
- Top Channels by Average Engagement
- Videos by Country
- Top Videos by Views
- Most Tagged Videos

### Complex Queries
- Channels with High Engagement Videos
- Category Performance by Country
- Tag Co-occurrence with Categories
- Day-of-Week Trending Patterns
- Cross-Country Video Analysis

---

## 8. Next Steps

1. Test queries using Neo4j Browser or Cypher shell
2. Proceed to Phase 5: Query Execution and Visualization
3. Analyze graph patterns and relationships
4. Create custom queries based on analysis needs

---

**Report Generated**: 2025-11-09 22:55:49
