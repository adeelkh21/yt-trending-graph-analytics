"""
Phase 3: Exploratory Data Analysis (EDA)
YouTube Trending Videos Dataset Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import ast
import os
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        plt.style.use('ggplot')
sns.set_palette("husl")

# Create output directory for visualizations
os.makedirs('phase3_visualizations', exist_ok=True)
os.makedirs('phase3_visualizations/country_wise', exist_ok=True)
os.makedirs('phase3_visualizations/distributions', exist_ok=True)
os.makedirs('phase3_visualizations/trends', exist_ok=True)
os.makedirs('phase3_visualizations/correlations', exist_ok=True)
os.makedirs('phase3_visualizations/channels', exist_ok=True)

print("=" * 80)
print("PHASE 3: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 80)

# ============================================================================
# STEP 1: Load Cleaned Dataset
# ============================================================================

print("\n[1] Loading Cleaned Dataset...")
print("-" * 80)

try:
    df = pd.read_csv('youtube_trending_cleaned.csv')
    print(f"✓ Loaded cleaned dataset: {len(df):,} rows, {len(df.columns)} columns")
except FileNotFoundError:
    print("✗ Error: youtube_trending_cleaned.csv not found. Please run Phase 2 first.")
    exit(1)

# Parse dates
df['trending_date'] = pd.to_datetime(df['trending_date'])
df['publish_time'] = pd.to_datetime(df['publish_time'])

# Parse tags_list if it's a string
def parse_tags_safe(x):
    if pd.isna(x) or x == '' or x == '[]':
        return []
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        try:
            # Try to parse as list
            if x.startswith('[') and x.endswith(']'):
                return ast.literal_eval(x)
            else:
                return [x]
        except:
            return []
    return []

if df['tags_list'].dtype == 'object':
    df['tags_list'] = df['tags_list'].apply(parse_tags_safe)

# Define numeric columns for analysis
numeric_cols = ['views', 'likes', 'dislikes', 'comment_count', 'engagement_ratio', 'like_dislike_ratio']

print(f"✓ Dataset loaded successfully")
print(f"  Countries: {df['country'].unique()}")
print(f"  Date range: {df['trending_date'].min()} to {df['trending_date'].max()}")

# ============================================================================
# STEP 2: Summary Statistics
# ============================================================================

print("\n[2] Computing Summary Statistics...")
print("-" * 80)

# Basic statistics for numeric columns
summary_stats = df[numeric_cols].describe()

# Calculate mode (handle cases where mode doesn't exist)
mode_values = []
for col in numeric_cols:
    mode_result = df[col].mode()
    if len(mode_result) > 0:
        mode_values.append(mode_result.iloc[0])
    else:
        mode_values.append(np.nan)
summary_stats.loc['mode'] = mode_values

print("\nOverall Summary Statistics:")
print(summary_stats)

# Country-wise statistics
country_stats = []

for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    
    stats = {
        'country': country,
        'num_videos': len(df_country),
        'avg_views': df_country['views'].mean(),
        'avg_likes': df_country['likes'].mean(),
        'avg_dislikes': df_country['dislikes'].mean(),
        'avg_comments': df_country['comment_count'].mean(),
        'avg_engagement_ratio': df_country['engagement_ratio'].mean(),
        'avg_like_dislike_ratio': df_country['like_dislike_ratio'].mean(),
        'median_views': df_country['views'].median(),
        'median_likes': df_country['likes'].median(),
        'std_views': df_country['views'].std(),
        'std_likes': df_country['likes'].std(),
        'max_views': df_country['views'].max(),
        'max_likes': df_country['likes'].max()
    }
    country_stats.append(stats)

country_stats_df = pd.DataFrame(country_stats)
print("\nCountry-wise Statistics:")
print(country_stats_df)

# Top 5 categories per country by video count
print("\nTop 5 Categories by Video Count per Country:")
top_categories_count = {}
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    top_cats = df_country['category_name'].value_counts().head(5)
    top_categories_count[country] = top_cats
    print(f"\n{country}:")
    print(top_cats)

# Top 5 categories per country by average views
print("\nTop 5 Categories by Average Views per Country:")
top_categories_views = {}
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    cat_views = df_country.groupby('category_name')['views'].mean().sort_values(ascending=False).head(5)
    top_categories_views[country] = cat_views
    print(f"\n{country}:")
    print(cat_views)

# Top channels per country by total views
print("\nTop 10 Channels by Total Views per Country:")
top_channels_views = {}
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    channel_views = df_country.groupby('channel_title')['views'].sum().sort_values(ascending=False).head(10)
    top_channels_views[country] = channel_views
    print(f"\n{country}:")
    print(channel_views)

# Top channels per country by total engagement ratio
print("\nTop 10 Channels by Average Engagement Ratio per Country:")
top_channels_engagement = {}
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    channel_eng = df_country.groupby('channel_title')['engagement_ratio'].mean().sort_values(ascending=False).head(10)
    top_channels_engagement[country] = channel_eng
    print(f"\n{country}:")
    print(channel_eng)

# ============================================================================
# STEP 3: Distribution Analysis
# ============================================================================

print("\n[3] Creating Distribution Visualizations...")
print("-" * 80)

# Histograms and boxplots for numeric columns
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Distribution of Numeric Variables', fontsize=16, fontweight='bold')

for idx, col in enumerate(numeric_cols):
    row = idx // 3
    col_idx = idx % 3
    ax = axes[row, col_idx]
    
    # Histogram
    df[col].hist(bins=50, ax=ax, alpha=0.7, edgecolor='black')
    ax.set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('phase3_visualizations/distributions/numeric_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved numeric distributions histogram")

# Boxplots for numeric columns
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Boxplots of Numeric Variables', fontsize=16, fontweight='bold')

for idx, col in enumerate(numeric_cols):
    row = idx // 3
    col_idx = idx % 3
    ax = axes[row, col_idx]
    
    df.boxplot(column=col, ax=ax)
    ax.set_title(f'Boxplot of {col}', fontsize=12, fontweight='bold')
    ax.set_ylabel(col)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('phase3_visualizations/distributions/numeric_boxplots.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved numeric boxplots")

# Country-wise boxplots for views
plt.figure(figsize=(14, 8))
df.boxplot(column='views', by='country', ax=plt.gca())
plt.title('Views Distribution by Country', fontsize=14, fontweight='bold')
plt.suptitle('')  # Remove default title
plt.xlabel('Country')
plt.ylabel('Views')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('phase3_visualizations/distributions/views_by_country_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved views by country boxplot")

# Top 10 categories by video count per country
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    top_cats = df_country['category_name'].value_counts().head(10)
    
    plt.figure(figsize=(12, 8))
    top_cats.plot(kind='barh')
    plt.title(f'Top 10 Categories by Video Count - {country}', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Videos')
    plt.ylabel('Category')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f'phase3_visualizations/country_wise/top_categories_count_{country}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved top categories by count for {country}")

# Top 10 categories by average views per country
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    cat_views = df_country.groupby('category_name')['views'].mean().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(12, 8))
    cat_views.plot(kind='barh')
    plt.title(f'Top 10 Categories by Average Views - {country}', fontsize=14, fontweight='bold')
    plt.xlabel('Average Views')
    plt.ylabel('Category')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f'phase3_visualizations/country_wise/top_categories_views_{country}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved top categories by views for {country}")

# Top 10 channels per country by total views
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    channel_views = df_country.groupby('channel_title')['views'].sum().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(12, 8))
    channel_views.plot(kind='barh')
    plt.title(f'Top 10 Channels by Total Views - {country}', fontsize=14, fontweight='bold')
    plt.xlabel('Total Views')
    plt.ylabel('Channel')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f'phase3_visualizations/channels/top_channels_views_{country}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved top channels by views for {country}")

# ============================================================================
# STEP 4: Trend Analysis Over Time
# ============================================================================

print("\n[4] Creating Trend Analysis Visualizations...")
print("-" * 80)

# Number of trending videos per day for each country
plt.figure(figsize=(16, 10))
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    daily_trends = df_country.groupby('trending_date').size()
    plt.plot(daily_trends.index, daily_trends.values, label=country, linewidth=2, marker='o', markersize=3)

plt.title('Number of Trending Videos Per Day by Country', fontsize=16, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Number of Trending Videos')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('phase3_visualizations/trends/daily_trending_videos.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved daily trending videos chart")

# Category trends over time (weekly aggregation)
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    # Get top 5 categories
    top_cats = df_country['category_name'].value_counts().head(5).index
    
    # Group by week and category
    df_country['trending_week'] = df_country['trending_date'].dt.to_period('W')
    weekly_cat_trends = df_country[df_country['category_name'].isin(top_cats)].groupby(['trending_week', 'category_name']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(16, 10))
    for cat in top_cats:
        if cat in weekly_cat_trends.columns:
            plt.plot(range(len(weekly_cat_trends)), weekly_cat_trends[cat], label=cat, linewidth=2, marker='o', markersize=3)
    
    plt.title(f'Category Trends Over Time (Weekly) - {country}', fontsize=14, fontweight='bold')
    plt.xlabel('Week')
    plt.ylabel('Number of Trending Videos')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'phase3_visualizations/trends/category_trends_{country}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved category trends for {country}")

# Day-of-week patterns
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['trending_day_of_week'] = pd.Categorical(df['trending_day_of_week'], categories=day_order, ordered=True)

day_stats = df.groupby(['country', 'trending_day_of_week']).agg({
    'views': 'mean',
    'likes': 'mean',
    'comment_count': 'mean',
    'engagement_ratio': 'mean'
}).reset_index()

# Plot day-of-week patterns
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Day-of-Week Patterns by Country', fontsize=16, fontweight='bold')

metrics = ['views', 'likes', 'comment_count', 'engagement_ratio']
for idx, metric in enumerate(metrics):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]
    
    for country in ['US', 'GB', 'CA', 'IN']:
        country_data = day_stats[day_stats['country'] == country]
        ax.plot(country_data['trending_day_of_week'], country_data[metric], marker='o', label=country, linewidth=2)
    
    ax.set_title(f'Average {metric.title()} by Day of Week', fontsize=12, fontweight='bold')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel(metric.title())
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('phase3_visualizations/trends/day_of_week_patterns.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved day-of-week patterns chart")

# Peak trending days
peak_days = df.groupby(['country', 'trending_day_of_week']).size().reset_index(name='count')
peak_days = peak_days.sort_values(['country', 'count'], ascending=[True, False])

print("\nPeak Trending Days by Country:")
for country in ['US', 'GB', 'CA', 'IN']:
    country_peak = peak_days[peak_days['country'] == country].head(1)
    if len(country_peak) > 0:
        print(f"  {country}: {country_peak['trending_day_of_week'].values[0]} ({country_peak['count'].values[0]} videos)")

# ============================================================================
# STEP 5: Correlation Analysis
# ============================================================================

print("\n[5] Computing Correlation Analysis...")
print("-" * 80)

# Correlation matrix
corr_matrix = df[numeric_cols].corr()

# Heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Numeric Variables', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('phase3_visualizations/correlations/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved correlation heatmap")

# Country-wise correlation matrices
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    corr_matrix_country = df_country[numeric_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix_country, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title(f'Correlation Matrix - {country}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'phase3_visualizations/correlations/correlation_heatmap_{country}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved correlation heatmap for {country}")

# Scatter plots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Scatter Plots: Relationships Between Variables', fontsize=16, fontweight='bold')

# views vs likes
axes[0, 0].scatter(df['views'], df['likes'], alpha=0.5, s=10)
axes[0, 0].set_xlabel('Views')
axes[0, 0].set_ylabel('Likes')
axes[0, 0].set_title('Views vs Likes')
axes[0, 0].grid(True, alpha=0.3)

# views vs comment_count
axes[0, 1].scatter(df['views'], df['comment_count'], alpha=0.5, s=10)
axes[0, 1].set_xlabel('Views')
axes[0, 1].set_ylabel('Comment Count')
axes[0, 1].set_title('Views vs Comment Count')
axes[0, 1].grid(True, alpha=0.3)

# engagement_ratio vs views
axes[1, 0].scatter(df['views'], df['engagement_ratio'], alpha=0.5, s=10)
axes[1, 0].set_xlabel('Views')
axes[1, 0].set_ylabel('Engagement Ratio')
axes[1, 0].set_title('Engagement Ratio vs Views')
axes[1, 0].grid(True, alpha=0.3)

# like_dislike_ratio vs views
axes[1, 1].scatter(df['views'], df['like_dislike_ratio'], alpha=0.5, s=10)
axes[1, 1].set_xlabel('Views')
axes[1, 1].set_ylabel('Like-Dislike Ratio')
axes[1, 1].set_title('Like-Dislike Ratio vs Views')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('phase3_visualizations/correlations/scatter_plots.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved scatter plots")

# ============================================================================
# STEP 6: Tag Analysis
# ============================================================================

print("\n[6] Performing Tag Analysis...")
print("-" * 80)

# Count most common tags across all videos
all_tags = []
for tags_list in df['tags_list']:
    if isinstance(tags_list, list):
        all_tags.extend(tags_list)

tag_counts = Counter(all_tags)
top_tags = tag_counts.most_common(20)

# Top 20 tags bar chart
if len(top_tags) > 0:
    tags_df = pd.DataFrame(top_tags, columns=['tag', 'count'])
    tags_df = tags_df.sort_values('count', ascending=True)
    
    plt.figure(figsize=(12, 10))
    plt.barh(range(len(tags_df)), tags_df['count'])
    plt.yticks(range(len(tags_df)), tags_df['tag'])
    plt.xlabel('Count')
    plt.ylabel('Tag')
    plt.title('Top 20 Most Common Tags Across All Videos', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('phase3_visualizations/top_tags_all.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved top tags chart")

# Top tags per country
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    country_tags = []
    for tags_list in df_country['tags_list']:
        if isinstance(tags_list, list):
            country_tags.extend(tags_list)
    
    if len(country_tags) > 0:
        country_tag_counts = Counter(country_tags)
        top_country_tags = country_tag_counts.most_common(20)
        
        if len(top_country_tags) > 0:
            country_tags_df = pd.DataFrame(top_country_tags, columns=['tag', 'count'])
            country_tags_df = country_tags_df.sort_values('count', ascending=True)
            
            plt.figure(figsize=(12, 10))
            plt.barh(range(len(country_tags_df)), country_tags_df['count'])
            plt.yticks(range(len(country_tags_df)), country_tags_df['tag'])
            plt.xlabel('Count')
            plt.ylabel('Tag')
            plt.title(f'Top 20 Most Common Tags - {country}', fontsize=14, fontweight='bold')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(f'phase3_visualizations/country_wise/top_tags_{country}.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✓ Saved top tags for {country}")

# ============================================================================
# STEP 7: Save Summary Statistics
# ============================================================================

print("\n[7] Saving Summary Statistics...")
print("-" * 80)

# Create comprehensive summary statistics DataFrame
summary_data = []

# Overall statistics
for col in numeric_cols:
    mode_val = np.nan
    mode_result = df[col].mode()
    if len(mode_result) > 0:
        mode_val = mode_result.iloc[0]
    
    summary_data.append({
        'metric': col,
        'country': 'All',
        'mean': df[col].mean(),
        'median': df[col].median(),
        'mode': mode_val,
        'std': df[col].std(),
        'min': df[col].min(),
        'max': df[col].max(),
        'q25': df[col].quantile(0.25),
        'q75': df[col].quantile(0.75)
    })

# Country-wise statistics
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    for col in numeric_cols:
        mode_val = np.nan
        mode_result = df_country[col].mode()
        if len(mode_result) > 0:
            mode_val = mode_result.iloc[0]
        
        summary_data.append({
            'metric': col,
            'country': country,
            'mean': df_country[col].mean(),
            'median': df_country[col].median(),
            'mode': mode_val,
            'std': df_country[col].std(),
            'min': df_country[col].min(),
            'max': df_country[col].max(),
            'q25': df_country[col].quantile(0.25),
            'q75': df_country[col].quantile(0.75)
        })

summary_stats_df = pd.DataFrame(summary_data)
summary_stats_df.to_csv('phase3_summary_statistics.csv', index=False)
print("✓ Saved summary statistics to phase3_summary_statistics.csv")

# ============================================================================
# STEP 8: Generate EDA Report
# ============================================================================

print("\n[8] Generating EDA Report...")
print("-" * 80)

report = f"""
# Phase 3: Exploratory Data Analysis (EDA) Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. Dataset Overview

- **Total Videos**: {len(df):,}
- **Countries**: {', '.join(df['country'].unique())}
- **Date Range**: {df['trending_date'].min().strftime('%Y-%m-%d')} to {df['trending_date'].max().strftime('%Y-%m-%d')}
- **Categories**: {df['category_name'].nunique()} unique categories
- **Channels**: {df['channel_title'].nunique():,} unique channels

---

## 2. Summary Statistics

### 2.1 Overall Statistics

{summary_stats.to_string()}

### 2.2 Country-wise Statistics

{country_stats_df.to_string()}

### 2.3 Videos per Country

{df['country'].value_counts().to_string()}

---

## 3. Top Categories

### 3.1 Top 5 Categories by Video Count

"""

for country in ['US', 'GB', 'CA', 'IN']:
    report += f"\n**{country}:**\n"
    report += top_categories_count[country].to_string()
    report += "\n\n"

report += "\n### 3.2 Top 5 Categories by Average Views\n\n"

for country in ['US', 'GB', 'CA', 'IN']:
    report += f"**{country}:**\n"
    report += top_categories_views[country].to_string()
    report += "\n\n"

report += """
---

## 4. Top Channels

### 4.1 Top 10 Channels by Total Views

"""

for country in ['US', 'GB', 'CA', 'IN']:
    report += f"\n**{country}:**\n"
    report += top_channels_views[country].to_string()
    report += "\n\n"

report += "\n### 4.2 Top 10 Channels by Average Engagement Ratio\n\n"

for country in ['US', 'GB', 'CA', 'IN']:
    report += f"**{country}:**\n"
    report += top_channels_engagement[country].to_string()
    report += "\n\n"

report += f"""
---

## 5. Correlation Analysis

### 5.1 Correlation Matrix

{corr_matrix.to_string()}

### 5.2 Key Correlations

- Views vs Likes: {corr_matrix.loc['views', 'likes']:.3f}
- Views vs Comments: {corr_matrix.loc['views', 'comment_count']:.3f}
- Views vs Engagement Ratio: {corr_matrix.loc['views', 'engagement_ratio']:.3f}
- Likes vs Engagement Ratio: {corr_matrix.loc['likes', 'engagement_ratio']:.3f}

---

## 6. Day-of-Week Patterns

### 6.1 Peak Trending Days

"""

for country in ['US', 'GB', 'CA', 'IN']:
    country_peak = peak_days[peak_days['country'] == country].head(1)
    if len(country_peak) > 0:
        report += f"- **{country}**: {country_peak['trending_day_of_week'].values[0]} ({country_peak['count'].values[0]} videos)\n"

report += f"""
---

## 7. Key Insights

### 7.1 Engagement Patterns

- Average engagement ratio: {df['engagement_ratio'].mean():.3f}
- Average like-dislike ratio: {df['like_dislike_ratio'].mean():.3f}
- Videos with highest engagement: {df.loc[df['engagement_ratio'].idxmax(), 'title'][:50]}...

### 7.2 Category Insights

- Most popular category overall: {df['category_name'].value_counts().index[0]}
- Category with highest average views: {df.groupby('category_name')['views'].mean().idxmax()}
- Category with highest engagement: {df.groupby('category_name')['engagement_ratio'].mean().idxmax()}

### 7.3 Country Insights

- Country with most videos: {df['country'].value_counts().index[0]}
- Country with highest average views: {country_stats_df.loc[country_stats_df['avg_views'].idxmax(), 'country']}
- Country with highest engagement: {country_stats_df.loc[country_stats_df['avg_engagement_ratio'].idxmax(), 'country']}

---

## 8. Visualizations Generated

All visualizations have been saved in the `phase3_visualizations` directory:

- Distribution charts (histograms, boxplots)
- Country-wise analysis charts
- Trend analysis charts
- Correlation heatmaps
- Scatter plots
- Channel analysis charts
- Tag analysis charts

---

## 9. Files Generated

1. **phase3_summary_statistics.csv** - Comprehensive summary statistics
2. **phase3_visualizations/** - Directory containing all visualizations
3. **phase3_eda_report.md** - This report

---

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

# Save report
with open('phase3_eda_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✓ Saved EDA report to phase3_eda_report.md")

# ============================================================================
# STEP 9: Additional Visualizations
# ============================================================================

print("\n[9] Creating Additional Visualizations...")
print("-" * 80)

# Country comparison bar charts
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Country-wise Comparison', fontsize=16, fontweight='bold')

metrics_to_compare = ['views', 'likes', 'dislikes', 'comment_count', 'engagement_ratio', 'like_dislike_ratio']
for idx, metric in enumerate(metrics_to_compare):
    row = idx // 3
    col = idx % 3
    ax = axes[row, col]
    
    country_means = df.groupby('country')[metric].mean()
    country_means.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
    ax.set_title(f'Average {metric.title()} by Country', fontsize=12, fontweight='bold')
    ax.set_ylabel(metric.title())
    ax.set_xlabel('Country')
    ax.tick_params(axis='x', rotation=0)
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('phase3_visualizations/country_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved country comparison chart")

# Engagement ratio distribution by country
plt.figure(figsize=(14, 8))
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    plt.hist(df_country['engagement_ratio'], alpha=0.6, label=country, bins=50, edgecolor='black')

plt.title('Engagement Ratio Distribution by Country', fontsize=14, fontweight='bold')
plt.xlabel('Engagement Ratio')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('phase3_visualizations/distributions/engagement_ratio_by_country.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved engagement ratio distribution by country")

# Views distribution by country (log scale for better visualization)
plt.figure(figsize=(14, 8))
for country in ['US', 'GB', 'CA', 'IN']:
    df_country = df[df['country'] == country]
    plt.hist(np.log10(df_country['views'] + 1), alpha=0.6, label=country, bins=50, edgecolor='black')

plt.title('Views Distribution by Country (Log Scale)', fontsize=14, fontweight='bold')
plt.xlabel('Log10(Views)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('phase3_visualizations/distributions/views_log_by_country.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved views distribution (log scale) by country")

print("\n" + "=" * 80)
print("PHASE 3 COMPLETED SUCCESSFULLY!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  1. phase3_summary_statistics.csv")
print(f"  2. phase3_eda_report.md")
print(f"  3. phase3_visualizations/ (directory with all visualizations)")
print(f"  4. phase3_eda.py (this script)")

