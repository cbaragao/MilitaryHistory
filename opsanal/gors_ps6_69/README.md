# GORS_PS6_69 Dataset

Military operational dataset containing GORS_PS6_69 related information and records.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/gors_ps6_69](https://data.world/aragaocb/gors_ps6_69)

### Source Information
- **NARA ID**: 40978561
- **Original Filename**: GORS69.AR.P6.txt
- **Catalog URL**: https://catalog.archives.gov/id/40978561
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records/rg-472/GORS/GORS69.AR.PS6.txt

## 🗃️ Data Structure

### Transaction Files
- **gors_ps6_69_tx.csv**: Primary transaction data file containing 14 fields

### Schema Information
- **Total Fields**: 14
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **DATE**: Publication date of the operational report (Type: Alphanumeric, Length: 6)
- **DATAT**: Publication date of the operational report (Type: Alphanumeric, Length: 1)
- **SERAL**: Record sequence number within the operational report (Type: Alphanumeric, Length: 3)
- **CORP**: Corps tactical zone in which the action occurred (Type: Alphanumeric, Length: 1)
- **PART**: Major force of the action (Type: Alphanumeric, Length: 1)
- **PCN**: Periodic set number; created by the NIPSTRAN program (Type: Alphanumeric, Length: 3)
- **PSSQ6**: Subset sequence number used for periodic set identification; created by the NIPSTRAN (Type: Alphanumeric, Length: 4)
- **VSZ6**: Indicates number of characters in the logical record's variable field; the field will contain zeros if there is no variable field for a logical record; created by the NIPSTRAN program (Type: Numeric, Length: 4)
- **RTWER**: Ratio of VC weapons lost to allied weapons (Type: Numeric, Length: 4)
- **RTPER**: Ratio of VC casualties to allied casualties (Type: Numeric, Length: 4)

... and 4 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/gors_ps6_69.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/gors_ps6_69.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/gors_ps6_69](https://data.world/aragaocb/gors_ps6_69)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `gors_ps6_69_tx.csv`
- **Schema Metadata**: `gors_ps6_69_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM gors_ps6_69_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/gors_ps6_69')

# Access transaction data
df = dataset.dataframes['gors_ps6_69_tx']

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
MilitaryHistory Project. (2025). GORS_PS6_69 Dataset. 
Retrieved from https://data.world/aragaocb/gors_ps6_69
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
