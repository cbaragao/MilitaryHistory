# Military Visualization RAG System - Usage Instructions

## Overview

The Military Visualization RAG (Retrieval-Augmented Generation) system transforms natural language queries into interactive visualizations of military historical data. It combines ChromaDB vector search, DuckDB SQL execution, and specialized generators for Vega-Lite charts and Folium maps.

## Quick Start

### 1. Basic Setup

```python
from src.rag_system import MilitaryVizInterface

# Initialize the system
viz_interface = MilitaryVizInterface("path/to/your/military_data.db")

# Process a simple query
result = viz_interface.process_query("Show artillery incidents over time")

print(f"Success: {result['success']}")
print(f"Data shape: {result['metadata']['data_shape']}")
print(f"Visualization saved to: {result['visualization']['path']}")
```

### 2. Query Examples

**Temporal Analysis:**
```python
# Time series analysis
result = viz_interface.process_query("Show HOSTA incidents from 1968 to 1972")
result = viz_interface.process_query("Plot casualty trends by month")
result = viz_interface.process_query("Display operation frequency timeline")
```

**Geographic Visualization:**
```python
# Interactive maps
result = viz_interface.process_query("Map incident locations in Cambodia")
result = viz_interface.process_query("Show geographic distribution of naval attacks")
result = viz_interface.process_query("Plot coordinates of artillery strikes")
```

**Categorical Comparison:**
```python
# Bar charts and comparisons
result = viz_interface.process_query("Compare incidents by province")
result = viz_interface.process_query("Show breakdown by operation type")
result = viz_interface.process_query("Chart casualties by ship")
```

**Correlation Analysis:**
```python
# Scatter plots and relationships
result = viz_interface.process_query("Plot casualties vs mission duration")
result = viz_interface.process_query("Show relationship between intensity and damage")
result = viz_interface.process_query("Correlate frequency with effectiveness")
```

**Activity Heatmaps:**
```python
# Intensity patterns
result = viz_interface.process_query("Create activity heatmap by month and year")
result = viz_interface.process_query("Show intensity patterns over time")
result = viz_interface.process_query("Display geographic heat zones")
```

## Advanced Usage

### 3. Working with Query Results

```python
result = viz_interface.process_query("Map naval incidents in 1970")

if result['success']:
    # Access the data
    data = result['data']
    print(f"Found {len(data)} records")
    print(data.head())
    
    # Get visualization info
    viz = result['visualization']
    if viz['type'] == 'folium_map':
        print(f"Interactive map saved to: {viz['path']}")
    elif viz['type'] == 'vega_lite':
        print(f"Chart specification: {viz['spec']}")
        print(f"Saved to: {viz['path']}")
    
    # Check processing details
    processed = result['metadata']['processed_query']
    print(f"SQL executed: {processed['sql_query']}")
    print(f"Confidence: {processed['confidence']}")
    print(f"Entities found: {processed['entities']}")
```

### 4. Getting Suggestions

```python
# Get query suggestions
suggestions = viz_interface.get_suggestions("show incidents")

for suggestion in suggestions:
    print(f"Query: {suggestion['query']}")
    print(f"Pattern: {suggestion['pattern']}")
    print(f"Description: {suggestion['description']}")
    print()
```

### 5. Exploring Available Data

```python
# Get data source information
data_info = viz_interface.get_available_data()

print(f"Total tables: {data_info['total_tables']}")
print(f"Total records: {data_info['total_records']}")

for table, info in data_info['tables'].items():
    print(f"\n{table}:")
    print(f"  Rows: {info['row_count']}")
    print(f"  Columns: {', '.join(info['columns'][:5])}")  # First 5 columns
```

## Query Language Guide

### 6. Effective Query Patterns

**Time-based Queries:**
- "Show [data] over time"
- "Plot [metric] from [year] to [year]"
- "Display [events] timeline"
- "Chart [activity] by month/year"

**Geographic Queries:**
- "Map [events] in [location]"
- "Show [data] locations"
- "Plot [incidents] on map"
- "Display geographic distribution of [events]"

**Comparison Queries:**
- "Compare [metric] by [category]"
- "Show breakdown by [field]"
- "Chart [data] by [grouping]"
- "Breakdown of [events] by [dimension]"

**Correlation Queries:**
- "[metric1] vs [metric2]"
- "Relationship between [field1] and [field2]"
- "Correlate [variable1] with [variable2]"
- "Plot [x] against [y]"

### 7. Query Optimization Tips

**Be Specific with Time Ranges:**
```python
# Good
"Show HOSTA incidents from 1968 to 1970"

# Less effective
"Show incidents sometime in the late 60s"
```

**Use Military Terminology:**
```python
# Good - uses recognized terms
"Map artillery bombardments in Binh Dinh province"

# Less effective - generic terms
"Show shooting events in that area"
```

**Specify Data Sources When Needed:**
```python
# Good - targets specific dataset
"Plot HOSTA naval incidents over time"

# Less effective - ambiguous
"Show some boat stuff"
```

## Configuration and Customization

### 8. Custom Visualization Patterns

Edit `src/config/visualization_patterns.json` to add new patterns:

```json
{
  "name": "custom_analysis",
  "description": "Your custom analysis description",
  "viz_type": "bar_chart",
  "triggers": ["custom", "special", "unique"],
  "data_requirements": ["category_field", "metric_field"],
  "best_for": ["custom use cases"],
  "examples": ["Show custom analysis", "Display special breakdown"]
}
```

### 9. Military Terms Dictionary

Extend `src/config/military_terms.json` for better entity recognition:

```json
{
  "operation_types": {
    "your_operation": ["keyword1", "keyword2", "keyword3"]
  },
  "custom_units": {
    "special_forces": ["sf", "green berets", "special ops"]
  }
}
```

## Output Management

### 10. Visualization Files

**Vega-Lite Charts:**
- Saved as JSON specifications in `visuals/vega_*.json`
- Can be viewed at [Vega Editor](https://vega.github.io/editor/)
- Embed in web pages with Vega-Lite JavaScript library

**Folium Maps:**
- Saved as HTML files in `visuals/map_*.html`
- Open directly in web browser
- Fully interactive with zoom, pan, popups

### 11. Programmatic Access

```python
# Don't save files, work with objects directly
result = viz_interface.process_query("Map incidents", save_output=False)

if result['visualization']['type'] == 'folium_map':
    map_obj = result['visualization']['object']
    # Use map_obj directly for custom display
    
elif result['visualization']['type'] == 'vega_lite':
    spec = result['visualization']['spec']
    # Use spec for custom rendering
```

## Troubleshooting

### 12. Common Issues

**No Data Returned:**
- Check table names with `get_available_data()`
- Verify date ranges are valid
- Ensure geographic filters match data

**Poor Query Understanding:**
- Use more specific military terminology
- Check entity recognition with result metadata
- Try alternative phrasings

**Visualization Errors:**
- Verify required columns exist for visualization type
- Check data types (dates, coordinates, numbers)
- Review query result structure

### 13. Debug Information

```python
result = viz_interface.process_query("your query")

# Check processing details
processed = result['metadata']['processed_query']
print(f"Entities found: {processed['entities']}")
print(f"Table selected: {processed['table_name']}")
print(f"SQL generated: {processed['sql_query']}")
print(f"Confidence score: {processed['confidence']}")

# Check for errors
if result['errors']:
    for error in result['errors']:
        print(f"Error: {error}")
```

## Best Practices

### 14. Query Strategy

1. **Start Simple:** Begin with basic queries to understand your data
2. **Be Specific:** Use precise military terms and date ranges
3. **Iterate:** Refine queries based on initial results
4. **Explore:** Use suggestions to discover new query patterns

### 15. Performance Tips

1. **Limit Date Ranges:** Large time spans may be slow
2. **Use Filters:** Geographic and categorical filters improve speed
3. **Cache Results:** Save intermediate results for complex analysis
4. **Monitor Confidence:** Low confidence scores indicate unclear queries

### 16. Integration Patterns

**Jupyter Notebooks:**
```python
# Display results inline
result = viz_interface.process_query("Map HOSTA incidents")
from IPython.display import IFrame
IFrame(result['visualization']['path'], width=800, height=600)
```

**Web Applications:**
```python
# Return JSON for web frontend
result = viz_interface.process_query(user_query, save_output=False)
return {
    'success': result['success'],
    'data': result['data'].to_dict('records'),
    'visualization': result['visualization']['spec']  # For Vega-Lite
}
```

**Batch Processing:**
```python
queries = [
    "Show incidents over time",
    "Map locations by province", 
    "Compare by operation type"
]

results = []
for query in queries:
    result = viz_interface.process_query(query)
    results.append({
        'query': query,
        'path': result['visualization']['path'],
        'success': result['success']
    })
```

## System Limits and Considerations

- **Data Size:** Large datasets (>100k records) may require query optimization
- **Memory Usage:** Maps with >1000 points may be slow to render
- **Dependencies:** Requires ChromaDB, sentence-transformers, folium, duckdb
- **Geographic Data:** Coordinate validation and cleaning is automatic
- **Date Parsing:** Flexible date format handling with pandas

---

**Need Help?** Check the examples above or explore with `get_suggestions()` to discover query patterns that work with your specific military datasets.