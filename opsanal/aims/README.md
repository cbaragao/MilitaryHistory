# AIMS Dataset

Awards and decorations database containing comprehensive records of military personnel recognition and honors.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/aimsawards](https://data.world/aragaocb/aimsawards)

### Source Information
- **NARA ID**: 1937232
- **Original Filename**: AIMSFY04.PU.DAT.zip
- **Catalog URL**: https://catalog.archives.gov/id/1937232
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records/rg-428/AIMS/AIMSFY04.PU.DAT.zip

## 🗃️ Data Structure

### Transaction Files
- **aims_tx.csv**: Primary transaction data file containing 50 fields

### Schema Information
- **Total Fields**: 50
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **INDV_UNIT**: Individual or unit case indicator (Type: I=Individual, U=Unit, Length: 1)
- **PRIM_TYPE**: Case type - CNO=Chief Naval Ops, CMC=Marine Corps, SEC=SECNAV, FLT=Fleet (Type: CNO, CMC, SEC, FLT, Length: 3)
- **FOREIGN**: Whether award is to foreign individual (Type: Y=Yes, N=No, Length: 1)
- **COUNTRY**: Country of foreign individual (Type: Text, Length: 25)
- **CAMPAIGN**: Period of action/campaign code (Type: Code, Length: 5)
- **SECBD_MTG**: SECNAV board meeting date (Type: Date, Length: 11)
- **DUP**: Duplicate record indicator (Type: Alphanumeric, Length: 2)
- **SSN**: Social Security Number (restricted data) (Type: Numeric, Length: 11)
- **LNAME**: Last name (Type: Text, Length: 20)
- **FNAME**: First name (Type: Text, Length: 15)

... and 40 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- **412_7-8ADA.pdf** (PDF Documentation, 95.6 KB)
- **412_7-8ADD.pdf** (PDF Documentation, 138.6 KB)
- **412_7-8ND.pdf** (PDF Documentation, 438.2 KB)
- **AIMS.8804.CD.ACT** (.ACT File, 322 B)
- **AIMS.8804.CD.AUTH** (.AUTH File, 1.5 KB)
- **AIMS.8804.CD.AWD** (.AWD File, 3.4 KB)
- **AIMS.8804.CD.CAMP** (.CAMP File, 598 B)
- **AIMS.8804.CD.CORP** (.CORP File, 176 B)
- **AIMS.8804.CD.DOC** (.DOC File, 42.7 KB)
- **AIMS.8804.CD.GRD** (.GRD File, 6.5 KB)
- **AIMS.8804.CD.RATE** (.RATE File, 23.9 KB)

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/aims.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/aims.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/aimsawards](https://data.world/aragaocb/aimsawards)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `aims_tx.csv`
- **Schema Metadata**: `aims_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM aims_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/aimsawards')

# Access transaction data
df = dataset.dataframes['aims_tx']

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
MilitaryHistory Project. (2025). AIMS Dataset. 
Retrieved from https://data.world/aragaocb/aimsawards
```

---

**Generated**: 2025-08-17 15:45:18 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
