# VSSG Dataset

Military operational dataset containing VSSG related information and records.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/vssgfiles](https://data.world/aragaocb/vssgfiles)

### Source Information
- **NARA ID**: 4658149
- **Original Filename**: PVSSG.7174ARTBFS.txt
- **Catalog URL**: https://catalog.archives.gov/id/4658149
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records/rg-330/HES/VSSG.7174ARTBFS.txt

## 🗃️ Data Structure

### Transaction Files
- **vssg_tx.csv**: Primary transaction data file containing 32 fields

### Schema Information
- **Total Fields**: 32
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **DATE**: Date of hamlet assessment (YYMMDD format) (Type: Alphanumeric, Length: 4)
- **USID**: Identifier of unit submitting the assessment report (Type: Alphanumeric, Length: 9)
- **+PCN**: NIPS Metadata - Province code (Type: Alphanumeric, Length: 3)
- **+SC0**: NIPS Metadata - District code (Type: Alphanumeric, Length: 4)
- **VSZ**: Village size classification code (Type: Numeric, Length: 4)
- **HPOP**: Total population of the hamlet (Type: Numeric, Length: 5)
- **POINT**: Grid reference point for hamlet location (Type: Alphanumeric, Length: 8)
- **URBAN**: Urban or rural classification (Type: Alphanumeric, Length: 1)
- **HMB1**: Hamlet security assessment for nighttime conditions (Type: Numeric, Length: 1)
- **XHMB1**: Extended hamlet security assessment for nighttime (Type: Numeric, Length: 1)

... and 22 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- **LOOKUP_AND_METHODOLOGY.pdf** (PDF Documentation, 2.1 MB)
- **VSSG.7174ARLAY.html** (HTML Documentation, 25.6 KB)
- **schema.pdf** (PDF Documentation, 59.2 KB)
- **user_notes.pdf** (PDF Documentation, 336.3 KB)

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/vssg.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/vssg.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/vssgfiles](https://data.world/aragaocb/vssgfiles)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `vssg_tx.csv`
- **Schema Metadata**: `vssg_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM vssg_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/vssgfiles')

# Access transaction data
df = dataset.dataframes['vssg_tx']

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
MilitaryHistory Project. (2025). VSSG Dataset. 
Retrieved from https://data.world/aragaocb/vssgfiles
```

---

**Generated**: 2025-08-17 19:38:42 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
