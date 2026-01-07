# Phase 2: Data Preprocessing and Cleaning

## Overview
This phase focuses on cleaning, transforming, and preparing the YouTube Trending Videos dataset for analysis.

## Prerequisites
- Phase 1 must be completed
- All CSV and JSON files must be present in the directory
- Virtual environment activated with required packages installed

## Setup Instructions

### 1. Activate Virtual Environment
```bash
# On Windows (PowerShell)
venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
venv\Scripts\activate.bat

# On Linux/Mac
source venv/bin/activate
```

### 2. Run Phase 2 Preprocessing
```bash
python phase2_preprocessing.py
```

## What Phase 2 Does

### 1. Handle Missing Values
- Fills missing description values with "No description"
- Drops rows with missing critical values (views, likes, etc.)

### 2. Handle Duplicates
- Removes duplicate video_id entries within the same country
- Keeps only the latest trending occurrence based on trending_date
- Aggregates engagement metrics (uses max values)

### 3. Handle Zero/Negative Values
- Replaces zeros in likes, dislikes, comment_count with 1 (for safe ratio calculations)
- Ensures all numeric fields are >= 0

### 4. Handle Outliers
- Identifies extreme outliers in numeric fields
- Caps values at 99th percentile to reduce skewness

### 5. Text Cleaning
- Cleans title, description, channel_title: removes special characters, extra whitespace, HTML entities
- Parses tags column (pipe-separated) into a list
- Creates tags_list and tags_count columns

### 6. Date Normalization
- Converts publish_time and trending_date into datetime objects
- Extracts date components:
  - publish_year, publish_month, publish_day, publish_day_of_week
  - trending_year, trending_month, trending_day, trending_day_of_week
- Calculates days_to_trend = trending_date - publish_time

### 7. Merge Category Mappings
- Merges JSON category files into the dataset
- Creates category_name column
- Applies country-specific category mapping

### 8. Derived Fields
- Creates engagement_ratio = (likes + comment_count) / views
- Creates like_dislike_ratio = likes / dislikes
- Rounds ratios to 2 decimal places

### 9. Data Validation
- Verifies no duplicates remain (video_id per country)
- Ensures all numeric fields are >= 0
- Validates categorical fields and countries
- Checks date component consistency

### 10. Output
- Saves cleaned dataset as `youtube_trending_cleaned.csv`
- Saves summary report as `phase2_preprocessing_report.txt`

## Expected Output Files

1. **youtube_trending_cleaned.csv** - Cleaned and preprocessed dataset
2. **phase2_preprocessing_report.txt** - Summary report with statistics

## Key Features

### Data Quality Improvements
- Missing values handled
- Duplicates removed
- Outliers capped
- Text fields cleaned
- Dates normalized

### New Columns Added
- `category_name` - Category name from JSON mapping
- `tags_list` - Parsed tags as a list
- `tags_count` - Number of tags per video
- `publish_year`, `publish_month`, `publish_day`, `publish_day_of_week`
- `trending_year`, `trending_month`, `trending_day`, `trending_day_of_week`
- `days_to_trend` - Days between publish and trending
- `engagement_ratio` - (likes + comments) / views
- `like_dislike_ratio` - likes / dislikes

### Data Validation
- No duplicates (video_id per country)
- All numeric fields >= 0
- All categorical fields valid
- Date components consistent

## Next Steps

After completing Phase 2, proceed to:
- **Phase 3**: Exploratory Data Analysis (EDA)
- Use the cleaned dataset for visualization and statistical analysis

## Troubleshooting

### Common Issues

1. **Memory Error**: If dataset is too large, process countries separately
2. **Date Parsing Errors**: Check date formats in source data
3. **Missing JSON Files**: Ensure all category JSON files are present
4. **Duplicate Handling**: Review aggregation strategy if needed

## Performance Notes

- Processing time: ~2-5 minutes depending on system
- Memory usage: ~500MB - 1GB
- Output file size: ~50-100MB (CSV)

