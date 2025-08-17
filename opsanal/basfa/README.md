# BASFA Dataset

Base facilities administration and logistics data.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/basfa](https://data.world/aragaocb/basfa)

### Source Information
- **NARA ID**: 2573252
- **Original Filename**: BASFA.TR.DAT.txt
- **Catalog URL**: https://catalog.archives.gov/id/2573252
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records/rg-330/BASFA/BASFA.TR.DAT.txt

## 🗃️ Data Structure

### Transaction Files
- **basfa_tx.csv**: Primary transaction data file containing 62 fields

### Schema Information
- **Total Fields**: 62
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **BASNO**: A unique identification number assigned to each base area (Type: Alphanumeric, Length: 3)
- **PRCNY**: This field contains a three digit code indicating the country and province location of the base area. For the code values see the table CPRVS (Table 5). (Type: Alphanumeric, Length: 3)
- **VCMR**: This field contains a two digit number indicating the VCMR where the base area is located. For the code values see the table VCMRS (Table 4). (Type: Alphanumeric, Length: 2)
- **UTMC**: This field contains the approximate center of the base area by UTM coordinate. (Type: Alphanumeric, Length: 8)
- **UTM1**: This field contains the first in a series of up to nine UTM coordinates used to describe the boundary of the base area. (Type: Alphanumeric, Length: 8)
- **UTM2**: This field contains the second in a series of up to nine UTM coordinates used to describe the boundary of the base area. (Type: Alphanumeric, Length: 8)
- **UTM3**: This field contains the third in a series of up to nine UTM coordinates used to describe the boundary of the base area. (Type: Alphanumeric, Length: 8)
- **UTM4**: This field contains the fourth in a series of up to nine UTM coordinates used to describe the boundary of the base area. (Type: Alphanumeric, Length: 8)
- **UTM5**: This field contains the fifth in a series of up to nine UTM coordinates used to describe the boundary of the base area. (Type: Alphanumeric, Length: 8)
- **UTM6**: This field contains the sixth in a series of up to nine UTM coordinates used to describe the boundary of the base area. (Type: Alphanumeric, Length: 8)

... and 52 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/basfa.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/basfa.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/basfa](https://data.world/aragaocb/basfa)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `basfa_tx.csv`
- **Schema Metadata**: `basfa_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM basfa_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/basfa')

# Access transaction data
df = dataset.dataframes['basfa_tx']

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
MilitaryHistory Project. (2025). BASFA Dataset. 
Retrieved from https://data.world/aragaocb/basfa
```

---

**Generated**: 2025-08-17 15:45:18 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
