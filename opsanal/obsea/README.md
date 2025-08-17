# OBSEA Dataset

Observation and surveillance data from Southeast Asia operations.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/obsea](https://data.world/aragaocb/obsea)

### Source Information
- **NARA ID**: UNKNOWN
- **Original Filename**: not applicable
- **Catalog URL**: not applicable
- **Available Online**: False
- **Source URL**: not applicable

## 🗃️ Data Structure

### Transaction Files
- **obsea_tx.csv**: Primary transaction data file containing 56 fields

### Schema Information
- **Total Fields**: 56
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **RCID**: A unique identification number assigned by the DIA. (Type: Numeric, Length: 17)
- **PROV**: A three-digit code of the current accepted location of the enemy unit. (Type: OB01S_Province_Codes.json, Length: 3)
- **UNAME**: Full name of the unit being reported. (Type: Alphanumeric, Length: 30)
- **USIZE**: A three-digit code specifying the unit size, such as platoon or regiment. (Type: Numeric, Length: 3)
- **USTRN**: Contains the current strength of the enemy unit. (Type: Numeric, Length: 6)
- **UNNAT**: Nationality of the unit being reported. (Type: Numeric, Length: 1)
- **UNCAT**: Contains a category designation for the unit. (Type: UNCAT.json, Length: 1)
- **UTYPE**: Specifies the type of force, such as Infantry, Artillery, Engineer. (Type: Alphabetic, Length: 1)
- **UNIFN**: Specifies the function of the enemy unit. (Type: UNIFN.json, Length: 1)
- **SERV**: Indicates the service branch of the enemy unit. (Type: SERV.json, Length: 1)

... and 46 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/obsea.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/obsea.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/obsea](https://data.world/aragaocb/obsea)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `obsea_tx.csv`
- **Schema Metadata**: `obsea_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM obsea_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/obsea')

# Access transaction data
df = dataset.dataframes['obsea_tx']

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
MilitaryHistory Project. (2025). OBSEA Dataset. 
Retrieved from https://data.world/aragaocb/obsea
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
