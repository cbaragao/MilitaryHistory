# VCIIA Dataset

Viet Cong Initiated Incidents database tracking enemy-initiated activities and engagements.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/viet-cong-initiated-incidents-vciia](https://data.world/aragaocb/viet-cong-initiated-incidents-vciia)

### Source Information
- **NARA ID**: 600133
- **Original Filename**: VCIIA.AR.FIX.txt
- **Catalog URL**: https://catalog.archives.gov/id/600133
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records/rg-330/VCIIA/VCIIA.AR.FIX.txt

## 🗃️ Data Structure

### Transaction Files
- **vciia_tx.csv**: Primary transaction data file containing 16 fields

### Schema Information
- **Total Fields**: 16
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **SITRP**: Identifies the report from which the data for the incident was taken. (Type: Alphanumeric, Length: 9)
- **PCN**: NIPS Metadata (Type: Alphanumeric, Length: 3)
- **SC0**: NIPS Metadata (Type: Alphanumeric, Length: 4)
- **VSZ**: NIPS Metadata (Type: Alphanumeric, Length: 4)
- **EKIAC**: Confirmed count of enemy killed in action. (Type: Numeric, Length: 3)
- **EWIAC**: Confirmed count of enemy wounded in action. (Type: Numeric, Length: 3)
- **EPOWC**: Confirmed count of enemy prisoners of war. (Type: Numeric, Length: 3)
- **QUART**: Identifies the quarter of the year in which the incident took place. (Type: Numeric, Length: 1)
- **ZNDIV**: This field, when used, indicates any special geographic division, e.g., ARVN divisional area of operation. (Type: Alphanumeric, Length: 2)
- **XNAME**: Identifies the country in which the incident occurred. (Type: XNAME.json, Length: 1)

... and 6 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/vciia.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/vciia.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/viet-cong-initiated-incidents-vciia](https://data.world/aragaocb/viet-cong-initiated-incidents-vciia)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `vciia_tx.csv`
- **Schema Metadata**: `vciia_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM vciia_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/viet-cong-initiated-incidents-vciia')

# Access transaction data
df = dataset.dataframes['vciia_tx']

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
MilitaryHistory Project. (2025). VCIIA Dataset. 
Retrieved from https://data.world/aragaocb/viet-cong-initiated-incidents-vciia
```

---

**Generated**: 2025-08-17 15:45:20 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
