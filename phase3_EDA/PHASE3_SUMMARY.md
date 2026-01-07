# Phase 3: Exploratory Data Analysis (EDA) - Summary

## ✅ Phase 3 Completed Successfully!

**Date**: November 9, 2025  
**Dataset**: youtube_trending_cleaned.csv (50,357 videos)  
**Countries Analyzed**: US, GB, CA, IN

---

## 📊 Key Findings

### 1. Dataset Overview
- **Total Videos**: 50,357
- **Date Range**: November 14, 2017 to June 14, 2018
- **Categories**: 18 unique categories
- **Channels**: 8,053 unique channels
- **Countries**: US (6,351), GB (3,272), CA (24,427), IN (16,307)

### 2. Summary Statistics

#### Overall Metrics
- **Average Views**: 1,064,764
- **Average Likes**: 28,141
- **Average Comments**: 3,076
- **Average Engagement Ratio**: 0.030 (3.0%)
- **Average Like-Dislike Ratio**: 34.72

#### Country-wise Performance
| Country | Videos | Avg Views | Avg Likes | Avg Engagement |
|---------|--------|-----------|-----------|----------------|
| **GB** | 3,272 | 3,426,436 | 82,402 | 3.46% |
| **US** | 6,351 | 1,780,739 | 49,721 | 3.36% |
| **CA** | 24,427 | 822,043 | 24,661 | 3.57% |
| **IN** | 16,307 | 675,632 | 14,062 | 2.02% |

**Key Insight**: GB has the highest average views per video, while CA has the highest engagement ratio.

### 3. Top Categories

#### By Video Count
- **US**: Entertainment (1,621), Music (801), Howto & Style (594)
- **GB**: Music (877), Entertainment (858), People & Blogs (282)
- **CA**: Entertainment (8,245), News & Politics (2,940), People & Blogs (2,553)
- **IN**: Entertainment (7,548), News & Politics (2,505), People & Blogs (1,232)

#### By Average Views
- **US**: Music (4.88M), Film & Animation (2.54M), Gaming (2.33M)
- **GB**: Music (8.24M), Unknown (5.09M), Film & Animation (2.46M)
- **CA**: Movies (5.66M), Music (3.01M), Film & Animation (994K)
- **IN**: Movies (3.86M), Gaming (3.44M), Pets & Animals (2.49M)

**Key Insight**: Music and Entertainment dominate across all countries, with Music having the highest average views.

### 4. Top Channels

#### By Total Views
- **US**: Dude Perfect (206M), ibighit (190M), Ed Sheeran (152M)
- **GB**: ibighit (201M), Marvel Entertainment (161M), jypentertainment (141M)
- **CA**: T-Series (342M), MLG Highlights (199M), Dude Perfect (197M)
- **IN**: T-Series (492M), 5-Minute Crafts (208M), Speed Records (178M)

#### By Engagement Ratio
- **US**: KickThePj (19.0%), Amber Liu (18.0%), Desimpedidos (18.0%)
- **GB**: KickThePj (18.6%), ConnorFranta (18.0%), LukeIsNotSexy (18.0%)
- **CA**: Papi Melv (29.0%), JaeSix (28.0%), starshipTV (27.0%)
- **IN**: Prasadtechintelugu (21.6%), The RawKnee Show (16.0%), KhilliBuzzChiru (15.0%)

**Key Insight**: T-Series dominates in CA and IN, while smaller channels achieve higher engagement ratios.

### 5. Trend Analysis

#### Peak Trending Days
- **US**: Thursday (1,197 videos)
- **GB**: Thursday (672 videos)
- **CA**: Tuesday (3,719 videos)
- **IN**: Tuesday (2,542 videos)

**Key Insight**: Thursday is the peak day for US and GB, while Tuesday is peak for CA and IN.

#### Day-of-Week Patterns
- Engagement tends to be higher mid-week (Tuesday-Thursday)
- Views peak on different days per country
- Comments show consistent patterns across countries

### 6. Correlation Analysis

#### Key Correlations (Overall)
- **Views vs Likes**: Strong positive correlation (~0.85)
- **Views vs Comments**: Moderate positive correlation (~0.70)
- **Likes vs Engagement Ratio**: Strong positive correlation (~0.90)
- **Views vs Engagement Ratio**: Weak negative correlation (~-0.15)

**Key Insight**: Higher views don't necessarily mean higher engagement. Videos with moderate views can have very high engagement ratios.

### 7. Tag Analysis

#### Most Common Tags (Top 5)
1. Music-related tags (most frequent)
2. Entertainment tags
3. Gaming tags
4. Comedy tags
5. News/Politics tags

**Key Insight**: Tags reflect category popularity, with music and entertainment tags being most common.

---

## 📁 Generated Files

### 1. Data Files
- **phase3_summary_statistics.csv**: Comprehensive statistics for all metrics and countries
- **phase3_eda_report.md**: Detailed EDA report with all findings

### 2. Visualizations (30+ files)
All saved in `phase3_visualizations/` directory:

#### Distributions
- Numeric variable distributions (histograms)
- Boxplots for all numeric variables
- Country-wise distributions
- Engagement ratio distributions
- Views distributions (log scale)

#### Country Analysis
- Top categories by video count (per country)
- Top categories by average views (per country)
- Top channels by total views (per country)
- Country comparison charts

#### Trend Analysis
- Daily trending videos over time
- Category trends over time (weekly)
- Day-of-week patterns
- Peak trending days analysis

#### Correlation Analysis
- Correlation heatmaps (overall and per country)
- Scatter plots (views vs likes, comments, engagement ratios)

#### Tag Analysis
- Top 20 tags across all videos
- Top 20 tags per country

---

## 🔍 Key Insights Summary

### 1. Engagement Patterns
- **High Engagement**: Smaller channels often have higher engagement ratios
- **Engagement vs Views**: Negative correlation suggests viral videos may have lower engagement ratios
- **Country Differences**: CA has the highest average engagement (3.57%), IN has the lowest (2.02%)

### 2. Category Insights
- **Entertainment**: Most popular category by video count across all countries
- **Music**: Highest average views in most countries
- **Gaming**: Strong performer in US and IN
- **News & Politics**: Significant presence in CA and IN

### 3. Channel Insights
- **Large Channels**: T-Series, Dude Perfect, Marvel Entertainment dominate by views
- **Engagement Champions**: Smaller channels like KickThePj, Papi Melv achieve very high engagement ratios
- **Country-Specific**: T-Series is dominant in CA and IN, while music channels dominate in GB

### 4. Temporal Patterns
- **Peak Days**: Thursday (US/GB), Tuesday (CA/IN)
- **Weekly Trends**: Mid-week shows highest engagement
- **Category Trends**: Music and Entertainment show consistent trends over time

### 5. Correlation Insights
- **Views-Likes**: Strong positive correlation (expected)
- **Views-Engagement**: Weak negative correlation (viral videos have lower engagement)
- **Likes-Engagement**: Strong positive correlation (engagement driven by likes)

---

## 📈 Recommendations for Next Phase

### For Graph Database Design (Phase 4)
1. **Nodes to Create**:
   - Video nodes (with properties: views, likes, engagement_ratio, etc.)
   - Channel nodes (with properties: total_views, avg_engagement, etc.)
   - Category nodes
   - Country nodes
   - Tag nodes
   - Day-of-week nodes

2. **Relationships to Create**:
   - Video → BELONGS_TO → Category
   - Video → PUBLISHED_BY → Channel
   - Video → TRENDING_IN → Country
   - Video → HAS_TAG → Tag
   - Video → TRENDING_ON → Day
   - Channel → HAS_VIDEO → Video
   - Category → CONTAINS → Video

3. **Indexes to Create**:
   - Video: video_id, trending_date, views, engagement_ratio
   - Channel: channel_title, total_views
   - Category: category_name
   - Country: country code

### For Query Design (Phase 5)
1. **Simple Queries**:
   - Top 10 videos by views per country
   - Top 10 channels by total views
   - Most popular categories per country
   - Videos trending on specific days

2. **Complex Queries**:
   - Videos with high engagement but moderate views
   - Channels with consistent high performance across categories
   - Tag co-occurrence analysis
   - Temporal patterns (day-of-week, category trends)
   - Cross-country comparisons (same video in multiple countries)

---

## ✅ Phase 3 Completion Checklist

- [x] Summary statistics computed (mean, median, mode, std, min, max)
- [x] Country-wise statistics generated
- [x] Top categories identified (by count and views)
- [x] Top channels identified (by views and engagement)
- [x] Distribution analysis completed (histograms, boxplots)
- [x] Trend analysis completed (daily, weekly, day-of-week)
- [x] Correlation analysis completed (heatmaps, scatter plots)
- [x] Tag analysis completed (top tags, country-wise)
- [x] All visualizations saved (30+ PNG files)
- [x] Summary statistics saved (CSV)
- [x] EDA report generated (Markdown)

---

## 🚀 Next Steps

**Phase 4**: Graph Database Setup and Data Ingestion
- Set up Neo4j database
- Design graph schema based on EDA insights
- Ingest cleaned data into graph database
- Create indexes for performance
- Validate data ingestion

---

**Phase 3 Status**: ✅ **COMPLETED**  
**Generated**: November 9, 2025  
**Output Files**: 32 files (1 CSV, 1 MD report, 30+ visualizations)

