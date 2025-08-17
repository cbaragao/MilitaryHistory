# SEAFA Dataset

Southeast Asia Forces database with comprehensive personnel and operational data.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/southeast-asia-forces-seafa](https://data.world/aragaocb/southeast-asia-forces-seafa)

### Source Information
- **NARA ID**: 602104
- **Original Filename**: RG330.SEAFA.Y6672.txt
- **Catalog URL**: https://catalog.archives.gov/id/602104
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records/rg-330/SEAFA/RG330.SEAFA.Y6672.txt

## 🗃️ Data Structure

### Transaction Files
- **seafa_tx.csv**: Primary transaction data file containing 20 fields

### Schema Information
- **Total Fields**: 20
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **UNITO**: This field identifies the unit. The unit number for South Vietnamese units is an arbitrarily assigned number unique for every unit; the numbers for the US and FWMAF units were obtained from the STALA file. (Type: Alpha, Length: 6)
- **YEAR**: This field identifies the year, e.g., '68'. (Type: Alpha, Length: 2)
- **MONTH**: This field identifies the month, e.g., '10' represents October. (Type: Alpha, Length: 2)
- **UNAME**: This field identifies the unit name. (Type: Alpha, Length: 30)
- **PROV**: This field identifies the province in which the unit is located. The table for converting province code to province name is used in output. (Type: locations.json, Length: 3)
- **UTMQD**: This field contains the two characters -- quadrant identification -- of the UTM coordinate. (Type: Alpha, Length: 2)
- **UTMES**: This field contains the easting values of the UTM coordinate. (Type: Alpha, Length: 3)
- **UTMNO**: This field contains the northing values of the UTM coordinate. (Type: Alpha, Length: 3)
- **VCMR**: This field identifies the Viet Cong Military Region (VCMR) in which the unit is located. Data for this field is derived from the province in which the unit is reported to be located. Conversion from province to VCMR is as shown in Table 1 Chapter 7. (Type: VCMR.json, Length: 2)
- **CTZ**: This field identifies the Corps Tactical Zone in which the unit is located. Data for this field are derived from the province in which the unit is reported to be located. Conversion from province code to corps area is as shown in Table 1. (Type: ctz.json, Length: 1)

... and 10 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/seafa.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/seafa.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/southeast-asia-forces-seafa](https://data.world/aragaocb/southeast-asia-forces-seafa)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `seafa_tx.csv`
- **Schema Metadata**: `seafa_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM seafa_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/southeast-asia-forces-seafa')

# Access transaction data
df = dataset.dataframes['seafa_tx']

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
MilitaryHistory Project. (2025). SEAFA Dataset. 
Retrieved from https://data.world/aragaocb/southeast-asia-forces-seafa
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
