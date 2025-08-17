# INCDA_PS3 Dataset

Military operational dataset containing INCDA_PS3 related information and records.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/incda_ps3](https://data.world/aragaocb/incda_ps3)

### Source Information
- **NARA ID**: 2569436
- **Original Filename**: INCDA.AR.PER3
- **Catalog URL**: https://catalog.archives.gov/id/2569436
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/opastorage/live/36/5694/2569436/content/arcmedia/electronic-records/rg-218/INCDA/INCDA.AR.PER3

## 🗃️ Data Structure

### Transaction Files
- **incda_ps3_tx.csv**: Primary transaction data file containing 12 fields

### Schema Information
- **Total Fields**: 12
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **YEAR**: Year of report (Type: Alphanumeric, Length: 2)
- **MONTH**: Month of report (Type: Alphanumeric, Length: 2)
- **DAY**: Day of report (Type: Alphanumeric, Length: 2)
- **INSEQ**: Sequence Number (Type: Alphanumeric, Length: 4)
- **PCN**: System Generated (Type: Alphanumeric, Length: 3)
- **PSSQ3**: System Generated (Type: Alphanumeric, Length: 4)
- **VSZ3**: System Generated (Type: Numeric, Length: 4)
- **OSEQ**: Sequence Number (Type: Alphanumeric, Length: 1)
- **ORIG**: Message originator (Type: Alphanumeric, Length: 10)
- **ODTG**: Date Time Group of Message (Type: Alphanumeric, Length: 10)

... and 2 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/incda_ps3.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/incda_ps3.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/incda_ps3](https://data.world/aragaocb/incda_ps3)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `incda_ps3_tx.csv`
- **Schema Metadata**: `incda_ps3_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM incda_ps3_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/incda_ps3')

# Access transaction data
df = dataset.dataframes['incda_ps3_tx']

# Basic analysis
print(f"Total records: {len(df)}")
print(f"Columns: {list(df.columns)}")
```

### Spatial Analysis

This dataset includes spatial coordinates that can be used for mapping and geographic analysis:

```python
# Geographic visualization
import folium

# Create map with data points
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# Add data points to map
for idx, row in df.iterrows():
    if pd.notna(row['latitude']) and pd.notna(row['longitude']):
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=f"Event: {row['event_type']}"
        ).add_to(m)

m.save('map.html')
```

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
MilitaryHistory Project. (2025). INCDA_PS3 Dataset. 
Retrieved from https://data.world/aragaocb/incda_ps3
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
