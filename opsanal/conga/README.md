# CONGA Dataset

Congressional data and legislative information related to military operations.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/conga](https://data.world/aragaocb/conga)

### Source Information
- **NARA ID**: 573632
- **Original Filename**: CONGA.6673FIX
- **Catalog URL**: https://catalog.archives.gov/id/573632
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/opastorage/live/32/5736/573632/content/arcmedia/electronic-records/rg-218/CONGA/CONGA.6673FIX

## 🗃️ Data Structure

### Transaction Files
- **conga_tx.csv**: Primary transaction data file containing 39 fields

### Schema Information
- **Total Fields**: 39
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **SDATE**: Firing date (Type: Alphanumeric, Length: 6)
- **STIME**: Starting time (Type: Alphanumeric, Length: 6)
- **ETIME**: Ending time (Type: Alphanumeric, Length: 6)
- **UIC**: Ship UIC (Type: Alphanumeric, Length: 6)
- **SERIES**: Series number (Type: Alphanumeric, Length: 3)
- **UDATE**: Date of last update (Type: Numeric, Length: 5)
- **SHNME**: Ship name (Type: Alphanumeric, Length: 16)
- **SHFTP**: Ship type (Type: Alphanumeric, Length: 4)
- **HLLNO**: Hull number (Type: Alphanumeric, Length: 4)
- **ARCOD**: Area code (Type: Alphanumeric, Length: 1)

... and 29 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- **178.1-2AD.pdf** (PDF Documentation, 9.1 MB)
- **178.1DP.pdf** (PDF Documentation, 1.2 MB)
- **conga_definitions.pdf** (PDF Documentation, 292.3 KB)
- **conga_schema.pdf** (PDF Documentation, 53.1 KB)

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/conga.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/conga.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/conga](https://data.world/aragaocb/conga)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `conga_tx.csv`
- **Schema Metadata**: `conga_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM conga_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/conga')

# Access transaction data
df = dataset.dataframes['conga_tx']

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
MilitaryHistory Project. (2025). CONGA Dataset. 
Retrieved from https://data.world/aragaocb/conga
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
