# AWARDSDECORATIONS Dataset

Military operational dataset containing AWARDSDECORATIONS related information and records.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/awardsdecorations](https://data.world/aragaocb/awardsdecorations)

### Source Information
- **NARA ID**: 1937849
- **Original Filename**: AWADS.TR.PUBL
- **Catalog URL**: https://catalog.archives.gov/id/1937849
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/opastorage/live/49/9378/1937849/content/arcmedia/electronic-records/rg-472/AWADS/AWADS.TR.PUBL

## 🗃️ Data Structure

### Transaction Files
- **awardsdecorations_tx.csv**: Primary transaction data file containing 31 fields

### Schema Information
- **Total Fields**: 31
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **SERPX**: Service number prefix identifier (Type: Alphanumeric, Length: 2)
- **SERNO**: Individual service number identifier (Type: Alphanumeric, Length: 8)
- **SEQNO**: Sequence number for record ordering (Type: Numeric, Length: 3)
- **NAME**: Full name of the individual receiving award (Type: Alphanumeric, Length: 18)
- **GRDCD**: Military grade/rank code (Type: Alphanumeric, Length: 2)
- **CMD**: Command or staff unit code (Type: Alphanumeric, Length: 2)
- **CMDNM**: Full name of command or staff unit (Type: Alphanumeric, Length: 37)
- **SVC**: Service branch or country code (Type: Alphanumeric, Length: 1)
- **SVCNM**: Full name of service branch or country (Type: Alphanumeric, Length: 30)
- **DEROS**: Date individual is eligible to return from overseas (YYMMDD format) (Type: Date, Length: 5)

... and 21 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- **LOOKUP_TABLES.pdf** (PDF Documentation, 358.8 KB)
- **schema.pdf** (PDF Documentation, 335.2 KB)

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/awardsdecorations.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/awardsdecorations.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/awardsdecorations](https://data.world/aragaocb/awardsdecorations)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `awardsdecorations_tx.csv`
- **Schema Metadata**: `awardsdecorations_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM awardsdecorations_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/awardsdecorations')

# Access transaction data
df = dataset.dataframes['awardsdecorations_tx']

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
MilitaryHistory Project. (2025). AWARDSDECORATIONS Dataset. 
Retrieved from https://data.world/aragaocb/awardsdecorations
```

---

**Generated**: 2025-08-18 16:45:14 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
