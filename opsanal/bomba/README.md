# BOMBA Dataset

Bombing operations and ordnance data from air campaign activities.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/bomba](https://data.world/aragaocb/bomba)

### Source Information
- **NARA ID**: UNKNOWN
- **Original Filename**: not applicable
- **Catalog URL**: not applicable
- **Available Online**: False
- **Source URL**: not applicable

## 🗃️ Data Structure

### Transaction Files
- **bomba_tx.csv**: Primary transaction data file containing 23 fields

### Schema Information
- **Total Fields**: 23
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **YEAR**: This field indicates the last two digits of the year in which the mission occurred, i.e., for 1968. (Type: Alphanumeric, Length: 2)
- **MONTH**: This field indicates the two-digit code for the month in which the mission occurred, i.e., 01 for January. (Type: Alphanumeric, Length: 2)
- **CNTRY**: This field contains a two-character code for the target country. (Type: VN: NORTH VIETNAM, VS: SOUTH VIETNAM, TH: THAILAND, UN: UNKNOWN, Length: 2)
- **CNTRL**: This field contains a machine-generated number between 0001 and 99999 which ensures unique identification of the record. It is reinitialized to 00001 for each new month. (Type: Alphanumeric, Length: 5)
- **SERV**: This field contains an alphabetic code for the launch service. (Type: A: ARVN; J: USAF; M: USMC; N: USN; V: VNAF; W: ARMY, Length: 1)
- **STMAC**: This field contains the type, model, and series (TMS) of the sortie aircraft. (Type: Alphabetic, Length: 8)
- **TTYPE**: This field contains a code for the general type of target attacked. (Type: See Table 1, Length: 2)
- **SFUNC**: This field contains a code for sortie function; only the attack functions 01-06 are in the file. (Type: 01: STRIKE; 02: FLAK SUPPRESSION; 03: AIR INTERDICTION; 04: ARMED RECCE; 05: CLOSE AIR SUPPORT; 06: DIRECT AIR SUPPORT, Length: 2)
- **CORPS**: This field contains a code for Corps Tactical Zone or Route Package. (Type: See Table 2, Length: 1)
- **PROVN**: This field contains a code for the province area in South Vietnam. (Type: See Table 3, Length: 2)

... and 13 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/bomba.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/bomba.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/bomba](https://data.world/aragaocb/bomba)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `bomba_tx.csv`
- **Schema Metadata**: `bomba_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM bomba_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/bomba')

# Access transaction data
df = dataset.dataframes['bomba_tx']

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
MilitaryHistory Project. (2025). BOMBA Dataset. 
Retrieved from https://data.world/aragaocb/bomba
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
