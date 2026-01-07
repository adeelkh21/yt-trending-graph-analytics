# Phase 3: Exploratory Data Analysis (EDA)

## Overview
This phase performs comprehensive exploratory data analysis on the cleaned YouTube Trending Videos dataset.

## Prerequisites
- Phase 2 must be completed
- `youtube_trending_cleaned.csv` must be present
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

### 2. Run Phase 3 EDA
```bash
python phase3_eda.py
```

## What Phase 3 Does

### 1. Summary Statistics
- Computes basic statistics (mean, median, mode, std, min, max) for numeric columns
- Computes country-wise statistics
- Identifies top categories per country
- Identifies top channels per country

### 2. Distribution Analysis
- Creates histograms and boxplots for numeric variables
- Analyzes distributions by country
- Creates bar charts for top categories and channels

### 3. Trend Analysis Over Time
- Plots number of trending videos per day
- Analyzes category trends over time
- Identifies day-of-week patterns
- Computes correlation matrices

### 4. Correlation Analysis
- Creates correlation heatmaps
- Generates scatter plots
- Analyzes relationships between variables

### 5. Tag Analysis
- Counts most common tags
- Creates tag distribution charts
- Analyzes tags per country

### 6. Output & Reporting
- Saves summary statistics as CSV
- Saves all visualizations as PNG files
- Generates comprehensive EDA report

## Expected Output Files

1. **phase3_summary_statistics.csv** - Comprehensive summary statistics
2. **phase3_eda_report.md** - Detailed EDA report
3. **phase3_visualizations/** - Directory containing all visualizations:
   - `distributions/` - Distribution charts
   - `country_wise/` - Country-specific analysis
   - `trends/` - Trend analysis charts
   - `correlations/` - Correlation analysis
   - `channels/` - Channel analysis

## Key Visualizations Generated

### Distribution Charts
- Numeric variable distributions (histograms)
- Boxplots for all numeric variables
- Country-wise distributions

### Country Analysis
- Top categories by video count
- Top categories by average views
- Top channels by total views
- Country comparison charts

### Trend Analysis
- Daily trending videos over time
- Category trends over time (weekly)
- Day-of-week patterns
- Peak trending days

### Correlation Analysis
- Correlation heatmaps (overall and country-wise)
- Scatter plots (views vs likes, comments, engagement ratios)

### Tag Analysis
- Top 20 tags across all videos
- Top 20 tags per country

## Key Insights Generated

1. **Top Categories**: Most popular categories per country
2. **Top Channels**: Channels with highest views and engagement
3. **Trending Patterns**: Day-of-week and temporal patterns
4. **Correlations**: Relationships between engagement metrics
5. **Tag Distribution**: Most common tags and their distribution

## Next Steps

After completing Phase 3, proceed to:
- **Phase 4**: Graph Database Setup and Data Ingestion
- Use insights from EDA to guide graph schema design

## Troubleshooting

### Common Issues

1. **Memory Error**: If dataset is too large, process countries separately
2. **Visualization Errors**: Check matplotlib/seaborn installation
3. **Tags Parsing**: Tags are stored as strings in CSV, parsed automatically

## Performance Notes

- Processing time: ~5-10 minutes depending on system
- Memory usage: ~1-2GB
- Output file size: ~100-200MB (visualizations)

