# HOSTA Dataset

Military operational dataset containing HOSTA related information and records.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/hosta](https://data.world/aragaocb/hosta)

### Source Information
- **NARA ID**: 584667
- **Original Filename**: RG038.HOSTA.Y6670
- **Catalog URL**: https://catalog.archives.gov/id/584667
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/opastorage/live/67/5846/584667/content/arcmedia/electronic-records/rg-038/hosta/RG038.HOSTA.Y6670

## 🗃️ Data Structure

### Transaction Files
- **hosta_tx.csv**: Primary transaction data file containing 22 fields

### Schema Information
- **Total Fields**: 22
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **DATE_INCIDENT**: Date of incident in MM/DD/YY format (positions 1-8) (Type: Date, Length: 8)
- **BLANK1**: Blank field (positions 9-10) (Type: Alphanumeric, Length: 2)
- **TIME_INCIDENT**: Time of incident in 24-hour format (positions 11-14) (Type: Numeric, Length: 4)
- **BLANK2**: Blank field (position 15) (Type: Alphanumeric, Length: 1)
- **NUM_HOSTILE_GUNS**: Number of hostile guns involved (positions 16-17) (Type: Numeric, Length: 2)
- **SLASH1**: Slash separator (position 18) (Type: Alphanumeric, Length: 1)
- **CALIBRE_HOSTILE_GUNS**: Calibre/size of hostile guns (positions 19-26) (Type: Alphanumeric, Length: 8)
- **BLANK3**: Blank field (positions 27-28) (Type: Alphanumeric, Length: 2)
- **ROUNDS_FIRED**: Number of rounds fired in the incident (positions 29-34) (Type: Numeric, Length: 6)
- **ACCURACY_ENEMY_FIRE**: Assessment of accuracy of enemy fire (positions 35-45) (Type: Alphanumeric, Length: 11)

... and 12 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- **schema.pdf** (PDF Documentation, 453.4 KB)

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/hosta.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/hosta.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/hosta](https://data.world/aragaocb/hosta)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `hosta_tx.csv`
- **Schema Metadata**: `hosta_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM hosta_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/hosta')

# Access transaction data
df = dataset.dataframes['hosta_tx']

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
MilitaryHistory Project. (2025). HOSTA Dataset. 
Retrieved from https://data.world/aragaocb/hosta
```

---

**Generated**: 2025-08-18 17:15:28 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
