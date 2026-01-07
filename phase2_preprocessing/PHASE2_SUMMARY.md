# Phase 2: Data Preprocessing - Summary Report

## ✅ Completed Tasks

### 1. Handle Missing Values
- ✅ Filled 3,039 missing descriptions with "No description"
- ✅ Verified no missing values in critical columns
- ✅ Dropped rows with missing critical values

### 2. Handle Duplicates
- ✅ Identified 135,442 duplicate video_id entries within countries
- ✅ Removed 107,741 duplicate rows
- ✅ Kept latest trending occurrence based on trending_date
- ✅ Aggregated engagement metrics (used max values)
- ✅ Verified no duplicates remain (0 duplicates)

### 3. Handle Zero/Negative Values
- ✅ Replaced 1,509 zeros in likes with 1
- ✅ Replaced 1,947 zeros in dislikes with 1
- ✅ Replaced 3,441 zeros in comment_count with 1
- ✅ Ensured all numeric fields are >= 0

### 4. Handle Outliers
- ✅ Capped outliers at 99th percentile:
  - Views: 1,580 outliers capped at 40,838,093
  - Likes: 1,581 outliers capped at 985,483
  - Dislikes: 1,581 outliers capped at 51,198
  - Comment_count: 1,581 outliers capped at 90,063

### 5. Text Cleaning
- ✅ Cleaned title, description, channel_title
- ✅ Removed special characters, extra whitespace, HTML entities
- ✅ Parsed tags column (pipe-separated) into lists
- ✅ Created tags_list and tags_count columns
- ✅ Average 19.1 tags per video

### 6. Date Normalization
- ✅ Converted publish_time and trending_date to datetime objects
- ✅ Removed timezone information (made both timezone-naive)
- ✅ Extracted date components:
  - publish_year, publish_month, publish_day, publish_day_of_week
  - trending_year, trending_month, trending_day, trending_day_of_week
- ✅ Calculated days_to_trend (range: 0 to 4,214 days)

### 7. Merge Category Mappings
- ✅ Loaded all JSON category files
- ✅ Created category_name column
- ✅ Applied country-specific category mapping
- ✅ All categories successfully mapped

### 8. Derived Fields
- ✅ Created engagement_ratio = (likes + comment_count) / views
- ✅ Created like_dislike_ratio = likes / dislikes
- ✅ Rounded ratios to 2 decimal places
- ✅ Handled infinite values (replaced with 0)

### 9. Data Validation
- ✅ No duplicates remaining (video_id per country)
- ✅ All numeric fields are >= 0
- ✅ All category names valid
- ✅ All countries valid
- ✅ Date components consistent

### 10. Output
- ✅ Saved cleaned dataset as `youtube_trending_cleaned.csv`
- ✅ Saved summary report as `phase2_preprocessing_report.txt`
- ✅ Saved preprocessing script as `phase2_preprocessing.py`

## 📊 Key Results

### Dataset Transformation
- **Original rows**: 158,098
- **Final rows**: 50,357
- **Rows removed**: 107,741 (68.15%)
- **Final columns**: 31 (added 14 new columns)

### Rows per Country (After Cleaning)
- **CA**: 24,427 rows
- **GB**: 3,272 rows
- **IN**: 16,307 rows
- **US**: 6,351 rows

### Data Quality Improvements
1. **Missing Values**: All filled
2. **Duplicates**: All removed
3. **Outliers**: Capped at 99th percentile
4. **Zero Values**: Replaced with 1 for ratio calculations
5. **Text Fields**: Cleaned and normalized
6. **Dates**: Normalized and components extracted

### Statistics After Cleaning
- **Mean views**: 1,064,764
- **Mean likes**: 28,141
- **Mean dislikes**: 1,293
- **Mean comments**: 3,076
- **Average tags per video**: 19.1

## 📁 Output Files

1. **youtube_trending_cleaned.csv** - Cleaned and preprocessed dataset (50,357 rows, 31 columns)
2. **phase2_preprocessing_report.txt** - Detailed preprocessing report
3. **phase2_preprocessing.py** - Preprocessing script

## 🔍 New Columns Added

### Date Components
- `publish_year`, `publish_month`, `publish_day`, `publish_day_of_week`
- `trending_year`, `trending_month`, `trending_day`, `trending_day_of_week`
- `days_to_trend`

### Category
- `category_name`

### Tags
- `tags_list` - Parsed tags as list (stored as string in CSV)
- `tags_count` - Number of tags per video

### Engagement Metrics
- `engagement_ratio` - (likes + comments) / views
- `like_dislike_ratio` - likes / dislikes

## 🎯 Data Quality Validation

✅ **All validation checks passed:**
- No duplicates remaining
- All numeric fields >= 0
- All categorical fields valid
- Date components consistent
- No missing values in critical columns

## 📈 Key Insights

### Duplicate Handling
- Many videos appeared multiple times in trending lists
- Consolidated to one entry per video_id per country
- Used latest trending date and max engagement metrics

### Outlier Impact
- Outliers significantly skewed the data
- Capping at 99th percentile reduced extreme values
- More realistic statistics after capping

### Text Cleaning
- Special characters and HTML entities removed
- Tags successfully parsed into lists
- Ready for text analysis in next phases

### Date Analysis
- Videos can take 0 to 4,214 days to trend
- Date components extracted for time-based analysis
- Ready for temporal pattern analysis

## 🔄 Next Steps (Phase 3)

The cleaned dataset is ready for:
1. **Exploratory Data Analysis (EDA)**
   - Visualizations
   - Statistical analysis
   - Pattern identification

2. **Graph Database Ingestion**
   - Create nodes (Videos, Channels, Categories, Tags)
   - Create relationships
   - Store in Neo4j

3. **Advanced Analysis**
   - Trend analysis over time
   - Category popularity trends
   - Engagement pattern analysis

## ⚠️ Notes

1. **Tags List**: In CSV format, `tags_list` is stored as a string representation. When loading, parse it back to a list using `ast.literal_eval()` or `json.loads()`.

2. **Row Reduction**: Significant reduction in rows (68%) is expected due to duplicate removal. This is normal as videos appearing multiple times in trending are consolidated.

3. **Country Distribution**: GB has fewer unique videos (3,272) compared to others, which is expected based on the original data distribution after deduplication.

4. **Outlier Capping**: Values are capped at 99th percentile, which may affect very popular videos. Consider this when analyzing top performers.

---

**Phase 2 Status**: ✅ **COMPLETED SUCCESSFULLY**

**Ready for Phase 3**: Exploratory Data Analysis (EDA) and Graph Database Setup

