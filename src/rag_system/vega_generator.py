"""
VegaLiteGenerator - Generate Vega-Lite specifications for military data visualization
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class VegaLiteGenerator:
    """
    Generates Vega-Lite specifications for military historical data visualization.
    """
    
    def __init__(self):
        """Initialize the Vega-Lite generator."""
        self.military_colors = {
            'artillery': '#8B4513',      # Brown
            'air_mission': '#4169E1',    # Royal Blue  
            'ground_operation': '#228B22', # Forest Green
            'reconnaissance': '#8A2BE2',  # Blue Violet
            'naval': '#000080',          # Navy
            'default': '#2F4F4F'         # Dark Slate Gray
        }
        
        self.base_schema = "https://vega.github.io/schema/vega-lite/v5.json"
    
    def generate_spec(self, data: pd.DataFrame, viz_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Vega-Lite specification based on data and visualization type.
        
        Args:
            data: DataFrame with the data to visualize
            viz_type: Type of visualization (line_chart, bar_chart, scatter_plot, heatmap)
            context: Additional context for visualization customization
            
        Returns:
            Vega-Lite specification as dictionary
        """
        if data.empty:
            return self._empty_data_spec()
        
        # Route to appropriate template
        if viz_type == "line_chart":
            return self._temporal_line_template(data, context)
        elif viz_type == "bar_chart":
            return self._categorical_bar_template(data, context)
        elif viz_type == "scatter_plot":
            return self._correlation_scatter_template(data, context)
        elif viz_type == "heatmap":
            return self._temporal_heatmap_template(data, context)
        else:
            # Default to line chart for temporal data, bar chart otherwise
            return self._auto_detect_template(data, context)
    
    def _temporal_line_template(self, data: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate temporal line chart template."""
        date_col = self._find_date_column(data)
        metric_col = self._find_metric_column(data, context)
        category_col = self._find_category_column(data)
        
        if not date_col or not metric_col:
            return self._error_spec("Could not identify date or metric columns for temporal analysis")
        
        # Prepare data for visualization
        viz_data = self._prepare_temporal_data(data, date_col, metric_col, category_col)
        
        spec = {
            "$schema": self.base_schema,
            "title": {
                "text": context.get('title', 'Military Events Over Time'),
                "fontSize": 16,
                "anchor": "start",
                "color": "#2F4F4F"
            },
            "width": 800,
            "height": 400,
            "data": {"values": viz_data.to_dict('records')},
            "mark": {
                "type": "line",
                "point": True,
                "strokeWidth": 2,
                "interpolate": "monotone"
            },
            "encoding": {
                "x": {
                    "field": date_col,
                    "type": "temporal",
                    "title": "Date",
                    "axis": {"labelAngle": -45}
                },
                "y": {
                    "field": metric_col,
                    "type": "quantitative",
                    "title": context.get('y_title', 'Count')
                }
            }
        }
        
        # Add color encoding if category column exists
        if category_col and category_col in viz_data.columns:
            spec["encoding"]["color"] = {
                "field": category_col,
                "type": "nominal",
                "scale": {"scheme": "category10"},
                "title": category_col.replace('_', ' ').title()
            }
        
        return spec
    
    def _categorical_bar_template(self, data: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate categorical bar chart template."""
        category_col = self._find_category_column(data)
        metric_col = self._find_metric_column(data, context)
        
        if not category_col or not metric_col:
            return self._error_spec("Could not identify category or metric columns for comparison")
        
        # Aggregate data by category
        viz_data = data.groupby(category_col)[metric_col].sum().reset_index()
        viz_data = viz_data.sort_values(metric_col, ascending=False).head(20)  # Top 20 categories
        
        spec = {
            "$schema": self.base_schema,
            "title": {
                "text": context.get('title', f'{metric_col.replace("_", " ").title()} by {category_col.replace("_", " ").title()}'),
                "fontSize": 16,
                "anchor": "start",
                "color": "#2F4F4F"
            },
            "width": 600,
            "height": 400,
            "data": {"values": viz_data.to_dict('records')},
            "mark": {
                "type": "bar",
                "color": self.military_colors['default']
            },
            "encoding": {
                "x": {
                    "field": category_col,
                    "type": "nominal",
                    "title": category_col.replace('_', ' ').title(),
                    "axis": {"labelAngle": -45}
                },
                "y": {
                    "field": metric_col,
                    "type": "quantitative",
                    "title": context.get('y_title', metric_col.replace('_', ' ').title())
                }
            }
        }
        
        return spec
    
    def _correlation_scatter_template(self, data: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate correlation scatter plot template."""
        numeric_cols = self._find_numeric_columns(data)
        
        if len(numeric_cols) < 2:
            return self._error_spec("Need at least 2 numeric columns for correlation analysis")
        
        x_col = numeric_cols[0]
        y_col = numeric_cols[1]
        category_col = self._find_category_column(data)
        
        # Remove rows with null values in key columns
        viz_data = data[[x_col, y_col] + ([category_col] if category_col else [])].dropna()
        
        spec = {
            "$schema": self.base_schema,
            "title": {
                "text": context.get('title', f'{y_col.replace("_", " ").title()} vs {x_col.replace("_", " ").title()}'),
                "fontSize": 16,
                "anchor": "start",
                "color": "#2F4F4F"
            },
            "width": 600,
            "height": 400,
            "data": {"values": viz_data.to_dict('records')},
            "mark": {
                "type": "circle",
                "size": 60,
                "opacity": 0.7
            },
            "encoding": {
                "x": {
                    "field": x_col,
                    "type": "quantitative",
                    "title": x_col.replace('_', ' ').title()
                },
                "y": {
                    "field": y_col,
                    "type": "quantitative", 
                    "title": y_col.replace('_', ' ').title()
                }
            }
        }
        
        # Add color encoding if category column exists
        if category_col and category_col in viz_data.columns:
            spec["encoding"]["color"] = {
                "field": category_col,
                "type": "nominal",
                "scale": {"scheme": "category10"},
                "title": category_col.replace('_', ' ').title()
            }
        
        return spec
    
    def _temporal_heatmap_template(self, data: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate temporal heatmap template."""
        date_col = self._find_date_column(data)
        metric_col = self._find_metric_column(data, context)
        
        if not date_col or not metric_col:
            return self._error_spec("Could not identify date or metric columns for heatmap")
        
        # Create temporal aggregations
        viz_data = self._prepare_heatmap_data(data, date_col, metric_col)
        
        spec = {
            "$schema": self.base_schema,
            "title": {
                "text": context.get('title', 'Military Activity Heatmap'),
                "fontSize": 16,
                "anchor": "start",
                "color": "#2F4F4F"
            },
            "width": 800,
            "height": 400,
            "data": {"values": viz_data.to_dict('records')},
            "mark": "rect",
            "encoding": {
                "x": {
                    "field": "month",
                    "type": "ordinal",
                    "title": "Month"
                },
                "y": {
                    "field": "year",
                    "type": "ordinal",
                    "title": "Year"
                },
                "color": {
                    "field": metric_col,
                    "type": "quantitative",
                    "scale": {"scheme": "reds"},
                    "title": "Activity Level"
                }
            }
        }
        
        return spec
    
    def _auto_detect_template(self, data: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-detect appropriate template based on data characteristics."""
        date_col = self._find_date_column(data)
        numeric_cols = self._find_numeric_columns(data)
        category_col = self._find_category_column(data)
        
        if date_col and len(numeric_cols) > 0:
            # Temporal data - use line chart
            return self._temporal_line_template(data, context)
        elif category_col and len(numeric_cols) > 0:
            # Categorical data - use bar chart
            return self._categorical_bar_template(data, context)
        elif len(numeric_cols) >= 2:
            # Multiple numeric columns - use scatter plot
            return self._correlation_scatter_template(data, context)
        else:
            return self._error_spec("Could not determine appropriate visualization type for this data")
    
    def _find_date_column(self, data: pd.DataFrame) -> Optional[str]:
        """Find the primary date column in the data."""
        date_patterns = [
            'date', 'time', 'incident_date', 'event_date', 'date_incident', 
            'timestamp', 'datetime', 'occurred', 'when'
        ]
        
        for col in data.columns:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in date_patterns):
                # Check if it's actually date-like data
                if pd.api.types.is_datetime64_any_dtype(data[col]) or self._looks_like_date(data[col]):
                    return col
        
        return None
    
    def _find_metric_column(self, data: pd.DataFrame, context: Dict[str, Any]) -> Optional[str]:
        """Find the primary metric column for visualization."""
        # Check context for explicit metric
        if 'metric_field' in context:
            return context['metric_field']
        
        # Look for common military metrics
        metric_patterns = [
            'count', 'casualty', 'killed', 'wounded', 'total', 'frequency',
            'duration', 'intensity', 'rounds', 'missions', 'incidents'
        ]
        
        numeric_cols = self._find_numeric_columns(data)
        
        for col in numeric_cols:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in metric_patterns):
                return col
        
        # If no obvious metric, use first numeric column or count
        if numeric_cols:
            return numeric_cols[0]
        
        # Create a count column if no numeric data
        return 'count'
    
    def _find_category_column(self, data: pd.DataFrame) -> Optional[str]:
        """Find the primary categorical column."""
        category_patterns = [
            'province', 'operation', 'unit', 'type', 'category', 'name',
            'ship', 'location', 'region', 'command', 'service'
        ]
        
        for col in data.columns:
            if data[col].dtype == 'object' or data[col].dtype.name == 'category':
                col_lower = col.lower()
                if any(pattern in col_lower for pattern in category_patterns):
                    return col
        
        # Return first categorical column if no obvious pattern match
        for col in data.columns:
            if data[col].dtype == 'object' and data[col].nunique() < len(data) * 0.8:
                return col
        
        return None
    
    def _find_numeric_columns(self, data: pd.DataFrame) -> List[str]:
        """Find all numeric columns in the data."""
        numeric_cols = []
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                numeric_cols.append(col)
        return numeric_cols
    
    def _looks_like_date(self, series: pd.Series) -> bool:
        """Check if a series contains date-like strings."""
        if series.dtype != 'object':
            return False
        
        # Sample some non-null values
        sample = series.dropna().head(10)
        if len(sample) == 0:
            return False
        
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]
        
        matches = 0
        for value in sample:
            str_value = str(value)
            if any(re.search(pattern, str_value) for pattern in date_patterns):
                matches += 1
        
        return matches / len(sample) > 0.5
    
    def _prepare_temporal_data(self, data: pd.DataFrame, date_col: str, metric_col: str, category_col: Optional[str]) -> pd.DataFrame:
        """Prepare data for temporal visualization."""
        # Convert date column
        if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
            data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
        
        # If metric_col doesn't exist, create count
        if metric_col == 'count' or metric_col not in data.columns:
            if category_col:
                viz_data = data.groupby([date_col, category_col]).size().reset_index(name='count')
                metric_col = 'count'
            else:
                viz_data = data.groupby(date_col).size().reset_index(name='count')
                metric_col = 'count'
        else:
            # Aggregate by date (and category if available)
            if category_col:
                viz_data = data.groupby([date_col, category_col])[metric_col].sum().reset_index()
            else:
                viz_data = data.groupby(date_col)[metric_col].sum().reset_index()
        
        return viz_data
    
    def _prepare_heatmap_data(self, data: pd.DataFrame, date_col: str, metric_col: str) -> pd.DataFrame:
        """Prepare data for heatmap visualization."""
        # Convert date column
        if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
            data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
        
        # Extract year and month
        data['year'] = data[date_col].dt.year
        data['month'] = data[date_col].dt.month
        
        # If metric_col doesn't exist, create count
        if metric_col == 'count' or metric_col not in data.columns:
            viz_data = data.groupby(['year', 'month']).size().reset_index(name='count')
            metric_col = 'count'
        else:
            viz_data = data.groupby(['year', 'month'])[metric_col].sum().reset_index()
        
        # Convert month to name
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                      7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        viz_data['month'] = viz_data['month'].map(month_names)
        
        return viz_data
    
    def _empty_data_spec(self) -> Dict[str, Any]:
        """Return specification for empty data."""
        return {
            "$schema": self.base_schema,
            "title": "No Data Available",
            "width": 400,
            "height": 200,
            "mark": {"type": "text", "text": "No data available for visualization", "fontSize": 16, "color": "gray"},
            "data": {"values": [{}]}
        }
    
    def _error_spec(self, error_message: str) -> Dict[str, Any]:
        """Return specification for error state."""
        return {
            "$schema": self.base_schema,
            "title": "Visualization Error",
            "width": 400,
            "height": 200,
            "mark": {"type": "text", "text": error_message, "fontSize": 14, "color": "red"},
            "data": {"values": [{}]}
        }