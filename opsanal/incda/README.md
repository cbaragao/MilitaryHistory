# INCDA Dataset

Republic of Vietnam incidents database documenting security events and operational reports.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/republic-of-vietnam-incidents-files-incda](https://data.world/aragaocb/republic-of-vietnam-incidents-files-incda)

### Source Information
- **NARA ID**: 2569432
- **Original Filename**: INCDA.AR.FIX
- **Catalog URL**: https://catalog.archives.gov/id/2569432
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/opastorage/live/32/5694/2569432/content/arcmedia/electronic-records/rg-218/INCDA/INCDA.AR.FIX

## 🗃️ Data Structure

### Transaction Files
- **incda_tx.csv**: Primary transaction data file containing 21 fields

### Schema Information
- **Total Fields**: 21
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **YEAR**: Year of cease-fire violation (Type: Alphanumeric, Length: 2)
- **MONTH**: Month of cease-fire violation (Type: Alphanumeric, Length: 2)
- **DAY**: Day of cease-fire violation (Type: Alphanumeric, Length: 2)
- **INSEQ**: Locally Assigned Sequence Number (Type: Alphanumeric, Length: 4)
- **PCN**: System Generated (Type: Alphanumeric, Length: 3)
- **SC0**: System Generated (Type: Alphanumeric, Length: 4)
- **VSZ**: System Generated (Type: Alphanumeric, Length: 4)
- **ILOC**: UTM Coordinates of cease fire violation (Type: Alphanumeric, Length: 15)
- **NOINC**: Number of Incidents (Type: Alphanumeric, Length: 3)
- **CAT**: Category of the Incident (Type: Alphanumeric, Length: 1)

... and 11 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- No additional documentation files available

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/incda.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/incda.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/republic-of-vietnam-incidents-files-incda](https://data.world/aragaocb/republic-of-vietnam-incidents-files-incda)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `incda_tx.csv`
- **Schema Metadata**: `incda_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM incda_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/republic-of-vietnam-incidents-files-incda')

# Access transaction data
df = dataset.dataframes['incda_tx']

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
MilitaryHistory Project. (2025). INCDA Dataset. 
Retrieved from https://data.world/aragaocb/republic-of-vietnam-incidents-files-incda
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
