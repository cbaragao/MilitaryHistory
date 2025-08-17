# TIRSA Dataset

Terrorist Incident Reporting System containing detailed incident analysis and intelligence reports.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/terrorist-incident-reporting-system-tirsa](https://data.world/aragaocb/terrorist-incident-reporting-system-tirsa)

### Source Information
- **NARA ID**: 7423670
- **Original Filename**: RG330.TIRSA.Y6773.txt
- **Catalog URL**: https://catalog.archives.gov/id/7423670
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records/rg-330/TIRSA/RG330.TIRSA.Y6773.txt

## 🗃️ Data Structure

### Transaction Files
- **tirsa_tx.csv**: Primary transaction data file containing 31 fields

### Schema Information
- **Total Fields**: 31
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **MYM**: This is the highest order field in the control field. (Type: YY = last 2 digits of year; MM = 2 digit month, Length: 4)
- **WEEK**: This field is also part of the control set and the week of the year the incident was reported. (Type: 01-52, Length: 2)
- **SRONO**: The incident number designates a single incident and is unique within the report week. (Type: Incident Number, Length: 4)
- **CORPS**: The corps tactical zone within which the reported incident occurred. Must be entered. (Type: CORPS.json, Length: 1)
- **PROVN**: The province within which the reported incident occurred. This table corresponds to that used by HES/HAMLA. Must be entered. (Type: province_codes.json, Length: 2)
- **DIST**: Where known, the district within which the reported incident occurred. May be '0'. (Type: See HES/HAMLA code. Zero if unknown., Length: 2)
- **VILGE**: Where known, the village in which the reported incident occurred. May be '0'. (Type: See HES/HAMLA code. Zero if unknown., Length: 2)
- **HAMLT**: The hamlet in which the reported incident occurred. May be '0'. (Type: See HES/HAMLA code. Zero if unknown., Length: 2)
- **YEAR**: N/A (Type: The last two digits of the year during which the reported incident occurred., Length: 2)
- **MONTH**: The month during which the reported incident occurred. (Type: 2-digit month code, Length: 2)

... and 21 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/tirsa.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/tirsa.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/terrorist-incident-reporting-system-tirsa](https://data.world/aragaocb/terrorist-incident-reporting-system-tirsa)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `tirsa_tx.csv`
- **Schema Metadata**: `tirsa_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM tirsa_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/terrorist-incident-reporting-system-tirsa')

# Access transaction data
df = dataset.dataframes['tirsa_tx']

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
MilitaryHistory Project. (2025). TIRSA Dataset. 
Retrieved from https://data.world/aragaocb/terrorist-incident-reporting-system-tirsa
```

---

**Generated**: 2025-08-17 15:45:20 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
