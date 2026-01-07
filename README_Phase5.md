# Phase 5: Query Execution and Analysis

## Overview
Phase 5 executes comprehensive queries on the Neo4j graph database, generates visualizations, and creates detailed analysis reports. The script runs queries in three groups with checkpoints between each group.

## Prerequisites
- Phase 4 completed (data ingested into Neo4j)
- Neo4j Desktop running with database started
- Python virtual environment activated
- Required packages installed (see requirements.txt)

## Configuration

### Environment Variables (Optional)
You can set these environment variables or the script will use defaults:
- `NEO4J_URI`: Neo4j connection URI (default: `bolt://127.0.0.1:7687`)
- `NEO4J_USER`: Neo4j username (default: `neo4j`)
- `NEO4J_PASSWORD`: Neo4j password (default: `adeel123`)
- `NEO4J_DATABASE`: Neo4j database name (default: `neo4j`)

### Script Parameters
- `QUERY_TIMEOUT`: Query timeout in seconds (default: 60)
- `BATCH_SIZE`: Batch size for large result sets (default: 1000)
- `SAMPLE_LIMIT`: Sample limit for initial runs (default: 1000)

## Execution

### Step 1: Test Connection
```bash
python test_neo4j_connection.py
```

### Step 2: Run Phase 5
```bash
python phase5_query_analysis.py
```

## Query Groups

### Group A: Simple Queries
1. **A.1**: Top Categories by Video Count
2. **A.2**: Top Channels by Total Views
3. **A.3**: Videos by Country
4. **A.4**: Top Videos by Views
5. **A.5**: Average Engagement by Category
6. **A.6**: Day-of-Week Trending Patterns

**Checkpoint**: After Group A completes, the script pauses and waits for user confirmation to proceed.

### Group B: Complex Queries
1. **B.1**: Channels with High Engagement Videos
2. **B.2**: Category Performance by Country
3. **B.3**: Tag Co-occurrence with Categories
4. **B.4**: Cross-Country Video Analysis
5. **B.5**: Channel Performance Analysis

**Checkpoint**: After Group B completes, the script pauses and waits for user confirmation to proceed.

### Group C: Visualization & Statistical Analysis
1. **C.1**: Correlation Analysis
2. **C.2**: Engagement Distribution Analysis
3. **C.3**: Category-Country Network Analysis

## Output Structure

All outputs are saved to a separate repository directory: `phase5_output/`

```
.
└── phase5_output/                    # Main output repository
    ├── query_results/                # CSV query results
    │   ├── groupA_A1_top_categories.csv
    │   ├── groupA_A2_top_channels.csv
    │   ├── groupA_A3_videos_by_country.csv
    │   ├── groupA_A4_top_videos.csv
    │   ├── groupA_A5_engagement_by_category.csv
    │   ├── groupA_A6_day_patterns.csv
    │   ├── groupA_index.json
    │   ├── groupB_B1_high_engagement_channels.csv
    │   ├── groupB_B2_category_by_country.csv
    │   ├── groupB_B3_tag_cooccurrence.csv
    │   ├── groupB_B4_cross_country_videos.csv
    │   ├── groupB_B5_channel_performance.csv
    │   ├── groupB_index.json
    │   ├── groupC_C1_correlation_matrix.csv
    │   └── groupC_C3_category_country_network.csv
    ├── visualizations/               # PNG visualizations
    │   ├── groupA_A1_top_categories.png
    │   ├── groupA_A2_top_channels.png
    │   ├── groupA_A3_videos_by_country.png
    │   ├── groupA_A4_top_videos.png
    │   ├── groupA_A5_engagement_by_category.png
    │   ├── groupA_A6_day_patterns.png
    │   ├── groupB_B1_high_engagement_channels.png
    │   ├── groupB_B2_category_by_country.png
    │   ├── groupB_B3_tag_cooccurrence.png
    │   ├── groupB_B4_cross_country_videos.png
    │   ├── groupB_B5_channel_performance.png
    │   ├── groupC_C1_correlation_heatmap.png
    │   └── groupC_C2_engagement_distribution.png
    ├── reports/                      # Markdown reports
    │   ├── phase5_groupA_summary.md
    │   ├── phase5_groupB_summary.md
    │   ├── phase5_groupC_summary.md
    │   ├── phase5_query_report.md
    │   └── statistical_tests.csv
    ├── phase5_execution_log.json     # Execution log
    └── phase5_results_full.zip       # Complete archive
```

## Output Repository

All Phase 5 outputs are saved to a **separate repository directory** (`phase5_output/`) to keep the main project directory clean and organized. The repository contains:

- **query_results/**: All CSV files with query results
- **visualizations/**: All PNG visualization files
- **reports/**: All Markdown reports and statistical tests
- **phase5_execution_log.json**: Complete execution log
- **phase5_results_full.zip**: Zip archive of all outputs

This structure makes it easy to:
- Share results with others
- Archive outputs
- Keep project directory clean
- Version control outputs separately (if needed)

## Features

### 1. Checkpoint System
- Script pauses after each group
- User can review results before proceeding
- Type `yes` to continue or `no` to stop

### 2. Error Handling
- Continues execution on individual query failures
- Logs all errors to execution log
- Reports errors in summary files

### 3. Batch Processing
- Automatically batches large result sets (>1000 rows)
- Saves multiple CSV files for large datasets
- Prevents memory issues

### 4. Visualizations
- Bar charts for top items
- Line charts for trends
- Heatmaps for correlations
- Scatter plots for relationships

### 5. Statistical Analysis
- Correlation matrices
- Distribution analysis
- Performance metrics

## Execution Log

The script creates `phase5_execution_log.json` with:
- Start and end times
- Query execution details
- Error logs
- Checkpoint timestamps
- Execution status

## Final Report

The final report (`phase5_query_report.md`) includes:
- Executive summary
- Group summaries
- File listings
- Execution statistics
- Key insights
- Recommendations

## Troubleshooting

### Connection Issues
- Ensure Neo4j Desktop is running
- Verify database is started (green status)
- Check connection credentials

### Query Timeouts
- Increase `QUERY_TIMEOUT` if queries are slow
- Check database performance
- Verify indexes are created

### Memory Issues
- Reduce `BATCH_SIZE` for large datasets
- Process queries in smaller batches
- Close other applications

### Visualization Errors
- Check matplotlib/seaborn installation
- Verify data format
- Check file permissions

## Next Steps

After Phase 5 completes:
1. Review generated reports
2. Analyze visualizations
3. Export data for further analysis
4. Create custom queries as needed
5. Share results with stakeholders

## Notes

- The script uses environment variables for configuration
- All queries are logged with timestamps
- Visualizations are saved as PNG files (300 DPI)
- CSV files are saved with UTF-8 encoding
- The final zip archive contains all outputs

## Support

For issues or questions:
1. Check execution log for errors
2. Verify Neo4j connection
3. Review query examples in Phase 4
4. Check database state in Neo4j Browser

