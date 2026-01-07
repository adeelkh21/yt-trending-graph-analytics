# Phase 1: Data Exploration and Initial Analysis

## Overview
This phase focuses on loading, inspecting, and understanding the YouTube Trending Videos dataset.


## Run Phase 1 Exploration
```bash
python phase1_data_exploration.py
```

## Expected Output Files

1. **phase1_summary_table.csv** - Summary statistics table
2. **phase1_data_quality_report.txt** - Data quality issues report

## What Phase 1 Does

1. **Data Loading**
   - Loads all 4 CSV files (US, GB, CA, IN)
   - Combines them into a single dataframe
   - Adds country identifier to each row

2. **Data Inspection**
   - Checks data shapes and dimensions
   - Identifies data types
   - Finds missing values
   - Detects duplicates

3. **Category Mapping**
   - Loads JSON category files
   - Maps category IDs to category names
   - Creates category name column

4. **Date Analysis**
   - Parses trending_date (YY.DD.MM format)
   - Parses publish_time (ISO format)
   - Calculates date ranges per country

5. **Statistics Generation**
   - Basic statistics for numeric columns (views, likes, dislikes, comments)
   - Category distributions per country
   - Summary tables and reports

6. **Data Quality Assessment**
   - Missing values report
   - Duplicates detection
   - Special characters analysis
   - Outlier detection
   - Data type validation

## Key Metrics Analyzed

- **Rows per country**: Total number of records per country
- **Date ranges**: Trending date and publish time ranges
- **Category distributions**: Top categories per country
- **Engagement metrics**: Views, likes, dislikes, comments statistics
- **Data quality**: Missing values, duplicates, inconsistencies