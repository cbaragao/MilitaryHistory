# PSYOPSA Dataset

Psychological operations dataset containing strategic communication and influence campaign data.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/psyopsa](https://data.world/aragaocb/psyopsa)

### Source Information
- **NARA ID**: 148414386
- **Original Filename**: PSY.M70TF73.ARFS.csv
- **Catalog URL**: https://catalog.archives.gov/id/148414386
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records/rg-472/PSYOPSIS/PSY.M70TF73.ARFS.csv

## 🗃️ Data Structure

### Transaction Files
- **psyopsa_tx.csv**: Primary transaction data file containing 16 fields

### Schema Information
- **Total Fields**: 16
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **USID**: Unit or district identifier (primary key) (Type: Alphanumeric, Length: 5)
- **PCN**: System-generated sequence number (Type: Alphanumeric, Length: 3)
- **SC0**: System-generated security code (Type: Alphanumeric, Length: 15)
- **VSZ**: System-generated variable size field (Type: Numeric, Length: 4)
- **POP**: Total population of the district (Type: Numeric, Length: 7)
- **GVNPOP**: Population under GVN (Government of Vietnam) control (Type: Numeric, Length: 7)
- **HOICHN**: Number of Hoi Chanh (defectors) received (Type: Numeric, Length: 5)
- **REF**: Number of refugees in the district (Type: Numeric, Length: 6)
- **NVA**: Estimated North Vietnamese Army personnel count (Type: Numeric, Length: 6)
- **VCHAM**: Estimated Viet Cong/Hamlet guerrillas count (Type: Numeric, Length: 6)

... and 6 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- **378.1DP.pdf** (PDF Documentation, 342.1 KB)
- **LOOKUP_TABLES.pdf** (PDF Documentation, 490.2 KB)
- **PSY.M70TF73.ARLAY.html** (HTML Documentation, 41.0 KB)

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/psyopsa.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/psyopsa.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/psyopsa](https://data.world/aragaocb/psyopsa)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `psyopsa_tx.csv`
- **Schema Metadata**: `psyopsa_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM psyopsa_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/psyopsa')

# Access transaction data
df = dataset.dataframes['psyopsa_tx']

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
MilitaryHistory Project. (2025). PSYOPSA Dataset. 
Retrieved from https://data.world/aragaocb/psyopsa
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
