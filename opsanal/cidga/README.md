# CIDGA Dataset

Combat intelligence and damage assessment reports.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/cidga](https://data.world/aragaocb/cidga)

### Source Information
- **NARA ID**: UNKNOWN
- **Original Filename**: not applicable
- **Catalog URL**: not applicable
- **Available Online**: False
- **Source URL**: not applicable

## 🗃️ Data Structure

### Transaction Files
- **cidga_tx.csv**: Primary transaction data file containing 54 fields

### Schema Information
- **Total Fields**: 54
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **RMNTH**: This field indicates the month by number reported for the message, e.g., 01 for January, 02 for February. (Type: Alphabetic, Length: 2)
- **CORPS**: This field indicates the Corps Tactical Zone of South Vietnam being reported, 1, 2, 3, or 4. (Type: Alphabetic, Length: 1)
- **DET**: This field identifies the detachment reported. (Type: Alphabetic, Length: 5)
- **MTYP1**: This field contains a code for the first mission type reported. (Type: See Table 1, Length: 4)
- **MTYP2**: This field contains a code for the second mission type, if reported. (Type: See Table 1, Length: 4)
- **MTYP3**: This field contains a code for the third mission type, if reported. (Type: See Table 1, Length: 4)
- **POINT**: This field indicates the UTM coordinate location of the detachment reported. (Type: Alphabetic, Length: 8)
- **LOC**: This field indicates the geographical location reported. (Type: Alphabetic, Length: 15)
- **PROVN**: This field contains a code for a province. (Type: See Table 4, Length: 2)
- **SDATE**: This field indicates the year and month the mission started, e.g., 6801 for January 1968. (Type: Numeric, Length: 4)

... and 44 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/cidga.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/cidga.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/cidga](https://data.world/aragaocb/cidga)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `cidga_tx.csv`
- **Schema Metadata**: `cidga_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM cidga_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/cidga')

# Access transaction data
df = dataset.dataframes['cidga_tx']

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
MilitaryHistory Project. (2025). CIDGA Dataset. 
Retrieved from https://data.world/aragaocb/cidga
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
