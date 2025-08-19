# Military History Visualization RAG System - Claude Code Instructions

## 1. Project Overview
Create a RAG (Retrieval-Augmented Generation) system that generates Vega-Lite specifications and Folium maps from natural language queries over a DuckDB database containing military historical data (58 datasets, 500K+ records from 1967-2004).

## 2. System Architecture

### 2.1 Core Components
1. **Vector Store**: ChromaDB for storing visualization patterns and schema embeddings
2. **Query Processing**: Natural language to SQL translation
3. **Visualization Generation**: 
   - Vega-Lite specifications for charts/plots
   - Folium maps for geographic visualizations
4. **Data Source**: Existing DuckDB database with military datasets

### 2.2 File Structure
src/
├── rag_system/
│   ├── init.py
│   ├── military_viz_rag.py          # Main RAG system
│   ├── vega_generator.py            # Vega-Lite spec generation
│   ├── folium_generator.py          # Folium map generation
│   ├── query_processor.py           # NL to SQL translation
│   └── main_interface.py            # Public API interface
├── templates/
│   ├── vega_templates.json          # Predefined Vega-Lite templates
│   └── map_styles.json              # Map styling configurations
├── config/
│   ├── military_terms.json          # Military terminology mappings
│   └── visualization_patterns.json  # Viz pattern definitions
└── tests/
├── test_vega_generation.py
├── test_folium_generation.py
└── test_integration.py

## 3. Core Classes and Methods

### 3.1 MilitaryVizRAG (`military_viz_rag.py`)
```python
class MilitaryVizRAG:
    def __init__(self, duckdb_path: str)
    def _initialize_vector_store(self) -> chromadb.Collection
    def _build_viz_knowledge_base(self) -> None
    def query_visualization_patterns(self, query: str) -> Dict
    def get_table_schema(self, table_name: str) -> Dict
```

#### 3.1.1 Key Features
- Initialize ChromaDB with visualization patterns
- Store embeddings for chart types, map types, and data requirements
- Pattern matching for query intent recognition

### 3.2 VegaLiteGenerator (`vega_generator.py`)
```python
class VegaLiteGenerator:
    def __init__(self)
    def generate_spec(self, data: pd.DataFrame, viz_type: str, context: Dict) -> Dict
    def _temporal_line_template(self, data: pd.DataFrame, context: Dict) -> Dict
    def _categorical_bar_template(self, data: pd.DataFrame, context: Dict) -> Dict
    def _correlation_scatter_template(self, data: pd.DataFrame, context: Dict) -> Dict
    def _temporal_heatmap_template(self, data: pd.DataFrame, context: Dict) -> Dict
    def _auto_detect_columns(self, data: pd.DataFrame, context: Dict) -> Dict
```

#### 3.2.1 Template Types
- **Temporal Line**: Time series analysis of military events
- **Categorical Bar**: Comparisons by province, operation type, etc.
- **Scatter Plot**: Correlation analysis (casualties vs duration, etc.)
- **Heatmap**: Temporal patterns (month vs year activity)
- **Geographic Points**: Coordinate-based visualizations

### 3.3 FoliumMapGenerator (`folium_generator.py`)
```python
class FoliumMapGenerator:
    def __init__(self)
    def generate_map(self, data: pd.DataFrame, map_type: str, context: Dict) -> folium.Map
    def _create_density_map(self, data: pd.DataFrame, context: Dict) -> folium.Map
    def _create_heatmap(self, data: pd.DataFrame, context: Dict) -> folium.Map
    def _create_clustered_map(self, data: pd.DataFrame, context: Dict) -> folium.Map
    def _create_timeline_map(self, data: pd.DataFrame, context: Dict) -> folium.Map
    def _create_military_popup(self, row: pd.Series) -> str
```

#### 3.3.1 Map Types
- **Density Maps**: Point markers with military-specific icons and colors
- **Heatmaps**: Intensity visualization based on casualties or event frequency
- **Clustered Maps**: DBSCAN clustering of geographic events
- **Timeline Maps**: Animated temporal progression of events

### 3.4 QueryProcessor (`query_processor.py`)
```python
```python
class QueryProcessor:
    def __init__(self, rag_system: MilitaryVizRAG)
    def process_natural_language(self, query: str) -> Dict
    def _extract_military_entities(self, query: str) -> Dict
    def _extract_temporal_info(self, query: str) -> Dict
    def _extract_spatial_info(self, query: str) -> Dict
    def _generate_sql_query(self, entities: Dict, context: Dict) -> str
    def _determine_visualization_type(self, query: str, entities: Dict) -> str
```

#### 3.4.1 Entity Extraction
- **Military Terms**: artillery, air mission, ground operation, incident
- **Geographic**: Cambodia, Vietnam, Laos, provinces, coordinates
- **Temporal**: years (1967-2004), months, date ranges
- **Metrics**: casualties, duration, intensity, frequency

## 4. Implementation Details

### 4.1 Vector Store Schema

#### Entity Extraction:

Military Terms: artillery, air mission, ground operation, incident
Geographic: Cambodia, Vietnam, Laos, provinces, coordinates
Temporal: years (1967-2004), months, date ranges
Metrics: casualties, duration, intensity, frequency

#### Implementation Details
#### Vector Store Schema
```python
visualization_patterns = [
    {
        "description": "temporal analysis of military incidents over time",
        "viz_type": "line_chart",
        "data_requirements": ["date_field", "count_or_metric"],
        "keywords": ["over time", "temporal", "trend", "timeline"]
    },
    {
        "description": "geographic distribution of military events on map",
        "viz_type": "folium_map", 
        "data_requirements": ["latitude", "longitude", "event_data"],
        "keywords": ["geographic", "spatial", "map", "location", "where"]
    }
    # ... more patterns
]
```

### 4.2 SQL Query Generation Logic
```python
def _generate_sql_from_query(self, query: str, context: Dict) -> str:
    # Base query structure
    base_query = "SELECT * FROM military_events"
    conditions = []
    
    # Geographic filters
    if 'cambodia' in query.lower():
        conditions.append("country = 'Cambodia'")
    
    # Temporal filters  
    year_match = re.search(r'(\d{4})', query)
    if year_match:
        conditions.append(f"EXTRACT(year FROM incident_date) = {year_match.group(1)}")
    
    # Operation type filters
    if 'artillery' in query.lower():
        conditions.append("operation_type LIKE '%artillery%'")
    
    # Casualty filters
    if 'high casualt' in query.lower():
        conditions.append("casualty_count > 10")
    
    # Combine conditions
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    return base_query + " LIMIT 1000"
```

## 5. Template Examples

### 5.1 Vega-Lite Template Example
```python
def _temporal_line_template(self, data: pd.DataFrame, context: Dict) -> Dict:
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": f"Military Events: {context.get('title', 'Temporal Analysis')}",
        "width": 800,
        "height": 400,
        "data": {"values": data.to_dict('records')},
        "mark": {"type": "line", "point": True, "strokeWidth": 2, "color": "#8B4513"},
        "encoding": {
            "x": {
                "field": self._find_date_column(data),
                "type": "temporal",
                "title": "Date"
            },
            "y": {
                "field": self._find_metric_column(data, context),
                "type": "quantitative", 
                "title": "Count"
            },
            "color": {
                "field": "operation_type",
                "type": "nominal",
                "scale": {"scheme": "category10"}
            }
        }
    }
```

### 5.2 Folium Map Styling
```python
def _create_density_map(self, data: pd.DataFrame, context: Dict) -> folium.Map:
    # Military-specific color scheme
    operation_colors = {
        'artillery': 'red',
        'air_mission': 'blue', 
        'ground_operation': 'green',
        'reconnaissance': 'purple'
    }
    
    # Military-style markers
    for idx, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=self._create_military_popup(row),
            icon=folium.Icon(
                color=operation_colors.get(row['operation_type'], 'gray'),
                icon='crosshairs',
                prefix='fa'
            )
        ).add_to(map)

    return map
```

## 6. Technical Requirements

### 6.1 Dependencies
```python
# requirements.txt
duckdb>=0.9.0
pandas>=2.0.0
folium>=0.14.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
altair>=5.0.0  # For Vega-Lite validation
numpy>=1.24.0
```

### 6.2 Data Requirements
- **Spatial Data**: latitude, longitude columns
- **Temporal Data**: Date columns (incident_date, event_date, etc.)
- **Categorical Data**: operation_type, province, unit, etc.
- **Metrics**: casualty_count, duration, intensity, etc.

### 6.3 Military-Specific Features
- **Terminology Recognition**: Artillery, air missions, ground operations, incidents
- **Geographic Context**: Vietnam, Cambodia, Laos provinces and regions
- **Temporal Context**: Vietnam War era (1967-2004)
- **Visual Styling**: Military color schemes, appropriate icons
- **Casualty Analysis**: High/medium/low casualty classifications

## 7. Usage Examples

### 7.1 Natural Language Queries
```python
example_queries = [
    "Show artillery missions in Cambodia over time",
    "Map all high-casualty incidents in Vietnam",  
    "Compare operation types by casualty count",
    "Show heatmap of military activity in 1971",
    "Timeline of air missions in Laos",
    "Scatter plot of duration vs casualties",
    "Bar chart of incidents by province"
]
```

### 7.2 API Interface
```python
# Main interface
interface = MilitaryVizInterface("path/to/military_history.db")

result = interface.create_visualization("Show artillery missions in Cambodia over time")

# Returns:
{
    'type': 'vega_lite',  # or 'folium_map'
    'spec': {...},        # Vega-Lite JSON spec
    'data_summary': {
        'total_records': 1250,
        'date_range': '1970-01-01 to 1975-12-31',
        'geographic_scope': '5 provinces'
    },
    'sql_used': "SELECT * FROM military_events WHERE..."
}
```

## 8. Testing Strategy

### 8.1 Unit Tests
- Test each visualization template with sample data
- Test SQL generation for various query patterns
- Test entity extraction accuracy
- Test map generation with different data sizes

### 8.2 Integration Tests
- End-to-end query processing
- Vega-Lite spec validation
- Folium map rendering verification
- Performance testing with large datasets

### 8.3 Example Test Cases
```python
def test_artillery_query():
    query = "Show artillery missions in Cambodia"
    result = interface.create_visualization(query)
    assert result['type'] == 'folium_map'
    assert 'artillery' in result['sql_used'].lower()
    assert 'cambodia' in result['sql_used'].lower()

def test_temporal_chart():
    query = "Military events over time"
    result = interface.create_visualization(query)
    assert result['type'] == 'vega_lite'
    assert result['spec']['mark']['type'] == 'line'
```

## 9. Configuration Files

### 9.1 Military Terms Mapping (`military_terms.json`)
```json
{
    "operation_types": {
        "artillery": ["artillery", "firing", "bombardment", "shelling"],
        "air_mission": ["air", "bombing", "airstrike", "aircraft"],
        "ground_operation": ["patrol", "sweep", "ground", "infantry"]
    },
    "casualty_levels": {
        "high": [">10", "heavy", "significant"],
        "medium": ["5-10", "moderate"],
        "low": ["<5", "light", "minimal"]
    }
}
```

### 9.2 Visualization Patterns (`visualization_patterns.json`)
```json
{
    "patterns": [
        {
            "name": "temporal_analysis",
            "description": "Analysis of military events over time periods",
            "viz_type": "line_chart",
            "triggers": ["over time", "temporal", "trend", "timeline", "chronological"],
            "data_requirements": ["date_field", "metric_field"],
            "best_for": ["incident frequency", "casualty trends", "operation patterns"]
        },
        {
            "name": "geographic_distribution", 
            "description": "Spatial distribution of military events",
            "viz_type": "folium_map",
            "triggers": ["map", "geographic", "spatial", "location", "where"],
            "data_requirements": ["latitude", "longitude", "event_data"],
            "best_for": ["event locations", "geographic patterns", "spatial clustering"]
        },
        {
            "name": "categorical_comparison",
            "description": "Comparison across categories like provinces or operation types",
            "viz_type": "bar_chart", 
            "triggers": ["compare", "by province", "by type", "breakdown"],
            "data_requirements": ["category_field", "metric_field"],
            "best_for": ["province comparisons", "operation type analysis", "unit performance"]
        },
        {
            "name": "correlation_analysis",
            "description": "Relationship between two numerical variables",
            "viz_type": "scatter_plot",
            "triggers": ["correlation", "relationship", "vs", "versus", "against"],
            "data_requirements": ["numeric_x", "numeric_y", "optional_category"],
            "best_for": ["casualty vs duration", "intensity relationships", "effectiveness metrics"]
        },
        {
            "name": "activity_heatmap",
            "description": "Intensity patterns across time and space",
            "viz_type": "heatmap",
            "triggers": ["heatmap", "intensity", "activity level", "density", "heat"],
            "data_requirements": ["time_dimension", "space_dimension", "intensity_metric"],
            "best_for": ["activity patterns", "seasonal trends", "geographic hotspots"]
        }
    ]
}
```

## 10. Error Handling and Validation

### 10.1 Query Validation
```python
def validate_query(self, query: str) -> Dict[str, Any]:
    """Validate and provide feedback on user queries"""
    validation_result = {
        'is_valid': True,
        'warnings': [],
        'suggestions': []
    }
    
    # Check for geographic entities
    if not any(geo in query.lower() for geo in ['cambodia', 'vietnam', 'laos']):
        validation_result['warnings'].append("No geographic region specified")
        validation_result['suggestions'].append("Consider adding: 'in Cambodia', 'in Vietnam', etc.")
    
    # Check for temporal context
    if not any(temp in query.lower() for temp in ['time', 'year', '19']):
        validation_result['suggestions'].append("Consider adding temporal context: 'over time', 'in 1971', etc.")
    
    return validation_result
```

### 10.2 Data Quality Checks
```python
def validate_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
    """Check data quality before visualization"""
    quality_report = {
        'total_records': len(data),
        'missing_coordinates': 0,
        'missing_dates': 0,
        'data_quality_score': 1.0
    }
    
    # Check spatial data completeness
    if 'latitude' in data.columns and 'longitude' in data.columns:
        missing_coords = data[['latitude', 'longitude']].isnull().any(axis=1).sum()
        quality_report['missing_coordinates'] = missing_coords
        quality_report['data_quality_score'] -= (missing_coords / len(data)) * 0.3
    
    # Check temporal data completeness
    date_cols = [col for col in data.columns if 'date' in col.lower()]
    if date_cols:
        missing_dates = data[date_cols[0]].isnull().sum()
        quality_report['missing_dates'] = missing_dates
        quality_report['data_quality_score'] -= (missing_dates / len(data)) * 0.2
    
    return quality_report
```