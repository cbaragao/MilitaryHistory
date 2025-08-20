"""
FoliumMapGenerator - Generate interactive maps for military data visualization
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
try:
    import folium
    from folium import plugins
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    print("Warning: Folium not available. Install with: pip install folium")

try:
    from sklearn.cluster import DBSCAN
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: scikit-learn not available for clustering. Install with: pip install scikit-learn")


class FoliumMapGenerator:
    """
    Generates interactive Folium maps for military historical data visualization.
    """
    
    def __init__(self):
        """Initialize the Folium map generator."""
        if not FOLIUM_AVAILABLE:
            raise ImportError("Folium is required. Install with: pip install folium")
            
        # Military-specific styling
        self.operation_colors = {
            'artillery': 'red',
            'air_mission': 'blue', 
            'ground_operation': 'green',
            'reconnaissance': 'purple',
            'naval': 'darkblue',
            'incident': 'orange',
            'default': 'gray'
        }
        
        self.military_icons = {
            'artillery': 'crosshairs',
            'air_mission': 'plane',
            'ground_operation': 'male',
            'reconnaissance': 'search',
            'naval': 'anchor',
            'incident': 'exclamation-triangle',
            'default': 'info-sign'
        }
        
        # Default map centers for common regions
        self.region_centers = {
            'vietnam': [16.0, 108.0],
            'cambodia': [12.5, 105.0],
            'laos': [18.0, 105.0],
            'southeast_asia': [15.0, 107.0]
        }
    
    def generate_map(self, data: pd.DataFrame, map_type: str, context: Dict[str, Any]) -> folium.Map:
        """
        Generate interactive map based on data and map type.
        
        Args:
            data: DataFrame with geographic data
            map_type: Type of map (density, heatmap, clustered, timeline)
            context: Additional context for map customization
            
        Returns:
            Folium map object
        """
        if not FOLIUM_AVAILABLE:
            raise RuntimeError("Folium not available")
            
        if data.empty:
            return self._empty_map(context)
        
        # Validate geographic data
        lat_col, lon_col = self._find_coordinate_columns(data)
        if not lat_col or not lon_col:
            return self._error_map("No valid coordinate columns found")
        
        # Route to appropriate map type
        if map_type == "density" or map_type == "markers":
            return self._create_density_map(data, lat_col, lon_col, context)
        elif map_type == "heatmap":
            return self._create_heatmap(data, lat_col, lon_col, context)
        elif map_type == "clustered":
            return self._create_clustered_map(data, lat_col, lon_col, context)
        elif map_type == "timeline":
            return self._create_timeline_map(data, lat_col, lon_col, context)
        else:
            # Default to density map
            return self._create_density_map(data, lat_col, lon_col, context)
    
    def _create_density_map(self, data: pd.DataFrame, lat_col: str, lon_col: str, context: Dict[str, Any]) -> folium.Map:
        """Create density map with point markers."""
        # Clean coordinate data
        clean_data = self._clean_coordinate_data(data, lat_col, lon_col)
        if clean_data.empty:
            return self._error_map("No valid coordinates after cleaning")
        
        # Calculate map center and zoom
        center_lat, center_lon = self._calculate_map_center(clean_data, lat_col, lon_col, context)
        zoom_level = self._calculate_zoom_level(clean_data, lat_col, lon_col)
        
        # Create base map with more compatible settings
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_level,
            tiles='OpenStreetMap',
            prefer_canvas=True  # Better performance and compatibility
        )
        
        # Use simple CircleMarkers for better compatibility and performance
        for idx, row in clean_data.iterrows():
            # Limit to first 500 points for performance
            if idx >= 500:
                break
                
            # Determine marker style
            operation_col = self._find_operation_column(clean_data)
            operation_type = 'default'
            if operation_col and pd.notna(row[operation_col]):
                operation_type = str(row[operation_col]).lower()
                
            color = self._get_operation_color(operation_type)
            
            # Create popup content
            popup_content = self._create_military_popup(row)
            
            # Use simple CircleMarkers to avoid zIndex issues
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=6,
                popup=folium.Popup(popup_content, max_width=250),
                tooltip=self._create_tooltip(row),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2,
                opacity=0.8
            ).add_to(m)
        
        return m
    
    def _create_heatmap(self, data: pd.DataFrame, lat_col: str, lon_col: str, context: Dict[str, Any]) -> folium.Map:
        """Create heatmap visualization."""
        # Clean coordinate data
        clean_data = self._clean_coordinate_data(data, lat_col, lon_col)
        if clean_data.empty:
            return self._error_map("No valid coordinates for heatmap")
        
        # Calculate map center
        center_lat, center_lon = self._calculate_map_center(clean_data, lat_col, lon_col, context)
        
        # Create base map with compatibility settings
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=8,
            tiles='CartoDB positron',
            prefer_canvas=True
        )
        
        # Prepare heatmap data
        heat_data = []
        weight_col = self._find_weight_column(clean_data, context)
        
        for idx, row in clean_data.iterrows():
            weight = 1.0  # Default weight
            if weight_col and pd.notna(row[weight_col]):
                weight = float(row[weight_col])
            
            heat_data.append([row[lat_col], row[lon_col], weight])
        
        # Add heatmap layer
        if heat_data:
            heatmap = plugins.HeatMap(
                heat_data,
                gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'},
                min_opacity=0.5,
                max_zoom=18,
                radius=15,
                blur=10
            )
            heatmap.add_to(m)
        
        return m
    
    def _create_clustered_map(self, data: pd.DataFrame, lat_col: str, lon_col: str, context: Dict[str, Any]) -> folium.Map:
        """Create map with spatial clustering."""
        if not SKLEARN_AVAILABLE:
            return self._error_map("Clustering requires scikit-learn. Install with: pip install scikit-learn")
        
        # Clean coordinate data
        clean_data = self._clean_coordinate_data(data, lat_col, lon_col)
        if clean_data.empty:
            return self._error_map("No valid coordinates for clustering")
        
        # Calculate map center
        center_lat, center_lon = self._calculate_map_center(clean_data, lat_col, lon_col, context)
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=8,
            tiles='OpenStreetMap'
        )
        
        # Perform DBSCAN clustering
        coordinates = clean_data[[lat_col, lon_col]].values
        eps = context.get('cluster_eps', 0.1)  # ~11km at equator
        min_samples = context.get('cluster_min_samples', 3)
        
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coordinates)
        clean_data['cluster'] = clustering.labels_
        
        # Color map for clusters
        unique_clusters = clean_data['cluster'].unique()
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 
                 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 
                 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
        
        # Add clustered markers
        for cluster_id in unique_clusters:
            cluster_data = clean_data[clean_data['cluster'] == cluster_id]
            color = colors[cluster_id % len(colors)] if cluster_id != -1 else 'black'
            
            for idx, row in cluster_data.iterrows():
                popup_content = self._create_military_popup(row)
                popup_content += f"<br><b>Cluster:</b> {cluster_id if cluster_id != -1 else 'Noise'}"
                
                folium.CircleMarker(
                    location=[row[lat_col], row[lon_col]],
                    radius=5,
                    popup=folium.Popup(popup_content, max_width=300),
                    color=color,
                    fill=True,
                    opacity=0.7
                ).add_to(m)
        
        return m
    
    def _create_timeline_map(self, data: pd.DataFrame, lat_col: str, lon_col: str, context: Dict[str, Any]) -> folium.Map:
        """Create timeline map with temporal progression."""
        # Clean coordinate data
        clean_data = self._clean_coordinate_data(data, lat_col, lon_col)
        if clean_data.empty:
            return self._error_map("No valid coordinates for timeline")
        
        # Find date column
        date_col = self._find_date_column(clean_data)
        if not date_col:
            return self._error_map("No date column found for timeline visualization")
        
        # Calculate map center
        center_lat, center_lon = self._calculate_map_center(clean_data, lat_col, lon_col, context)
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=8,
            tiles='OpenStreetMap'
        )
        
        # Sort by date and add time-based markers
        clean_data = clean_data.sort_values(date_col)
        
        # Create color gradient based on time
        n_points = len(clean_data)
        for i, (idx, row) in enumerate(clean_data.iterrows()):
            # Color from blue (early) to red (late)
            color_intensity = i / max(1, n_points - 1)
            color = f"#{int(255 * color_intensity):02x}{int(255 * (1 - color_intensity)):02x}00"
            
            popup_content = self._create_military_popup(row)
            popup_content += f"<br><b>Sequence:</b> {i + 1} of {n_points}"
            
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=6,
                popup=folium.Popup(popup_content, max_width=300),
                color=color,
                fill=True,
                opacity=0.8
            ).add_to(m)
        
        return m
    
    def _find_coordinate_columns(self, data: pd.DataFrame) -> Tuple[Optional[str], Optional[str]]:
        """Find latitude and longitude columns."""
        lat_patterns = ['lat', 'latitude', 'y', 'northing']
        lon_patterns = ['lon', 'lng', 'longitude', 'x', 'easting']
        
        lat_col = None
        lon_col = None
        
        for col in data.columns:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in lat_patterns):
                if pd.api.types.is_numeric_dtype(data[col]):
                    lat_col = col
            elif any(pattern in col_lower for pattern in lon_patterns):
                if pd.api.types.is_numeric_dtype(data[col]):
                    lon_col = col
        
        return lat_col, lon_col
    
    def _find_operation_column(self, data: pd.DataFrame) -> Optional[str]:
        """Find column containing operation type information."""
        operation_patterns = ['operation', 'type', 'category', 'kind', 'mission']
        
        for col in data.columns:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in operation_patterns):
                return col
        
        return None
    
    def _find_date_column(self, data: pd.DataFrame) -> Optional[str]:
        """Find date column for timeline visualization."""
        date_patterns = ['date', 'time', 'when', 'occurred', 'incident_date']
        
        for col in data.columns:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in date_patterns):
                return col
        
        return None
    
    def _find_weight_column(self, data: pd.DataFrame, context: Dict[str, Any]) -> Optional[str]:
        """Find column to use for heatmap weights."""
        if 'weight_field' in context:
            return context['weight_field']
        
        weight_patterns = ['casualty', 'count', 'intensity', 'weight', 'value']
        
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                col_lower = col.lower()
                if any(pattern in col_lower for pattern in weight_patterns):
                    return col
        
        return None
    
    def _clean_coordinate_data(self, data: pd.DataFrame, lat_col: str, lon_col: str) -> pd.DataFrame:
        """Clean and validate coordinate data."""
        # Remove rows with missing coordinates
        clean_data = data.dropna(subset=[lat_col, lon_col])
        
        # Validate coordinate ranges
        clean_data = clean_data[
            (clean_data[lat_col] >= -90) & (clean_data[lat_col] <= 90) &
            (clean_data[lon_col] >= -180) & (clean_data[lon_col] <= 180)
        ]
        
        # Remove obvious invalid coordinates (0,0)
        clean_data = clean_data[
            ~((clean_data[lat_col] == 0) & (clean_data[lon_col] == 0))
        ]
        
        return clean_data
    
    def _calculate_map_center(self, data: pd.DataFrame, lat_col: str, lon_col: str, context: Dict[str, Any]) -> Tuple[float, float]:
        """Calculate appropriate map center."""
        # Check for region hint in context
        region = context.get('region', '').lower()
        if region in self.region_centers:
            return self.region_centers[region]
        
        # Calculate center from data
        center_lat = data[lat_col].median()
        center_lon = data[lon_col].median()
        
        return float(center_lat), float(center_lon)
    
    def _calculate_zoom_level(self, data: pd.DataFrame, lat_col: str, lon_col: str) -> int:
        """Calculate appropriate zoom level based on data spread."""
        lat_range = data[lat_col].max() - data[lat_col].min()
        lon_range = data[lon_col].max() - data[lon_col].min()
        max_range = max(lat_range, lon_range)
        
        if max_range > 10:
            return 5
        elif max_range > 5:
            return 6
        elif max_range > 2:
            return 7
        elif max_range > 1:
            return 8
        elif max_range > 0.5:
            return 9
        else:
            return 10
    
    def _get_operation_color(self, operation_type: str) -> str:
        """Get color for operation type."""
        for key, color in self.operation_colors.items():
            if key in operation_type:
                return color
        return self.operation_colors['default']
    
    def _get_operation_icon(self, operation_type: str) -> str:
        """Get icon for operation type."""
        for key, icon in self.military_icons.items():
            if key in operation_type:
                return icon
        return self.military_icons['default']
    
    def _create_military_popup(self, row: pd.Series) -> str:
        """Create detailed popup content for military events."""
        popup_content = "<div style='font-family: Arial; max-width: 250px;'>"
        
        # Event header
        popup_content += "<h4 style='margin: 0 0 10px 0; color: #2F4F4F;'>Military Event</h4>"
        
        # Key information
        important_fields = ['date', 'time', 'ship', 'unit', 'operation', 'type', 'location', 'province']
        
        for field in important_fields:
            for col in row.index:
                if field in col.lower() and pd.notna(row[col]):
                    field_name = col.replace('_', ' ').title()
                    popup_content += f"<b>{field_name}:</b> {row[col]}<br>"
        
        # Casualty information
        casualty_fields = ['casualty', 'killed', 'wounded', 'damage']
        for field in casualty_fields:
            for col in row.index:
                if field in col.lower() and pd.notna(row[col]):
                    field_name = col.replace('_', ' ').title()
                    popup_content += f"<b>{field_name}:</b> {row[col]}<br>"
        
        # Coordinates
        lat_col, lon_col = self._find_coordinate_columns(pd.DataFrame([row]))
        if lat_col and lon_col:
            popup_content += f"<b>Coordinates:</b> {row[lat_col]:.4f}, {row[lon_col]:.4f}<br>"
        
        popup_content += "</div>"
        return popup_content
    
    def _create_tooltip(self, row: pd.Series) -> str:
        """Create brief tooltip for quick preview."""
        # Find most relevant field for tooltip
        tooltip_fields = ['ship_name', 'unit', 'operation_name', 'date_incident']
        
        for field in tooltip_fields:
            if field in row.index and pd.notna(row[field]):
                return str(row[field])
        
        return "Military Event"
    
    def _add_marker_clusters(self, m: folium.Map, data: pd.DataFrame, lat_col: str, lon_col: str) -> None:
        """Add marker clustering for large datasets."""
        marker_cluster = plugins.MarkerCluster().add_to(m)
        
        for idx, row in data.iterrows():
            popup_content = self._create_military_popup(row)
            
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=self._create_tooltip(row)
            ).add_to(marker_cluster)
    
    def _empty_map(self, context: Dict[str, Any]) -> folium.Map:
        """Create empty map when no data is available."""
        center = self.region_centers.get(context.get('region', 'southeast_asia'), [15.0, 107.0])
        
        m = folium.Map(
            location=center,
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        folium.Marker(
            location=center,
            popup="No data available for mapping",
            icon=folium.Icon(color='gray', icon='info-sign')
        ).add_to(m)
        
        return m
    
    def _error_map(self, error_message: str) -> folium.Map:
        """Create error map with message."""
        center = [15.0, 107.0]  # Southeast Asia default
        
        m = folium.Map(
            location=center,
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        folium.Marker(
            location=center,
            popup=f"Map Error: {error_message}",
            icon=folium.Icon(color='red', icon='exclamation-triangle')
        ).add_to(m)
        
        return m