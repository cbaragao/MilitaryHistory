"""
MilitaryVizInterface - Main interface for the military visualization RAG system
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

from .military_viz_rag import MilitaryVizRAG
from .vega_generator import VegaLiteGenerator
from .folium_generator import FoliumMapGenerator
from .query_processor import QueryProcessor


class MilitaryVizInterface:
    """
    Main interface for the Military Visualization RAG system.
    Provides high-level API for natural language queries to visualization generation.
    """
    
    def __init__(self, duckdb_path: str):
        """
        Initialize the interface.
        
        Args:
            duckdb_path: Path to the DuckDB database with military data
        """
        self.rag_system = MilitaryVizRAG(duckdb_path)
        self.vega_generator = VegaLiteGenerator()
        self.folium_generator = FoliumMapGenerator()
        self.query_processor = QueryProcessor(self.rag_system)
        
        self.project_root = Path(__file__).parent.parent.parent
        self.output_dir = self.project_root / "visuals"
        self.output_dir.mkdir(exist_ok=True)
    
    def process_query(self, query: str, save_output: bool = True) -> Dict[str, Any]:
        """
        Process natural language query and generate visualization.
        
        Args:
            query: Natural language query about military data
            save_output: Whether to save visualization files to disk
            
        Returns:
            Dictionary containing query results, visualization specs, and metadata
        """
        result = {
            'query': query,
            'success': False,
            'data': None,
            'visualization': None,
            'metadata': {},
            'errors': []
        }
        
        try:
            # Step 1: Process natural language query
            processed_query = self.query_processor.process_natural_language(query)
            result['metadata']['processed_query'] = processed_query
            
            # Step 2: Execute SQL query
            sql_query = processed_query['sql_query']
            data = self.rag_system.execute_query(sql_query)
            
            if data.empty:
                result['errors'].append("No data returned from query")
                return result
            
            result['data'] = data
            result['metadata']['data_shape'] = data.shape
            
            # Step 3: Generate appropriate visualization
            viz_type = processed_query['visualization_type']
            context = {
                'title': self._generate_title(query, processed_query),
                'query': query,
                'table_name': processed_query['table_name'],
                'entities': processed_query['entities']
            }
            
            if viz_type == 'folium_map':
                # Generate interactive map
                map_obj = self.folium_generator.generate_map(data, "density", context)
                if save_output:
                    map_path = self._save_map(map_obj, query)
                    result['visualization'] = {'type': 'folium_map', 'path': map_path}
                else:
                    result['visualization'] = {'type': 'folium_map', 'object': map_obj}
            else:
                # Generate Vega-Lite chart
                vega_spec = self.vega_generator.generate_spec(data, viz_type, context)
                if save_output:
                    spec_path = self._save_vega_spec(vega_spec, query)
                    result['visualization'] = {'type': 'vega_lite', 'spec': vega_spec, 'path': spec_path}
                else:
                    result['visualization'] = {'type': 'vega_lite', 'spec': vega_spec}
            
            result['success'] = True
            result['metadata']['confidence'] = processed_query['confidence']
            
        except Exception as e:
            result['errors'].append(f"Error processing query: {str(e)}")
        
        return result
    
    def get_suggestions(self, partial_query: str = "") -> List[Dict[str, Any]]:
        """
        Get query suggestions based on available data and patterns.
        
        Args:
            partial_query: Partial query for context-aware suggestions
            
        Returns:
            List of suggested queries with descriptions
        """
        suggestions = []
        
        # Get visualization patterns for suggestions
        patterns = self.rag_system.query_visualization_patterns(partial_query, n_results=5)
        
        for pattern in patterns:
            for example in pattern.get('examples', []):
                suggestions.append({
                    'query': example,
                    'pattern': pattern['name'],
                    'description': pattern['description'],
                    'viz_type': pattern['viz_type']
                })
        
        # Add table-specific suggestions
        tables = self.rag_system.get_available_tables()
        for table in tables[:3]:  # Limit to first 3 tables
            suggestions.extend(self._get_table_suggestions(table))
        
        return suggestions[:10]  # Return top 10 suggestions
    
    def get_available_data(self) -> Dict[str, Any]:
        """
        Get information about available data sources.
        
        Returns:
            Dictionary with table information and statistics
        """
        data_info = {
            'tables': {},
            'total_tables': 0,
            'total_records': 0
        }
        
        tables = self.rag_system.get_available_tables()
        data_info['total_tables'] = len(tables)
        
        for table in tables:
            try:
                # Get row count
                count_result = self.rag_system.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                row_count = count_result.iloc[0]['count'] if not count_result.empty else 0
                data_info['total_records'] += row_count
                
                # Get schema
                schema = self.rag_system.get_table_schema(table)
                
                data_info['tables'][table] = {
                    'row_count': row_count,
                    'columns': schema.get('columns', []),
                    'types': schema.get('types', [])
                }
                
            except Exception as e:
                data_info['tables'][table] = {'error': str(e)}
        
        return data_info
    
    def _generate_title(self, query: str, processed_query: Dict[str, Any]) -> str:
        """Generate appropriate title for visualization."""
        entities = processed_query.get('entities', {})
        table_name = processed_query.get('table_name', '')
        
        # Extract key components
        operations = entities.get('operations', [])
        temporal_info = processed_query.get('temporal_info', {})
        
        title_parts = []
        
        if operations:
            title_parts.append(f"{operations[0].replace('_', ' ').title()}")
        
        if temporal_info.get('years'):
            if len(temporal_info['years']) == 1:
                title_parts.append(f"({temporal_info['years'][0]})")
            else:
                title_parts.append(f"({temporal_info['years'][0]}-{temporal_info['years'][-1]})")
        
        if title_parts:
            return " ".join(title_parts)
        
        # Fallback to table name
        return table_name.replace('_', ' ').title() if table_name else "Military Data Analysis"
    
    def _save_vega_spec(self, spec: Dict[str, Any], query: str) -> str:
        """Save Vega-Lite specification to file."""
        # Generate filename from query
        safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '_')).strip()
        safe_query = safe_query.replace(' ', '_')[:50]  # Limit length
        
        filename = f"vega_{safe_query}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(spec, f, indent=2)
        
        return str(filepath)
    
    def _save_map(self, map_obj, query: str) -> str:
        """Save Folium map to HTML file."""
        # Generate filename from query
        safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '_')).strip()
        safe_query = safe_query.replace(' ', '_')[:50]  # Limit length
        
        filename = f"map_{safe_query}.html"
        filepath = self.output_dir / filename
        
        map_obj.save(str(filepath))
        
        return str(filepath)
    
    def _get_table_suggestions(self, table_name: str) -> List[Dict[str, Any]]:
        """Get query suggestions for a specific table."""
        suggestions = []
        schema = self.rag_system.get_table_schema(table_name)
        
        if not schema:
            return suggestions
        
        columns = schema.get('columns', [])
        table_display = table_name.replace('_', ' ').title()
        
        # Temporal suggestions
        date_cols = [col for col in columns if 'date' in col.lower() or 'time' in col.lower()]
        if date_cols:
            suggestions.append({
                'query': f"Show {table_display.lower()} over time",
                'pattern': 'temporal_analysis',
                'description': f"Time series analysis of {table_display}",
                'viz_type': 'line_chart'
            })
        
        # Geographic suggestions
        if any('lat' in col.lower() for col in columns) and any('lon' in col.lower() for col in columns):
            suggestions.append({
                'query': f"Map {table_display.lower()} locations",
                'pattern': 'geographic_distribution',
                'description': f"Geographic distribution of {table_display}",
                'viz_type': 'folium_map'
            })
        
        # Categorical suggestions
        categorical_cols = [col for col in columns if 'province' in col.lower() or 'type' in col.lower()]
        if categorical_cols:
            suggestions.append({
                'query': f"Compare {table_display.lower()} by {categorical_cols[0].replace('_', ' ')}",
                'pattern': 'categorical_comparison',
                'description': f"Comparison of {table_display} across categories",
                'viz_type': 'bar_chart'
            })
        
        return suggestions
    
    def close(self) -> None:
        """Close the RAG system and cleanup resources."""
        self.rag_system.close()