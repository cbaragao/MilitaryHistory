# KHMER Dataset

Cambodia operations database documenting military activities and incident reports during the conflict period.

## 📊 Dataset Overview

**Data.world Location**: [aragaocb/khmer](https://data.world/aragaocb/khmer)

### Source Information
- **NARA ID**: 1937209
- **Original Filename**: KHMER.TR.7074
- **Catalog URL**: https://catalog.archives.gov/id/1937209
- **Available Online**: True
- **Source URL**: https://s3.amazonaws.com/NARAprodstorage/opastorage/live/9/9372/1937209/content/arcmedia/electronic-records/rg-330/KHMER/KHMER.TR.7074

## 🗃️ Data Structure

### Transaction Files
- **khmer_tx.csv**: Primary transaction data file containing 40 fields

### Schema Information
- **Total Fields**: 40
- **Data Format**: Fixed-width or delimited text
- **Processing Status**: ✅ Processed and uploaded to Data.world

### Key Fields
- **MSGDAT**: Message Date (Type: Alphanumeric, Length: 6)
- **ITEMNO**: Item Number (Type: Alphanumeric, Length: 2)
- **FLG1**: ARVN Flag (Type: Alphanumeric, Length: 1)
- **FLG2**: Second Flag (Type: Alphanumeric, Length: 1)
- **FLG3_FLG4**: Third & Fourth Flags (Type: Alphanumeric, Length: 8)
- **MRSD**: Military Region Subdivision (Type: Alphanumeric, Length: 4)
- **ADCT**: Conversion Code (Type: Alphanumeric, Length: 1)
- **ADCR**: Military / Political Subdivision Code (Type: Alphanumeric, Length: 3)
- **INCDATE**: Incident Date (Type: Alphanumeric, Length: 6)
- **QTR**: Quarter (Type: Alphanumeric, Length: 4)

... and 30 more fields. See schema documentation for complete field definitions.

## 📚 Documentation

### Available Files
- **147.1DP.pdf** (PDF Documentation, 1023.5 KB)
- **KHMER_schema.pdf** (PDF Documentation, 247.4 KB)
- **cords.txt** (Text File, 2.1 KB)

### Schema Documentation
- **schema.json**: Complete field definitions and data types
- **Processing script**: `src/scripts/khmer.py`

## 🔄 Data Processing

### Processing Pipeline
1. **Extract**: Download from NARA archives
2. **Transform**: Parse fixed-width format and apply data cleaning
3. **Load**: Upload to Data.world with schema metadata

### Processing Script
```bash
# Run from project root
python src/scripts/khmer.py
```

### Dependencies
- Python 3.8+
- pandas, numpy for data processing
- datadotworld for API integration
- Custom processing utilities in `src/`

## 🌐 Data Access

### Data.world Access
- **Public Dataset**: [aragaocb/khmer](https://data.world/aragaocb/khmer)
- **Query Interface**: SQL and SPARQL query support
- **API Access**: REST and GraphQL APIs available

### File Downloads
- **Transaction Data**: `khmer_tx.csv`
- **Schema Metadata**: `khmer_schema.csv`

### Sample Query
```sql
-- Get basic statistics
SELECT COUNT(*) as total_records,
       MIN(date_field) as earliest_date,
       MAX(date_field) as latest_date
FROM khmer_tx
LIMIT 10;
```

## 📈 Usage Examples

### Data Analysis
```python
import datadotworld as dw

# Connect to dataset
dataset = dw.load_dataset('aragaocb/khmer')

# Access transaction data
df = dataset.dataframes['khmer_tx']

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
MilitaryHistory Project. (2025). KHMER Dataset. 
Retrieved from https://data.world/aragaocb/khmer
```

---

**Generated**: 2025-08-17 15:45:19 | **Source**: NARA Archives | **Processed by**: MilitaryHistory Pipeline
