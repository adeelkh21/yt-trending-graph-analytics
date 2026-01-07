# YouTube Trending Videos Analysis Using Graph Database

## Project Overview
This project analyzes YouTube Trending Videos across the United States, Great Britain, Canada, and India using Python-based data processing and a Neo4j graph database. The end-to-end workflow spans data exploration, cleaning, exploratory analysis, graph modeling, and query-driven insights.

- Time period: Nov 2017 – Jun 2018
- Initial records: 158,098 → Cleaned unique videos: 50,357
- Graph size: 326,488 nodes and 1,264,948 relationships

## Data
- Source: YouTube Trending dataset (Kaggle)
- Raw inputs: Country CSVs (US, GB, CA, IN) and category JSONs
- Cleaned output: `youtube_trending_cleaned.csv`
- Current repository layout:
  - Data files in `data/`
  - JSON files in `jsonFiles/`

## Workflow (Phases)
1. Phase 1 — Data Exploration
   - Load and inspect raw CSVs
   - Combine datasets and add country identifiers
   - Generate summary statistics and data quality report
2. Phase 2 — Preprocessing
   - Handle missing values, duplicates, outliers
   - Clean text fields and standardize types
   - Produce cleaned dataset for downstream analysis
3. Phase 3 — EDA
   - Summary statistics and distributions
   - Trend analysis by category, channel, country, and time
   - Correlation matrices and visualizations
4. Phase 4 — Graph Ingestion
   - Neo4j setup (Aura or Desktop)
   - Model videos, channels, categories, and relationships
   - Ingest cleaned data to enable graph queries
5. Phase 5 — Query & Analysis
   - Execute simple and complex graph queries
   - Generate reports, visualizations, and statistical tests

## Key Results & Insights
- Entertainment and Music dominate trending content across countries.
- Great Britain shows highest average views per video (~3.4M); Canada has highest engagement ratio (~3.57%).
- T-Series leads with ~834M total views.
- Peak trending days: Thursday (US/GB), Tuesday (CA/IN).
- Views vs. engagement ratio shows a moderate negative correlation (≈ -0.41).

## How to Run
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Phase 1: Exploration
   ```bash
   python phase1_data_preperation/phase1_data_exploration.py
   ```
3. Phase 2: Preprocessing
   ```bash
   python phase2_preprocessing/phase2_preprocessing.py
   ```
4. Phase 3: EDA
   ```bash
   python phase3_EDA/phase3_eda.py
   ```
5. Phase 4: Graph Ingestion
   ```bash
   python phase4_data_ingestion/phase4_graph_ingestion.py
   ```
6. Phase 5: Query & Analysis
   ```bash
   python phase5_Query_Analysis/phase5_query_analysis.py
   ```

## Repository Structure (Key)
- data/ — CSV outputs and consolidated tables
- jsonFiles/ — Category and log JSONs
- phase1_data_preperation/ — Exploration scripts and reports
- phase2_preprocessing/ — Cleaning scripts and reports
- phase3_EDA/ — EDA scripts and visualizations
- phase4_data_ingestion/ — Neo4j ingestion and setup
- phase5_Query_Analysis/ — Graph queries, outputs, and reports

## Notes
- Neo4j Aura connection parameters are included in scripts; local Desktop setup is optional.
- Visualizations and query results are available under phase-specific output folders.