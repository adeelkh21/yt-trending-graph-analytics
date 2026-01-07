# Phase 2: Quick Reference Guide

## Quick Start

```bash
# Activate virtual environment
venv\Scripts\activate

# Run preprocessing
python phase2_preprocessing.py
```

## Output Files

1. **youtube_trending_cleaned.csv** - Main cleaned dataset
2. **phase2_preprocessing_report.txt** - Summary report
3. **phase2_preprocessing.py** - Preprocessing script

## Key Changes Made

### Data Reduction
- **Original**: 158,098 rows
- **Final**: 50,357 rows
- **Reduction**: 68.15% (duplicate removal)

### New Columns (14 added)
- Date components: `publish_year`, `publish_month`, `publish_day`, `publish_day_of_week`
- Date components: `trending_year`, `trending_month`, `trending_day`, `trending_day_of_week`
- `days_to_trend` - Days between publish and trending
- `category_name` - Category name from JSON mapping
- `tags_list` - Parsed tags as list (string in CSV)
- `tags_count` - Number of tags per video
- `engagement_ratio` - (likes + comments) / views
- `like_dislike_ratio` - likes / dislikes

## Data Quality Improvements

✅ **Missing Values**: All filled
✅ **Duplicates**: All removed (0 remaining)
✅ **Outliers**: Capped at 99th percentile
✅ **Zero Values**: Replaced with 1 for ratios
✅ **Text Fields**: Cleaned and normalized
✅ **Dates**: Normalized and parsed

## Loading the Cleaned Dataset

```python
import pandas as pd
import ast

# Load cleaned dataset
df = pd.read_csv('youtube_trending_cleaned.csv')

# Parse tags_list back to Python list (if needed)
df['tags_list'] = df['tags_list'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
```

## Statistics Summary

### After Cleaning
- **Mean views**: 1,064,764
- **Mean likes**: 28,141
- **Mean dislikes**: 1,293
- **Mean comments**: 3,076
- **Average tags**: 19.1 per video

### Rows per Country
- CA: 24,427
- GB: 3,272
- IN: 16,307
- US: 6,351

## Next Steps

1. **Phase 3**: Exploratory Data Analysis (EDA)
2. **Phase 4**: Graph Database Setup and Ingestion
3. **Phase 5**: Query Development

## Important Notes

1. **Tags List**: Stored as string in CSV. Parse using `ast.literal_eval()` when loading.

2. **Duplicate Removal**: Videos appearing multiple times are consolidated to one entry per video_id per country.

3. **Outlier Capping**: Values capped at 99th percentile may affect analysis of top performers.

4. **Timezone**: All dates are timezone-naive for easier comparison.

## Validation Results

✅ All validation checks passed:
- No duplicates
- All numeric fields >= 0
- All categorical fields valid
- Date components consistent

---

**Status**: ✅ Phase 2 Complete
**Ready for**: Phase 3 (EDA)

