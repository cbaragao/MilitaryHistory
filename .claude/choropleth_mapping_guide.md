# Choropleth Mapping Pipeline Guide

## Overview
This guide provides a complete pipeline for creating choropleth maps from conflict event data, including spatial joining with DuckDB and visualization with Folium. Based on the successful Cambodia conflict events mapping project.

## Prerequisites

### Required Software
- Python 3.8+
- DuckDB with spatial extension
- Virtual environment management

### Python Packages
```bash
pip install pandas folium duckdb
```

## Pipeline Steps

### 1. Data Preparation

#### Raw Data Requirements
- **Event Data**: CSV/dataset with longitude/latitude coordinates
- **Spatial Boundaries**: GeoJSON file with administrative boundaries
- **Matching Key**: Common field to join events to boundaries (e.g., province names)

#### Example Data Structure
```
Event Data (CSV):
- longitude, latitude, date, event_type, province_name

Boundary Data (GeoJSON):
- features[].properties.shapeName (matching province_name)
- features[].geometry (polygon/multipolygon coordinates)
```

### 2. Spatial Joining with DuckDB

#### Install DuckDB Spatial Extension
```sql
INSTALL spatial;
LOAD spatial;
```

#### Create Spatial Points from Event Data
```sql
-- Create event points
CREATE TABLE event_points AS
SELECT 
    *,
    ST_Point(longitude, latitude) as geometry
FROM read_csv('path/to/events.csv')
WHERE longitude IS NOT NULL 
  AND latitude IS NOT NULL
  AND longitude BETWEEN valid_min_lon AND valid_max_lon
  AND latitude BETWEEN valid_min_lat AND valid_max_lat;
```

#### Load Administrative Boundaries
```sql
-- Load GeoJSON boundaries
CREATE TABLE admin_boundaries AS
SELECT 
    shapeName,
    ST_GeomFromGeoJSON(geometry) as boundary_geom
FROM ST_Read('path/to/boundaries.geojson');
```

#### Perform Spatial Join
```sql
-- Join events to administrative regions
CREATE TABLE events_by_region AS
SELECT 
    b.shapeName as province_name,
    COUNT(*) as event_count,
    AVG(e.longitude) as avg_longitude,
    AVG(e.latitude) as avg_latitude
FROM event_points e
INNER JOIN admin_boundaries b 
    ON ST_Within(e.geometry, b.boundary_geom)
GROUP BY b.shapeName
ORDER BY event_count DESC;
```

#### Export Results
```sql
-- Export aggregated data
COPY events_by_region TO 'events_by_province.csv' (HEADER, DELIMITER ',');
```

### 3. Verify Spatial File Rendering

#### Test GeoJSON Validity
```python
import json
import folium

# Load and validate GeoJSON
with open('boundaries.geojson', 'r') as f:
    geojson_data = json.load(f)

# Check structure
print(f"Type: {geojson_data.get('type')}")
print(f"Features: {len(geojson_data.get('features', []))}")

# Verify feature properties
for i, feature in enumerate(geojson_data['features'][:3]):
    props = feature.get('properties', {})
    geom_type = feature.get('geometry', {}).get('type')
    print(f"Feature {i}: {props.get('shapeName')} ({geom_type})")
```

#### Create Test Map
```python
# Test basic map rendering
test_map = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# Add GeoJSON to verify boundaries render
folium.GeoJson(
    geojson_data,
    style_function=lambda x: {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.3
    }
).add_to(test_map)

test_map.save('test_boundaries.html')
```

### 4. Choropleth Generation with Folium

#### Complete Implementation
```python
#!/usr/bin/env python3
import json
import pandas as pd
import folium

def create_choropleth_map(event_data_path, geojson_path, output_path):
    """
    Create choropleth map from event data and boundaries
    
    Args:
        event_data_path: Path to CSV with province event counts
        geojson_path: Path to GeoJSON with administrative boundaries  
        output_path: Output HTML file path
    """
    
    # Load event data
    df = pd.read_csv(event_data_path)
    
    # Create base map
    map_center = [center_latitude, center_longitude]
    m = folium.Map(
        location=map_center,
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Create choropleth layer
    choropleth = folium.Choropleth(
        geo_data=geojson_path,
        name='Administrative Regions',
        data=df,
        columns=['province_name', 'event_count'],
        key_on='feature.properties.shapeName',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.8,
        line_color='black',
        line_weight=2,
        legend_name='Event Count',
        smooth_factor=0
    ).add_to(m)
    
    # Add interactive tooltips
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    
    # Create lookup for event counts
    event_lookup = dict(zip(df['province_name'], df['event_count']))
    
    tooltip_layer = folium.FeatureGroup(name='Region Details')
    
    for feature in geojson_data['features']:
        region_name = feature['properties']['shapeName']
        event_count = event_lookup.get(region_name, 0)
        
        tooltip_text = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <b style="font-size: 14px;">{region_name}</b><br>
            <b>Events:</b> {event_count:,}<br>
        </div>
        """
        
        folium.GeoJson(
            feature,
            style_function=lambda x: {
                'fillColor': 'transparent',
                'color': 'transparent',
                'weight': 0,
                'fillOpacity': 0
            },
            tooltip=folium.Tooltip(tooltip_text, sticky=True)
        ).add_to(tooltip_layer)
    
    tooltip_layer.add_to(m)
    folium.LayerControl().add_to(m)
    
    # Add title
    title_html = '''
    <div style="position: fixed; top: 10px; left: 50px; width: 400px; 
                background-color: white; border: 2px solid #333; z-index: 9999; 
                font-family: Arial; padding: 10px; border-radius: 5px;">
        <h3 style="margin: 0;">Event Distribution by Region</h3>
        <p style="margin: 5px 0;">Interactive choropleth visualization</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save map
    m.save(output_path)
    print(f"✅ Choropleth map saved: {output_path}")
    
    return output_path

# Usage
if __name__ == '__main__':
    create_choropleth_map(
        event_data_path='events_by_province.csv',
        geojson_path='admin_boundaries.geojson', 
        output_path='choropleth_map.html'
    )
```

## Common Issues and Solutions

### 1. Data Joining Problems
**Issue**: Events not matching to boundaries
**Solutions**:
- Verify coordinate validity (within expected geographic bounds)
- Check for null/invalid coordinates
- Ensure CRS consistency between datasets
- Use `ST_Within()` for point-in-polygon tests

### 2. GeoJSON Rendering Issues
**Issue**: Boundaries not displaying in Folium
**Solutions**:
- Validate GeoJSON format with online validators
- Check coordinate order (longitude, latitude)
- Simplify complex geometries if needed
- Verify feature properties contain required keys

### 3. Color Scale Problems
**Issue**: All regions same color
**Solutions**:
- Check data range (wide ranges may need log scaling)
- Verify data types (strings vs numbers)
- Use discrete color bins for wide ranges
- Test with different color schemes

### 4. Performance Issues
**Issue**: Large files causing slow rendering
**Solutions**:
- Simplify GeoJSON geometries
- Reduce coordinate precision
- Filter to relevant geographic area
- Use web-optimized file formats

## File Organization

### Recommended Structure
```
project/
├── data/
│   ├── raw/
│   │   ├── events.csv
│   │   └── boundaries.geojson
│   └── processed/
│       └── events_by_region.csv
├── maps/
│   └── choropleth_map.html
├── scripts/
│   ├── spatial_join.sql
│   └── create_choropleth.py
└── .claude/
    └── choropleth_mapping_guide.md
```

## Validation Checklist

### Before Creating Choropleth
- [ ] Event data has valid coordinates
- [ ] Boundaries render correctly in test map
- [ ] Spatial join produces expected results
- [ ] Region names match between datasets
- [ ] Data ranges are reasonable

### After Creating Choropleth  
- [ ] All regions display with appropriate colors
- [ ] Tooltips show correct information
- [ ] Color legend is meaningful
- [ ] Map centers and zooms properly
- [ ] Interactive features work

## Example Use Cases

### Military History Analysis
- Battle locations by administrative region
- Casualty counts by province/state
- Campaign intensity mapping

### Conflict Studies
- Incident frequency by district
- Violence patterns over time
- Displacement data visualization

### Historical Research
- Event density by geographic area
- Temporal patterns in spatial context
- Comparative regional analysis

## Advanced Features

### Temporal Animation
```python
# Add time slider for temporal analysis
from folium import plugins

# Create time-based data structure
time_data = []
for date in date_range:
    date_events = df[df['date'] == date]
    time_data.append({
        'date': date,
        'features': create_geojson_features(date_events)
    })

# Add TimestampedGeoJson
plugins.TimestampedGeoJson(
    time_data,
    period='P1M',  # Monthly intervals
    add_last_point=True
).add_to(m)
```

### Custom Popups
```python
# Rich popup content
popup_html = '''
<div style="width: 250px;">
    <h4>{region_name}</h4>
    <table>
        <tr><td>Events:</td><td>{event_count:,}</td></tr>
        <tr><td>Rank:</td><td>#{rank}</td></tr>
        <tr><td>Percentage:</td><td>{percentage:.1f}%</td></tr>
    </table>
</div>
'''

folium.Popup(
    popup_html.format(**region_data),
    max_width=300
).add_to(marker)
```

## Resources

### Documentation
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [DuckDB Spatial Extension](https://duckdb.org/docs/extensions/spatial)
- [GeoJSON Specification](https://geojson.org/)

### Tools
- [GeoJSON Validator](https://geojsonlint.com/)
- [Coordinate System Reference](https://epsg.io/)
- [Administrative Boundaries](https://www.geoboundaries.org/)

### Troubleshooting
- Always test with small datasets first
- Use browser developer tools to check for JavaScript errors
- Validate all intermediate data outputs
- Keep backups of working configurations

---

*Generated from successful Cambodia conflict events choropleth mapping project*