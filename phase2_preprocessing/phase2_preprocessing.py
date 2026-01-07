"""
Phase 2: Data Preprocessing and Cleaning
YouTube Trending Videos Dataset Analysis
"""

import pandas as pd
import numpy as np
import json
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# STEP 1: Load Data
# ============================================================================

print("=" * 80)
print("PHASE 2: DATA PREPROCESSING AND CLEANING")
print("=" * 80)

print("\n[1] Loading Data...")
print("-" * 80)

# Load CSV files
try:
    df_us = pd.read_csv('USvideos.csv')
    df_gb = pd.read_csv('GBvideos.csv')
    df_ca = pd.read_csv('CAvideos.csv')
    df_in = pd.read_csv('INvideos.csv')
    print("✓ Successfully loaded all CSV files")
except FileNotFoundError as e:
    print(f"✗ Error loading files: {e}")
    exit(1)

# Add country column
df_us['country'] = 'US'
df_gb['country'] = 'GB'
df_ca['country'] = 'CA'
df_in['country'] = 'IN'

# Combine all dataframes
df = pd.concat([df_us, df_gb, df_ca, df_in], ignore_index=True)
print(f"✓ Combined dataset: {len(df):,} rows")

# Track original row count
original_rows = len(df)

# ============================================================================
# STEP 2: Load Category Mappings
# ============================================================================

print("\n[2] Loading Category Mappings...")
print("-" * 80)

def load_category_mapping(country_code):
    """Load and parse category JSON file"""
    filename = f'{country_code}_category_id.json'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        category_map = {}
        if 'items' in data:
            for item in data['items']:
                cat_id = item.get('id')
                cat_title = item.get('snippet', {}).get('title', 'Unknown')
                category_map[int(cat_id)] = cat_title
        
        return category_map
    except FileNotFoundError:
        print(f"  ⚠ Warning: {filename} not found")
        return {}
    except json.JSONDecodeError as e:
        print(f"  ✗ Error parsing {filename}: {e}")
        return {}

category_mappings = {}
for country in ['US', 'GB', 'CA', 'IN']:
    category_mappings[country] = load_category_mapping(country)
    print(f"  {country}: {len(category_mappings[country])} categories loaded")

# ============================================================================
# STEP 3: Handle Missing Values
# ============================================================================

print("\n[3] Handling Missing Values...")
print("-" * 80)

# Track missing values before handling
missing_before = df.isnull().sum()

# Fill missing description values
missing_descriptions = df['description'].isnull().sum()
df['description'] = df['description'].fillna('No description')
print(f"✓ Filled {missing_descriptions:,} missing descriptions with 'No description'")

# Check critical columns for missing values
critical_columns = ['views', 'likes', 'dislikes', 'comment_count', 'category_id', 
                   'publish_time', 'trending_date', 'video_id', 'title', 'channel_title']

missing_critical = df[critical_columns].isnull().sum()
if missing_critical.sum() > 0:
    print(f"⚠ Found missing values in critical columns:")
    print(missing_critical[missing_critical > 0])
    # Drop rows with missing critical values
    rows_before = len(df)
    df = df.dropna(subset=critical_columns)
    rows_after = len(df)
    print(f"✓ Dropped {rows_before - rows_after:,} rows with missing critical values")
else:
    print("✓ No missing values in critical columns")

# ============================================================================
# STEP 4: Parse Dates
# ============================================================================

print("\n[4] Parsing and Normalizing Dates...")
print("-" * 80)

def parse_trending_date(date_str):
    """Parse trending date format: YY.DD.MM"""
    try:
        parts = date_str.split('.')
        if len(parts) == 3:
            year = int(parts[0]) + 2000
            day = int(parts[1])
            month = int(parts[2])
            return pd.Timestamp(year, month, day)
    except:
        return None

def parse_publish_time(time_str):
    """Parse publish time ISO format"""
    try:
        return pd.to_datetime(time_str)
    except:
        return None

# Parse dates
df['trending_date_parsed'] = df['trending_date'].apply(parse_trending_date)
df['publish_time_parsed'] = df['publish_time'].apply(parse_publish_time)

# Drop rows where date parsing failed
date_parse_failures = df['trending_date_parsed'].isnull().sum() + df['publish_time_parsed'].isnull().sum()
if date_parse_failures > 0:
    df = df.dropna(subset=['trending_date_parsed', 'publish_time_parsed'])
    print(f"✓ Dropped {date_parse_failures:,} rows with invalid dates")

# Convert to datetime
# Parse publish_time with UTC timezone, then convert to naive
df['publish_time'] = pd.to_datetime(df['publish_time_parsed'], utc=True)
df['publish_time'] = df['publish_time'].dt.tz_convert(None)  # Convert to timezone-naive

# Parse trending_date as timezone-naive (it doesn't have timezone info)
df['trending_date'] = pd.to_datetime(df['trending_date_parsed'])

df = df.drop(columns=['trending_date_parsed', 'publish_time_parsed'])

# Extract date components
df['publish_year'] = df['publish_time'].dt.year
df['publish_month'] = df['publish_time'].dt.month
df['publish_day'] = df['publish_time'].dt.day
df['publish_day_of_week'] = df['publish_time'].dt.day_name()

df['trending_year'] = df['trending_date'].dt.year
df['trending_month'] = df['trending_date'].dt.month
df['trending_day'] = df['trending_date'].dt.day
df['trending_day_of_week'] = df['trending_date'].dt.day_name()

# Calculate days to trend
df['days_to_trend'] = (df['trending_date'] - df['publish_time']).dt.days
# Handle negative values (should not happen, but just in case)
df['days_to_trend'] = df['days_to_trend'].clip(lower=0)

print("✓ Dates parsed and date components extracted")
print(f"✓ Calculated days_to_trend (range: {df['days_to_trend'].min()} to {df['days_to_trend'].max()} days)")

# ============================================================================
# STEP 5: Merge Category Mappings
# ============================================================================

print("\n[5] Merging Category Mappings...")
print("-" * 80)

def get_category_name(row):
    """Get category name from mapping based on country and category_id"""
    country = row['country']
    category_id = int(row['category_id'])
    
    if country in category_mappings:
        return category_mappings[country].get(category_id, f'Unknown ({category_id})')
    return f'Category {category_id}'

df['category_name'] = df.apply(get_category_name, axis=1)
print("✓ Category names merged successfully")

# ============================================================================
# STEP 6: Handle Zero/Negative Values
# ============================================================================

print("\n[6] Handling Zero/Negative Values...")
print("-" * 80)

# Ensure all numeric fields are >= 0
numeric_cols = ['views', 'likes', 'dislikes', 'comment_count']
for col in numeric_cols:
    negative_count = (df[col] < 0).sum()
    if negative_count > 0:
        df[col] = df[col].clip(lower=0)
        print(f"✓ Clipped {negative_count:,} negative values in {col} to 0")

# Replace zeros in likes, dislikes, comment_count with 1 for safe ratio calculations
zero_replacements = {
    'likes': (df['likes'] == 0).sum(),
    'dislikes': (df['dislikes'] == 0).sum(),
    'comment_count': (df['comment_count'] == 0).sum()
}

df['likes'] = df['likes'].replace(0, 1)
df['dislikes'] = df['dislikes'].replace(0, 1)
df['comment_count'] = df['comment_count'].replace(0, 1)

for col, count in zero_replacements.items():
    if count > 0:
        print(f"✓ Replaced {count:,} zeros in {col} with 1")

# ============================================================================
# STEP 7: Handle Outliers
# ============================================================================

print("\n[7] Handling Outliers...")
print("-" * 80)

def cap_outliers(series, percentile=99):
    """Cap outliers at specified percentile"""
    cap_value = series.quantile(percentile / 100)
    outliers_count = (series > cap_value).sum()
    series_capped = series.clip(upper=cap_value)
    return series_capped, outliers_count, cap_value

# Apply capping at 99th percentile
for col in numeric_cols:
    original_max = df[col].max()
    df[col], outliers_count, cap_value = cap_outliers(df[col], percentile=99)
    if outliers_count > 0:
        print(f"✓ Capped {outliers_count:,} outliers in {col} at {cap_value:,.0f} (was {original_max:,.0f})")

# ============================================================================
# STEP 8: Text Cleaning
# ============================================================================

print("\n[8] Cleaning Text Fields...")
print("-" * 80)

def clean_text(text):
    """Clean text: remove special characters, extra whitespace, HTML entities"""
    if pd.isna(text) or text == '':
        return text
    
    text = str(text)
    
    # Remove HTML entities
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    text = re.sub(r'&#\d+;', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def parse_tags(tags_str):
    """Parse pipe-separated tags into a list"""
    if pd.isna(tags_str) or tags_str == '' or tags_str == '[none]':
        return []
    
    tags_str = str(tags_str)
    # Split by pipe
    tags = [tag.strip() for tag in tags_str.split('|')]
    # Remove empty tags
    tags = [tag for tag in tags if tag and tag.lower() != 'none']
    return tags

# Clean text fields
text_columns = ['title', 'description', 'channel_title']
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].apply(clean_text)
        print(f"✓ Cleaned {col}")

# Parse tags
df['tags_list'] = df['tags'].apply(parse_tags)
df['tags_count'] = df['tags_list'].apply(len)

# Clean tags column (keep original for reference, but also store cleaned version)
df['tags_cleaned'] = df['tags'].apply(clean_text)

print(f"✓ Parsed tags into lists (average {df['tags_count'].mean():.1f} tags per video)")

# ============================================================================
# STEP 9: Handle Duplicates
# ============================================================================

print("\n[9] Handling Duplicates...")
print("-" * 80)

# Track duplicates before handling
duplicates_before = df.duplicated(subset=['video_id', 'country'], keep=False).sum()
print(f"  Found {duplicates_before:,} duplicate video_id entries within countries")

# Sort by trending_date (latest first) to keep most recent trending occurrence
df = df.sort_values(['country', 'video_id', 'trending_date'], ascending=[True, True, False])

# For duplicates within same country, keep the latest (first after sorting)
# Aggregate engagement metrics: use max values
agg_dict = {
    'views': 'max',
    'likes': 'max',
    'dislikes': 'max',
    'comment_count': 'max',
    'title': 'first',
    'channel_title': 'first',
    'category_id': 'first',
    'category_name': 'first',
    'publish_time': 'first',
    'trending_date': 'first',  # Keep the latest trending date
    'tags': 'first',
    'tags_list': 'first',
    'tags_cleaned': 'first',
    'tags_count': 'first',
    'thumbnail_link': 'first',
    'comments_disabled': 'first',
    'ratings_disabled': 'first',
    'video_error_or_removed': 'first',
    'description': 'first',
    'publish_year': 'first',
    'publish_month': 'first',
    'publish_day': 'first',
    'publish_day_of_week': 'first',
    'trending_year': 'first',
    'trending_month': 'first',
    'trending_day': 'first',
    'trending_day_of_week': 'first',
    'days_to_trend': 'first'
}

# Group by video_id and country, aggregate
df_deduplicated = df.groupby(['video_id', 'country'], as_index=False).agg(agg_dict)

rows_after_dedup = len(df_deduplicated)
rows_removed = len(df) - rows_after_dedup

df = df_deduplicated
print(f"✓ Removed {rows_removed:,} duplicate rows")
print(f"✓ Kept latest trending occurrence for each video_id per country")
print(f"✓ Aggregated engagement metrics (using max values)")

# ============================================================================
# STEP 10: Create Derived Fields
# ============================================================================

print("\n[10] Creating Derived Fields...")
print("-" * 80)

# Engagement ratio
df['engagement_ratio'] = ((df['likes'] + df['comment_count']) / df['views']).round(2)
# Handle infinite values
df['engagement_ratio'] = df['engagement_ratio'].replace([np.inf, -np.inf], 0)

# Like-dislike ratio
df['like_dislike_ratio'] = (df['likes'] / df['dislikes']).round(2)
# Handle infinite values
df['like_dislike_ratio'] = df['like_dislike_ratio'].replace([np.inf, -np.inf], 0)

print("✓ Created engagement_ratio")
print("✓ Created like_dislike_ratio")

# ============================================================================
# STEP 11: Data Validation
# ============================================================================

print("\n[11] Data Validation...")
print("-" * 80)

# Check for remaining duplicates
remaining_duplicates = df.duplicated(subset=['video_id', 'country'], keep=False).sum()
if remaining_duplicates == 0:
    print("✓ No duplicates remaining (video_id per country)")
else:
    print(f"⚠ Warning: {remaining_duplicates:,} duplicates still exist")

# Validate numeric fields
numeric_validation = (df[numeric_cols] >= 0).all().all()
if numeric_validation:
    print("✓ All numeric fields are >= 0")
else:
    print("⚠ Warning: Some numeric fields have negative values")

# Validate categorical fields
category_validation = df['category_name'].notna().all()
if category_validation:
    print("✓ All category names are valid")
else:
    print("⚠ Warning: Some category names are missing")

# Validate countries
valid_countries = ['US', 'GB', 'CA', 'IN']
country_validation = df['country'].isin(valid_countries).all()
if country_validation:
    print("✓ All countries are valid")
else:
    print("⚠ Warning: Some invalid countries found")

# Validate date components
date_validation = (
    (df['publish_year'] >= 2000) & (df['publish_year'] <= 2020) &
    (df['trending_year'] >= 2017) & (df['trending_year'] <= 2018)
).all()

if date_validation:
    print("✓ Date components are consistent")
else:
    print("⚠ Warning: Some date components are inconsistent")

# ============================================================================
# STEP 12: Prepare Final Dataset
# ============================================================================

print("\n[12] Preparing Final Dataset...")
print("-" * 80)

# Select and reorder columns for final output
final_columns = [
    'video_id', 'trending_date', 'title', 'channel_title', 'category_id', 
    'category_name', 'publish_time', 'tags', 'tags_list', 'tags_count', 
    'views', 'likes', 'dislikes', 'comment_count', 'thumbnail_link',
    'comments_disabled', 'ratings_disabled', 'video_error_or_removed', 
    'description', 'country',
    'publish_year', 'publish_month', 'publish_day', 'publish_day_of_week',
    'trending_year', 'trending_month', 'trending_day', 'trending_day_of_week',
    'days_to_trend', 'engagement_ratio', 'like_dislike_ratio'
]

# Ensure all columns exist
existing_columns = [col for col in final_columns if col in df.columns]
df_final = df[existing_columns].copy()

print(f"✓ Final dataset prepared with {len(df_final.columns)} columns")

# ============================================================================
# STEP 13: Generate Summary Statistics
# ============================================================================

print("\n[13] Generating Summary Statistics...")
print("-" * 80)

# Rows per country
rows_per_country = df_final['country'].value_counts().sort_index()
print("\nRows per country after cleaning:")
for country, count in rows_per_country.items():
    print(f"  {country}: {count:,}")

# Basic statistics
print("\nBasic Statistics (after cleaning):")
stats = df_final[numeric_cols].describe()
print(stats)

# ============================================================================
# STEP 14: Save Outputs
# ============================================================================

print("\n[14] Saving Outputs...")
print("-" * 80)

# Save cleaned dataset
output_file = 'youtube_trending_cleaned.csv'
df_final.to_csv(output_file, index=False)
print(f"✓ Saved cleaned dataset to {output_file}")

# Generate summary report
summary_report = f"""
PHASE 2: DATA PREPROCESSING SUMMARY REPORT
{'=' * 80}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ORIGINAL DATASET:
- Total rows: {original_rows:,}
- Countries: 4 (US, GB, CA, IN)

DATA CLEANING OPERATIONS:
1. Missing Values:
   - Missing descriptions filled: {missing_descriptions:,}
   - Rows dropped due to missing critical values: {missing_before.sum() - df_final.isnull().sum().sum():,}

2. Duplicates:
   - Duplicate video_id entries found: {duplicates_before:,}
   - Rows removed: {rows_removed:,}
   - Remaining duplicates: {remaining_duplicates:,}

3. Zero/Negative Values:
   - Zeros replaced in likes: {zero_replacements['likes']:,}
   - Zeros replaced in dislikes: {zero_replacements['dislikes']:,}
   - Zeros replaced in comment_count: {zero_replacements['comment_count']:,}

4. Outliers:
   - Capped at 99th percentile for all numeric fields

5. Text Cleaning:
   - Title, description, channel_title cleaned
   - Tags parsed into lists
   - Average tags per video: {df_final['tags_count'].mean():.1f}

6. Date Normalization:
   - Dates parsed and converted to datetime
   - Date components extracted
   - Days to trend calculated

7. Category Mappings:
   - Category names merged successfully
   - Country-specific mappings applied

8. Derived Fields:
   - engagement_ratio created
   - like_dislike_ratio created

FINAL DATASET:
- Total rows: {len(df_final):,}
- Total columns: {len(df_final.columns)}
- Rows removed: {original_rows - len(df_final):,} ({(original_rows - len(df_final))/original_rows*100:.2f}%)

ROWS PER COUNTRY (After Cleaning):
{rows_per_country.to_string()}

BASIC STATISTICS (After Cleaning):
{stats.to_string()}

DATA VALIDATION:
- Duplicates: {'✓ PASS' if remaining_duplicates == 0 else '✗ FAIL'}
- Numeric fields >= 0: {'✓ PASS' if numeric_validation else '✗ FAIL'}
- Category names valid: {'✓ PASS' if category_validation else '✗ FAIL'}
- Countries valid: {'✓ PASS' if country_validation else '✗ FAIL'}
- Date components consistent: {'✓ PASS' if date_validation else '✗ FAIL'}

{'=' * 80}
"""

# Save summary report
report_file = 'phase2_preprocessing_report.txt'
with open(report_file, 'w', encoding='utf-8') as f:
    f.write(summary_report)
print(f"✓ Saved summary report to {report_file}")

# Print summary
print(summary_report)

print("\n" + "=" * 80)
print("PHASE 2 COMPLETED SUCCESSFULLY!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  1. {output_file}")
print(f"  2. {report_file}")
print(f"  3. phase2_preprocessing.py (this script)")

