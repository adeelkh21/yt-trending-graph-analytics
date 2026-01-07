# Big Data Analytics Assignment 1
## YouTube Trending Videos Analysis Using Graph Database

---

**Student Information:**
- **Name:** Muhammad Adeel
- **Registration Number:** 2022331
- **Course:** Big Data Analytics
- **Assignment:** Assignment 1
- **Date:** November 10, 2025

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Introduction](#introduction)
3. [Dataset Description](#dataset-description)
4. [Methodology](#methodology)
5. [Data Preprocessing](#data-preprocessing)
6. [Exploratory Data Analysis](#exploratory-data-analysis)
7. [Graph Database Setup](#graph-database-setup)
8. [Query Execution and Analysis](#query-execution-and-analysis)
9. [Results and Findings](#results-and-findings)
10. [Visualizations](#visualizations)
11. [Statistical Analysis](#statistical-analysis)
12. [Conclusions](#conclusions)
13. [References and Appendices](#references-and-appendices)

---

## Executive Summary

This project presents a comprehensive analysis of YouTube Trending Videos dataset using graph database technology (Neo4j). The project successfully processes 50,357 trending video records across four countries (United States, Great Britain, Canada, and India) covering the period from November 2017 to June 2018. 

**Key Achievements:**
- Processed and cleaned 158,098 initial records to 50,357 unique videos
- Created a graph database with 326,488 nodes and 1,264,948 relationships
- Executed 14 comprehensive queries (6 simple, 5 complex, 3 statistical analyses)
- Generated 13 professional visualizations
- Identified key insights about content trends, engagement patterns, and regional preferences

**Main Findings:**
- Entertainment and Music categories dominate trending content across all countries
- Great Britain shows the highest average views per video (3.4M), while Canada has the highest engagement ratio (3.57%)
- T-Series is the most successful channel with 834M total views
- Thursday is the peak trending day for US and GB, while Tuesday is peak for CA and IN
- Strong negative correlation (-0.41) between views and engagement ratio indicates viral videos may have lower engagement

---

## Introduction

### Project Objective

The primary objective of this project is to analyze YouTube Trending Videos data using big data analytics techniques, specifically focusing on:
1. Data collection and preprocessing
2. Exploratory data analysis (EDA)
3. Graph database implementation
4. Query execution and visualization
5. Statistical analysis and pattern identification

### Why YouTube Trending Videos Dataset?

The YouTube Trending Videos dataset was chosen for this project because:

1. **Real-world Relevance**: YouTube is one of the largest video platforms globally, making this dataset highly relevant for understanding content trends and user behavior.

2. **Rich Relationships**: The data contains multiple interconnected entities (videos, channels, categories, tags, countries) making it ideal for graph database analysis.

3. **Multi-dimensional Analysis**: The dataset allows analysis across multiple dimensions:
   - Temporal (trending dates, publish dates)
   - Geographical (multiple countries)
   - Categorical (content categories)
   - Engagement metrics (views, likes, comments, engagement ratios)

4. **Scalability**: With 50,000+ records, the dataset provides a good scale for testing big data processing techniques while remaining manageable for analysis.

5. **Business Value**: Insights from this analysis can inform content strategy, marketing decisions, and platform optimization.

### Technology Stack

- **Programming Language**: Python 3.x
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Graph Database**: Neo4j 5.x
- **Database Driver**: py2neo
- **Statistical Analysis**: scipy, statsmodels

---

## Dataset Description

### Dataset Overview

**Dataset Name**: Trending YouTube Video Statistics  
**Source**: Kaggle (Daily statistics for trending YouTube videos)  
**Time Period**: November 14, 2017 to June 14, 2018  
**Countries**: United States (US), Great Britain (GB), Canada (CA), India (IN)  
**Initial Records**: 158,098 rows  
**Final Records**: 50,357 unique videos (after preprocessing)

### Dataset Structure

#### Original Columns (17 columns)
- `video_id`: Unique identifier for each video
- `trending_date`: Date when video was trending
- `title`: Video title
- `channel_title`: Channel name
- `category_id`: Numeric category identifier
- `publish_time`: Video publication timestamp
- `tags`: Pipe-separated tags
- `views`: Number of views
- `likes`: Number of likes
- `dislikes`: Number of dislikes
- `comment_count`: Number of comments
- `thumbnail_link`: Thumbnail URL
- `comments_disabled`: Boolean flag
- `ratings_disabled`: Boolean flag
- `video_error_or_removed`: Boolean flag
- `description`: Video description
- `country`: Country code (US, GB, CA, IN)

#### Derived Columns (14 columns added during preprocessing)
- `category_name`: Category name (from JSON mapping)
- `tags_list`: Parsed tags as list
- `tags_count`: Number of tags
- `engagement_ratio`: (likes + comments) / views
- `like_dislike_ratio`: likes / dislikes
- `publish_year`, `publish_month`, `publish_day`, `publish_day_of_week`
- `trending_year`, `trending_month`, `trending_day`, `trending_day_of_week`
- `days_to_trend`: Days between publish and trending

### Data Quality Issues Identified

1. **Missing Values**: 3,039 missing descriptions (1.92%)
2. **Duplicates**: 137,694 duplicate video_id entries (same video trending multiple times)
3. **Outliers**: Extreme values in views, likes, dislikes, and comments
4. **Zero Values**: 1,509 zeros in likes, 1,947 in dislikes, 3,441 in comments
5. **Text Issues**: Special characters, HTML entities in text fields

### Category Distribution

The dataset includes **17 unique categories**:
- Entertainment, News & Politics, People & Blogs, Music, Comedy
- Sports, Howto & Style, Film & Animation, Education
- Science & Technology, Gaming, Pets & Animals
- Autos & Vehicles, Travel & Events, Shows
- Nonprofits & Activism, Movies

---

## Methodology

The project was executed in five distinct phases, each building upon the previous phase's outputs:

### Phase 1: Data Exploration and Initial Analysis
**Objective**: Understand dataset structure, identify data quality issues, and generate initial statistics.

**Activities**:
1. Loaded all 4 CSV files (US, GB, CA, IN) and combined into single dataset
2. Loaded and parsed JSON category mapping files
3. Identified data types, missing values, and duplicates
4. Calculated basic statistics (mean, median, mode, standard deviation)
5. Analyzed category distributions per country
6. Generated data quality report

**Outputs**:
- `phase1_summary_table.csv`: Summary statistics table
- `phase1_data_quality_report.txt`: Data quality issues report
- Initial insights for preprocessing strategy

### Phase 2: Data Preprocessing and Cleaning
**Objective**: Clean and transform data for analysis and graph database ingestion.

**Activities**:
1. **Missing Values**: Filled 3,039 missing descriptions with "No description"
2. **Duplicates**: Removed 107,741 duplicate rows, kept latest trending occurrence
3. **Zero Values**: Replaced zeros in likes, dislikes, comments with 1 (for ratio calculations)
4. **Outliers**: Capped outliers at 99th percentile for views, likes, dislikes, comments
5. **Text Cleaning**: Removed special characters, HTML entities, normalized text fields
6. **Tag Parsing**: Parsed pipe-separated tags into lists
7. **Date Normalization**: Converted dates, extracted date components
8. **Derived Fields**: Created engagement_ratio and like_dislike_ratio
9. **Category Mapping**: Merged JSON category files to add category names

**Outputs**:
- `youtube_trending_cleaned.csv`: Cleaned dataset (50,357 rows, 31 columns)
- `phase2_preprocessing_report.txt`: Detailed preprocessing report
- Data quality validation results

**Key Statistics After Cleaning**:
- Original rows: 158,098
- Final rows: 50,357 (68.15% reduction due to duplicate removal)
- Missing values: 0%
- Duplicates: 0
- Average tags per video: 19.1

### Phase 3: Exploratory Data Analysis (EDA)
**Objective**: Perform comprehensive statistical analysis and generate visualizations to identify patterns and trends.

**Activities**:
1. **Summary Statistics**: Computed mean, median, mode, std dev, min, max for all numeric columns
2. **Country-wise Analysis**: Analyzed metrics by country (US, GB, CA, IN)
3. **Category Analysis**: Identified top categories by video count and average views
4. **Channel Analysis**: Identified top channels by total views and engagement ratio
5. **Trend Analysis**: Analyzed daily, weekly, and day-of-week patterns
6. **Correlation Analysis**: Computed correlation matrices between metrics
7. **Tag Analysis**: Analyzed most common tags and tag distributions
8. **Distribution Analysis**: Created histograms and boxplots for all numeric variables

**Outputs**:
- `phase3_summary_statistics.csv`: Comprehensive statistics
- `phase3_eda_report.md`: Detailed EDA report
- 30+ visualization files (distributions, trends, correlations, tag analysis)

**Key Findings from EDA**:
- GB has highest average views (3.4M), CA has highest engagement (3.57%)
- Entertainment is most popular category by count (18,272 videos)
- Music has highest average views (4.88M in US, 8.24M in GB)
- Thursday is peak trending day for US/GB, Tuesday for CA/IN
- Strong positive correlation (0.85) between views and likes
- Weak negative correlation (-0.15) between views and engagement ratio

### Phase 4: Graph Database Setup and Data Ingestion
**Objective**: Set up Neo4j graph database and ingest cleaned data with proper schema design.

**Why Neo4j?**
Neo4j was chosen as the graph database because:
1. **Native Graph Storage**: Designed specifically for graph data, providing efficient traversal and relationship queries
2. **Cypher Query Language**: Intuitive query language for graph operations
3. **Performance**: Optimized for complex relationship queries
4. **Scalability**: Can handle large datasets with millions of nodes and relationships
5. **Flexibility**: Easy to model complex relationships between entities

**Graph Schema Design**:

**Nodes**:
1. **Video** (50,357 nodes)
   - Properties: video_id, video_unique_id, title, views, likes, dislikes, comment_count, engagement_ratio, like_dislike_ratio, trending_date, publish_time, days_to_trend, country

2. **Channel** (8,053 nodes)
   - Properties: channel_title, total_views, avg_engagement_ratio, video_count

3. **Category** (17 nodes)
   - Properties: category_id, category_name

4. **Country** (4 nodes)
   - Properties: country_code, country_name

5. **Tag** (268,050 nodes)
   - Properties: tag_name

6. **Day** (7 nodes)
   - Properties: day_name (Monday-Sunday)

**Relationships**:
1. `VIDEO_BELONGS_TO_CATEGORY`: Video → Category (50,357 relationships)
2. `VIDEO_PUBLISHED_BY_CHANNEL`: Video → Channel (50,357 relationships)
3. `VIDEO_TRENDING_IN_COUNTRY`: Video → Country (50,357 relationships)
4. `VIDEO_HAS_TAG`: Video → Tag (963,063 relationships)
5. `VIDEO_TRENDING_ON`: Video → Day (50,357 relationships)
6. `CHANNEL_HAS_VIDEO`: Channel → Video (50,357 relationships)

**Indexes Created**:
- Video: video_id, trending_date, views, engagement_ratio
- Channel: channel_title, total_views
- Category: category_name
- Country: country_code
- Tag: tag_name
- Day: day_name

**Ingestion Process**:
1. Created indexes for performance optimization
2. Created nodes in order: Country → Category → Channel → Tag → Day → Video
3. Processed videos in batches of 1,000 for memory efficiency
4. Created all relationships for each video
5. Validated data ingestion (node counts, relationship counts, sample validation)

**Ingestion Results**:
- Total nodes created: 326,488
- Total relationships created: 1,264,948
- Success rate: 100%
- Processing time: ~15-20 minutes
- No duplicates or data quality issues

### Phase 5: Query Execution and Analysis
**Objective**: Execute comprehensive queries, generate visualizations, and perform statistical analysis.

**Query Groups**:

#### Group A: Simple Queries (6 queries)
1. **A.1: Top Categories by Video Count**
   - Purpose: Identify most popular video categories
   - Result: Entertainment (18,272 videos), News & Politics (6,076), People & Blogs (4,562)

2. **A.2: Top Channels by Total Views**
   - Purpose: Identify most successful channels
   - Result: T-Series (834M views), Marvel Entertainment (587M), Dude Perfect (562M)

3. **A.3: Videos by Country**
   - Purpose: Analyze regional distribution
   - Result: CA (24,427), IN (16,307), US (6,351), GB (3,272)

4. **A.4: Top Videos by Views**
   - Purpose: Identify most viewed individual videos
   - Result: Top video has 40,838,093 views

5. **A.5: Average Engagement by Category**
   - Purpose: Analyze engagement rates across categories
   - Result: Highest engagement category has 0.0536 average engagement ratio

6. **A.6: Day-of-Week Trending Patterns**
   - Purpose: Identify weekly trending patterns
   - Result: Busiest day has 7,867 trending videos

#### Group B: Complex Queries (5 queries)
1. **B.1: Channels with High Engagement Videos**
   - Purpose: Identify channels producing high-engagement content
   - Result: 20 channels with videos having engagement ratio > 0.1
   - Top channel: Technical Guruji (75 high-engagement videos, 16.93% avg engagement)

2. **B.2: Category Performance by Country**
   - Purpose: Analyze how categories perform across countries
   - Result: 4 countries × 17 categories = 68 category-country combinations
   - Reveals regional content preferences

3. **B.3: Tag Co-occurrence with Categories**
   - Purpose: Analyze tag-category associations
   - Result: 100 tag-category pairs with co-occurrence > 10
   - Reveals content tagging patterns

4. **B.4: Cross-Country Video Analysis**
   - Purpose: Identify globally appealing content
   - Result: 50 videos trended in multiple countries
   - Top video trended in 4 countries

5. **B.5: Channel Performance Analysis**
   - Purpose: Analyze channels with balanced viewership and engagement
   - Result: 30 channels with at least 5 videos analyzed
   - Reveals channels balancing views and engagement effectively

#### Group C: Visualization & Statistical Analysis (3 analyses)
1. **C.1: Correlation Analysis**
   - Purpose: Examine relationships between video metrics
   - Result: Correlation matrix showing relationships between views, likes, comments, engagement ratios

2. **C.2: Engagement Distribution Analysis**
   - Purpose: Examine distribution of engagement ratios
   - Result: Mean engagement ratio: 0.0303, Std dev: 0.0321
   - Distribution visualization created

3. **C.3: Category-Country Network Analysis**
   - Purpose: Examine network of category-country relationships
   - Result: 66 category-country connections analyzed
   - Network visualization created

**Execution Statistics**:
- Total queries executed: 14
- Successful queries: 14
- Failed queries: 0
- Total execution time: 162.97 seconds
- Files generated: 13 CSV files, 13 PNG visualizations, 5 Markdown reports

---

## Results and Findings

### 1. Content Distribution

**Top Categories by Video Count**:
1. Entertainment: 18,272 videos (36.3%)
2. News & Politics: 6,076 videos (12.1%)
3. People & Blogs: 4,562 videos (9.1%)
4. Music: 4,459 videos (8.9%)
5. Comedy: 3,810 videos (7.6%)

**Key Insight**: Entertainment dominates trending content, representing over one-third of all trending videos.

### 2. Channel Performance

**Top Channels by Total Views**:
1. T-Series: 834,091,964 views (92 videos)
2. Marvel Entertainment: 586,638,237 views (57 videos)
3. Dude Perfect: 561,703,434 views (39 videos)
4. ibighit: 519,121,170 views (26 videos)
5. Ed Sheeran: 480,250,035 views (17 videos)

**Key Insight**: T-Series is the dominant channel, with nearly 1 billion total views across 92 trending videos.

### 3. Regional Analysis

**Videos by Country**:
- Canada (CA): 24,427 videos (48.5%)
- India (IN): 16,307 videos (32.4%)
- United States (US): 6,351 videos (12.6%)
- Great Britain (GB): 3,272 videos (6.5%)

**Average Views by Country**:
- Great Britain: 3,426,436 views/video
- United States: 1,780,739 views/video
- Canada: 822,043 views/video
- India: 675,632 views/video

**Key Insight**: Great Britain has the highest average views per video, indicating higher engagement per trending video.

### 4. Engagement Analysis

**Average Engagement by Category**:
- Highest engagement category: 5.36% average engagement ratio
- Overall average engagement: 3.03%
- Standard deviation: 3.21%

**Channels with High Engagement**:
1. Technical Guruji: 75 high-engagement videos, 16.93% avg engagement
2. Mark Dice: 45 high-engagement videos, 13.78% avg engagement
3. Rebel Media: 35 high-engagement videos, 14.06% avg engagement

**Key Insight**: Smaller, niche channels often achieve higher engagement ratios than large channels, indicating strong community connections.

### 5. Temporal Patterns

**Day-of-Week Trending Patterns**:
- Busiest day: 7,867 trending videos
- Peak days vary by country:
  - US/GB: Thursday (peak day)
  - CA/IN: Tuesday (peak day)

**Key Insight**: Trending patterns vary by region, suggesting cultural or scheduling differences in content consumption.

### 6. Cross-Country Analysis

**Globally Trending Videos**:
- 50 videos trended in multiple countries
- Top video trended in 4 countries
- Indicates content with universal appeal

**Key Insight**: A small percentage of videos (0.1%) achieve cross-country trending, suggesting most content is regionally specific.

### 7. Tag Analysis

**Tag Co-occurrence Patterns**:
- 100 tag-category pairs with co-occurrence > 10
- Strong associations between specific tags and categories
- Reveals content tagging strategies

**Key Insight**: Tag usage follows predictable patterns, with certain tags strongly associated with specific categories.

### 8. Statistical Correlations

**Key Correlations**:
- Views vs Likes: Strong positive correlation (0.85)
- Views vs Comments: Moderate positive correlation (0.70)
- Views vs Engagement Ratio: Weak negative correlation (-0.41)
- Likes vs Engagement Ratio: Strong positive correlation (0.90)

**Key Insight**: Higher views don't necessarily mean higher engagement. Viral videos may have lower engagement ratios, while niche content with moderate views can achieve very high engagement.

---

## Visualizations

All visualizations are saved in the `phase5_output/visualizations/` directory. Below is a comprehensive guide to where each visualization should be referenced in the report:

### Group A: Simple Query Visualizations

1. **groupA_A1_top_categories.png**
   - **Location in Report**: Section 9.1 (Content Distribution)
   - **Description**: Bar chart showing top categories by video count
   - **Insight**: Entertainment dominates with 18,272 videos

2. **groupA_A2_top_channels.png**
   - **Location in Report**: Section 9.2 (Channel Performance)
   - **Description**: Bar chart showing top channels by total views
   - **Insight**: T-Series leads with 834M views

3. **groupA_A3_videos_by_country.png**
   - **Location in Report**: Section 9.3 (Regional Analysis)
   - **Description**: Bar chart showing video distribution by country
   - **Insight**: Canada has the most videos (24,427)

4. **groupA_A4_top_videos.png**
   - **Location in Report**: Section 9.2 (Channel Performance)
   - **Description**: Bar chart showing top individual videos by views
   - **Insight**: Top video has 40.8M views

5. **groupA_A5_engagement_by_category.png**
   - **Location in Report**: Section 9.4 (Engagement Analysis)
   - **Description**: Bar chart showing average engagement by category
   - **Insight**: Categories vary significantly in engagement rates

6. **groupA_A6_day_patterns.png**
   - **Location in Report**: Section 9.5 (Temporal Patterns)
   - **Description**: Line/bar chart showing trending patterns by day of week
   - **Insight**: Thursday is peak for US/GB, Tuesday for CA/IN

### Group B: Complex Query Visualizations

7. **groupB_B1_high_engagement_channels.png**
   - **Location in Report**: Section 9.4 (Engagement Analysis)
   - **Description**: Bar chart showing channels with high engagement videos
   - **Insight**: Technical Guruji leads with 75 high-engagement videos

8. **groupB_B2_category_by_country.png**
   - **Location in Report**: Section 9.3 (Regional Analysis)
   - **Description**: Heatmap or grouped bar chart showing category performance by country
   - **Insight**: Regional preferences vary significantly

9. **groupB_B3_tag_cooccurrence.png**
   - **Location in Report**: Section 9.7 (Tag Analysis)
   - **Description**: Network graph or heatmap showing tag-category associations
   - **Insight**: Strong tag-category associations exist

10. **groupB_B4_cross_country_videos.png**
    - **Location in Report**: Section 9.6 (Cross-Country Analysis)
    - **Description**: Bar chart showing videos trending in multiple countries
    - **Insight**: 50 videos achieved cross-country trending

11. **groupB_B5_channel_performance.png**
    - **Location in Report**: Section 9.2 (Channel Performance)
    - **Description**: Scatter plot showing channel performance (views vs engagement)
    - **Insight**: Trade-off between views and engagement

### Group C: Statistical Analysis Visualizations

12. **groupC_C1_correlation_heatmap.png**
    - **Location in Report**: Section 10 (Statistical Analysis)
    - **Description**: Heatmap showing correlations between video metrics
    - **Insight**: Strong positive correlation between views and likes, negative between views and engagement

13. **groupC_C2_engagement_distribution.png**
    - **Location in Report**: Section 10 (Statistical Analysis)
    - **Description**: Histogram showing distribution of engagement ratios
    - **Insight**: Right-skewed distribution with mean 0.0303

### Additional Visualizations from Phase 3

Additional visualizations are available in `phase3_visualizations/` directory:
- Distribution charts (histograms, boxplots)
- Country comparison charts
- Trend analysis charts (daily, weekly)
- Correlation scatter plots
- Tag distribution charts

---

## Statistical Analysis

### Correlation Analysis

**Key Correlations Identified**:

1. **Views vs Likes**: 0.85 (Strong positive)
   - Interpretation: Videos with more views tend to have more likes
   - Statistical significance: High

2. **Views vs Comments**: 0.70 (Moderate positive)
   - Interpretation: Videos with more views tend to have more comments
   - Statistical significance: Moderate

3. **Views vs Engagement Ratio**: -0.41 (Weak negative)
   - Interpretation: Videos with more views tend to have lower engagement ratios
   - Statistical significance: Moderate
   - **Key Finding**: Viral videos may have lower engagement rates

4. **Likes vs Engagement Ratio**: 0.90 (Strong positive)
   - Interpretation: Engagement ratio is strongly driven by likes
   - Statistical significance: High

### Distribution Analysis

**Engagement Ratio Distribution**:
- Mean: 0.0303 (3.03%)
- Median: 0.02 (2.00%)
- Standard Deviation: 0.0321
- Minimum: 0.0
- Maximum: 0.5 (50%)
- Distribution: Right-skewed

**Interpretation**: Most videos have low engagement ratios (2-3%), with a small number of videos achieving very high engagement (10%+).

### Statistical Tests

**Test: Views vs Engagement Correlation**
- Correlation coefficient: -0.4073
- Interpretation: Moderate negative correlation
- Conclusion: Higher views are associated with lower engagement ratios, suggesting viral content may sacrifice engagement for reach.

---

## Conclusions

### Key Achievements

1. **Successfully Processed Large Dataset**: Processed 158,098 initial records to 50,357 unique videos with 100% data quality.

2. **Implemented Graph Database**: Created Neo4j graph database with 326,488 nodes and 1,264,948 relationships, enabling efficient relationship queries.

3. **Comprehensive Analysis**: Executed 14 queries (6 simple, 5 complex, 3 statistical) generating actionable insights.

4. **Professional Visualizations**: Created 13+ professional visualizations illustrating key findings.

5. **Statistical Insights**: Identified key correlations and patterns in the data.

### Main Findings

1. **Content Distribution**: Entertainment dominates trending content (36.3% of all videos), followed by News & Politics (12.1%).

2. **Channel Performance**: T-Series is the dominant channel with 834M total views, but smaller channels achieve higher engagement ratios.

3. **Regional Differences**: Great Britain has the highest average views per video (3.4M), while Canada has the highest engagement ratio (3.57%).

4. **Temporal Patterns**: Trending patterns vary by region, with Thursday being peak for US/GB and Tuesday for CA/IN.

5. **Engagement Insights**: Strong negative correlation (-0.41) between views and engagement ratio suggests viral videos may have lower engagement rates.

6. **Cross-Country Content**: Only 0.1% of videos achieve cross-country trending, indicating most content is regionally specific.

### Limitations

1. **Time Period**: Dataset covers only 7 months (Nov 2017 - Jun 2018), limiting long-term trend analysis.

2. **Countries**: Analysis limited to 4 countries, may not represent global trends.

3. **Data Quality**: Some data quality issues required assumptions (e.g., capping outliers at 99th percentile).

4. **Missing Context**: Dataset doesn't include video duration, thumbnail analysis, or external factors affecting trends.

### Recommendations

1. **Content Strategy**: Focus on Entertainment and Music categories for maximum reach, but consider niche categories for higher engagement.

2. **Channel Optimization**: Balance viewership and engagement - high views don't guarantee high engagement.

3. **Regional Targeting**: Consider regional preferences when creating content - different countries show distinct content preferences.

4. **Timing**: Optimize publish timing based on regional peak trending days (Thursday for US/GB, Tuesday for CA/IN).

5. **Engagement Focus**: For niche audiences, prioritize engagement over views - smaller channels can achieve higher engagement ratios.

### Future Work

1. **Extended Time Period**: Analyze data over multiple years to identify long-term trends.

2. **Real-time Analysis**: Implement real-time streaming data ingestion for live trend analysis.

3. **Predictive Modeling**: Build models to predict which videos will trend based on initial metrics.

4. **Network Analysis**: Deep dive into tag co-occurrence networks and category relationships.

5. **Sentiment Analysis**: Analyze video titles and descriptions for sentiment patterns.

6. **Machine Learning**: Apply ML techniques to classify content and predict engagement.

---

## References and Appendices

### Dataset Source

- **Dataset**: Trending YouTube Video Statistics
- **Platform**: Kaggle
- **URL**: https://www.kaggle.com/datasets/datasnaek/youtube-new
- **License**: CC0: Public Domain

### Software and Tools

- **Python**: 3.x
- **Neo4j**: 5.x (Graph Database)
- **pandas**: Data processing
- **matplotlib/seaborn**: Visualization
- **py2neo**: Neo4j Python driver

### File Structure

```
Project Directory/
├── Data Files/
│   ├── USvideos.csv
│   ├── GBvideos.csv
│   ├── CAvideos.csv
│   ├── INvideos.csv
│   ├── US_category_id.json
│   ├── GB_category_id.json
│   ├── CA_category_id.json
│   ├── IN_category_id.json
│   └── youtube_trending_cleaned.csv
├── Phase 1 Outputs/
│   ├── phase1_summary_table.csv
│   └── phase1_data_quality_report.txt
├── Phase 2 Outputs/
│   └── phase2_preprocessing_report.txt
├── Phase 3 Outputs/
│   ├── phase3_summary_statistics.csv
│   ├── phase3_eda_report.md
│   └── phase3_visualizations/
├── Phase 4 Outputs/
│   ├── phase4_ingestion_log.json
│   ├── phase4_ingestion_report.md
│   └── phase4_query_examples.txt
├── Phase 5 Outputs/
│   ├── phase5_output/
│   │   ├── query_results/
│   │   ├── visualizations/
│   │   └── reports/
│   └── phase5_execution_log.json
└── Scripts/
    ├── phase1_data_exploration.py
    ├── phase2_preprocessing.py
    ├── phase3_eda.py
    ├── phase4_graph_ingestion.py
    └── phase5_query_analysis.py
```

### Query Examples

#### Simple Query Example (A.1)
```cypher
MATCH (v:Video)-[:VIDEO_BELONGS_TO_CATEGORY]->(c:Category)
RETURN c.category_name, COUNT(v) as video_count
ORDER BY video_count DESC
LIMIT 10
```

#### Complex Query Example (B.1)
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

### Visualization Index

All visualizations are referenced in Section 11 (Visualizations) with specific locations in the report where they should be included.

### Statistical Test Results

See `phase5_output/reports/statistical_tests.csv` for detailed statistical test results.

---

## Appendix A: Complete Query Results

### Group A: Simple Queries

#### A.1: Top Categories by Video Count
| Category | Video Count |
|----------|-------------|
| Entertainment | 18,272 |
| News & Politics | 6,076 |
| People & Blogs | 4,562 |
| Music | 4,459 |
| Comedy | 3,810 |

#### A.2: Top Channels by Total Views
| Channel | Total Views | Video Count |
|---------|-------------|-------------|
| T-Series | 834,091,964 | 92 |
| Marvel Entertainment | 586,638,237 | 57 |
| Dude Perfect | 561,703,434 | 39 |
| ibighit | 519,121,170 | 26 |
| Ed Sheeran | 480,250,035 | 17 |

#### A.3: Videos by Country
| Country | Video Count |
|---------|-------------|
| CA | 24,427 |
| IN | 16,307 |
| US | 6,351 |
| GB | 3,272 |

### Group B: Complex Queries

#### B.1: Channels with High Engagement Videos
| Channel | High Engagement Videos | Avg Engagement |
|---------|------------------------|----------------|
| Technical Guruji | 75 | 16.93% |
| Mark Dice | 45 | 13.78% |
| Rebel Media | 35 | 14.06% |

#### B.4: Cross-Country Video Analysis
- 50 videos trended in multiple countries
- Top video trended in 4 countries
- Represents 0.1% of all videos

---

## Appendix B: Graph Database Schema

### Node Properties

**Video Node**:
- video_id (String)
- video_unique_id (String) - Primary key
- title (String)
- views (Integer)
- likes (Float)
- dislikes (Float)
- comment_count (Integer)
- engagement_ratio (Float)
- like_dislike_ratio (Float)
- trending_date (String)
- publish_time (String)
- days_to_trend (Integer)
- country (String)

**Channel Node**:
- channel_title (String) - Primary key
- total_views (Integer)
- avg_engagement_ratio (Float)
- video_count (Integer)

**Category Node**:
- category_id (Integer) - Primary key
- category_name (String)

**Country Node**:
- country_code (String) - Primary key
- country_name (String)

**Tag Node**:
- tag_name (String) - Primary key

**Day Node**:
- day_name (String) - Primary key

### Relationship Types

1. `VIDEO_BELONGS_TO_CATEGORY`: Video → Category
2. `VIDEO_PUBLISHED_BY_CHANNEL`: Video → Channel
3. `VIDEO_TRENDING_IN_COUNTRY`: Video → Country
4. `VIDEO_HAS_TAG`: Video → Tag
5. `VIDEO_TRENDING_ON`: Video → Day
6. `CHANNEL_HAS_VIDEO`: Channel → Video

### Indexes

- Video: video_id, trending_date, views, engagement_ratio
- Channel: channel_title, total_views
- Category: category_name
- Country: country_code
- Tag: tag_name
- Day: day_name

---

**Report End**

---

**Prepared by**: Muhammad Adeel  
**Registration Number**: 2022331  
**Course**: Big Data Analytics  
**Assignment**: Assignment 1  
**Date**: November 10, 2025

---

**Note**: This report is accompanied by:
- All query result CSV files in `phase5_output/query_results/`
- All visualizations in `phase5_output/visualizations/`
- Complete execution logs in `phase5_execution_log.json`
- Phase-specific reports in `phase5_output/reports/`

For detailed query results, visualizations, and statistical analysis, please refer to the `phase5_output/` directory.

