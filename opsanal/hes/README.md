# HES Dataset

Hamlet Evaluation System data measuring security and development in Vietnamese communities.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/hes](https://data.world/aragaocb/hes)

### Source Information
- **NARA ID**: Unknown
- **Original Filename**: Unknown
- **Catalog URL**: Not available
- **Available Online**: Unknown
- **Source URL**: Not available

## 🗃️ Data Structure

### Transaction Files
- **hes_tx.csv**: Primary transaction data file containing 0 fields

### Schema Information
- **Total Fields**: 0
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/hes.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/hes.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/hes](https://data.world/aragaocb/hes)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `hes_tx.csv`
- **Schema Metadata**: `hes_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM hes_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/hes')

# Access transaction data
df = dataset.dataframes['hes_tx']

# Basic analysis
print(f"Total records: {len(df)}")
print(f"Columns: {list(df.columns)}")
```

### Spatial Analysis

## 🔍 Data Quality

### Completeness
- **Processing Status**: ✅ Complete
- **Data Validation**: Applied during processing
- **Missing Values**: Handled according to original data format

### Known Issues
- Original data may contain historical inconsistencies
- Coordinate precision varies by source
- Some fields may be sparsely populated

## 📖 Historical Context

This dataset is part of the Military History Archival Data Processing Pipeline, which digitizes and processes historical military records from the National Archives. The data provides insights into:

- Military operations and strategic planning
- Personnel management and recognition
- Geographic patterns of conflict events
- Historical operational effectiveness

## 🤝 Contributing

### Data Issues
Report data quality issues or processing errors via the project repository.

### Enhancement Requests
Suggest additional processing features or analysis capabilities.

### Citation
When using this data in research or analysis, please cite:
```
MilitaryHistory Project. (2025). HES Dataset. 
Retrieved from https://data.world/aragaocb/hes
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
