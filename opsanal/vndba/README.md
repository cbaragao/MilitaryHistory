# VNDBA Dataset

Vietnam database containing comprehensive operational and administrative records.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/vndba](https://data.world/aragaocb/vndba)

### Source Information
- **NARA ID**: 5927921
- **Original Filename**: not applicable
- **Catalog URL**: https://catalog.archives.gov/id/5927921
- **Available Online**: True
- **Source URL**: not applicable

## 🗃️ Data Structure

### Transaction Files
- **vndba_tx.csv**: Primary transaction data file containing 95 fields

### Schema Information
- **Total Fields**: 95
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **SITRP**: This field is a unique number identifying a specific incident/operation (Record). An E or F in the low-order position indicates the record is for an enemy or friendly initiated incident. (Type: Alphanumeric, Length: 9)
- **ZNDIV**: Corps zone (first character) and ARVN divisional area (last 2 characters) where the incident occurred. (Type: Numeric, Length: 3)
- **PROVN**: Code for the province where the incident occurred. (Type: province_names.json, Length: 2)
- **REGON**: Viet Cong Military Region where the incident occurred. (Type: Numeric, Length: 1)
- **COORX**: UTM coordinate location of the incident. (Type: Alphanumeric, Length: 8)
- **LUNAR**: Lunar date when the incident occurred. (Type: Numeric, Length: 5)
- **SDAYS**: Day of year (Julian), week, and the day when the incident started. (DDDWWddd) (Type: Numeric, Length: 8)
- **SDATE**: Year, month, and day when the incident started. (YYMMDD) (Type: Numeric, Length: 6)
- **STIME**: Hour and minute and the name of the month when the incident started. (HHMMmmm) (Type: Alphanumeric, Length: 7)
- **CDATE**: Year, month, and day when the incident terminated. (YYMMDD) (Type: Numeric, Length: 6)

... and 85 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/vndba.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/vndba.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/vndba](https://data.world/aragaocb/vndba)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `vndba_tx.csv`
- **Schema Metadata**: `vndba_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM vndba_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/vndba')

# Access transaction data
df = dataset.dataframes['vndba_tx']

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
MilitaryHistory Project. (2025). VNDBA Dataset. 
Retrieved from https://data.world/aragaocb/vndba
```

---

**Generated**: 2025-08-17 15:45:20 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
