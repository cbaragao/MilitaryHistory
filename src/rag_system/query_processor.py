"""
QueryProcessor - Natural language to SQL translation for military data queries
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd


class QueryProcessor:
    """
    Processes natural language queries and converts them to SQL for military data.
    """
    
    def __init__(self, rag_system):
        """
        Initialize query processor.
        
        Args:
            rag_system: Reference to MilitaryVizRAG instance
        """
        self.rag_system = rag_system
        self.config_dir = Path(__file__).parent.parent / "config"
        
        # Load military terminology
        self.military_terms = self._load_military_terms()
        
        # Common SQL templates
        self.sql_templates = {
            'temporal': "SELECT {date_field}, COUNT(*) as count FROM {table} WHERE {conditions} GROUP BY {date_field} ORDER BY {date_field}",
            'geographic': "SELECT {lat_field}, {lon_field}, {other_fields} FROM {table} WHERE {conditions}",
            'categorical': "SELECT {category_field}, COUNT(*) as count FROM {table} WHERE {conditions} GROUP BY {category_field} ORDER BY count DESC",
            'basic': "SELECT * FROM {table} WHERE {conditions} LIMIT 1000"
        }
    
    def process_natural_language(self, query: str) -> Dict[str, Any]:
        """
        Process natural language query and return structured information.
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary with extracted information and generated SQL
        """
        query_lower = query.lower()
        
        # Extract components
        entities = self._extract_military_entities(query_lower)
        temporal_info = self._extract_temporal_info(query_lower)
        spatial_info = self._extract_spatial_info(query_lower)
        viz_type = self._determine_visualization_type(query_lower, entities)
        
        # Determine best table to query
        table_name = self._select_best_table(entities, temporal_info, spatial_info)
        
        # Generate SQL query
        sql_query = self._generate_sql_query(table_name, entities, temporal_info, spatial_info, viz_type, query)
        
        return {
            'query': query,
            'entities': entities,
            'temporal_info': temporal_info,
            'spatial_info': spatial_info,
            'visualization_type': viz_type,
            'table_name': table_name,
            'sql_query': sql_query,
            'confidence': self._calculate_confidence(entities, temporal_info, spatial_info)
        }
    
    def _extract_military_entities(self, query: str) -> Dict[str, List[str]]:
        """Extract military-specific entities from query."""
        entities = {
            'operations': [],
            'units': [],
            'weapons': [],
            'activities': [],
            'metrics': [],
            'explicit_tables': [],
            'explicit_columns': []
        }
        
        # Operation types
        operation_patterns = {
            'artillery': ['artillery', 'firing', 'bombardment', 'shelling', 'guns'],
            'air_mission': ['air', 'bombing', 'airstrike', 'aircraft', 'plane', 'helicopter'],
            'ground_operation': ['patrol', 'sweep', 'ground', 'infantry', 'troops'],
            'naval': ['naval', 'ship', 'vessel', 'fleet', 'navy'],
            'reconnaissance': ['recon', 'surveillance', 'intelligence', 'observation']
        }
        
        for op_type, keywords in operation_patterns.items():
            if any(keyword in query for keyword in keywords):
                entities['operations'].append(op_type)
        
        # Units and ships
        unit_patterns = [
            r'\\b[A-Z]{2,}\\b',  # Acronyms like USS, ARVN
            r'\\b\\d+(?:st|nd|rd|th)\\s+\\w+',  # 1st Infantry, 2nd Battalion
        ]
        
        for pattern in unit_patterns:
            matches = re.findall(pattern, query)
            entities['units'].extend(matches)
        
        # Weapons and equipment
        weapon_keywords = ['gun', 'rifle', 'mortar', 'rocket', 'missile', 'bomb', 'grenade']
        for weapon in weapon_keywords:
            if weapon in query:
                entities['weapons'].append(weapon)
        
        # Activities
        activity_keywords = ['incident', 'attack', 'mission', 'operation', 'engagement', 'contact']
        for activity in activity_keywords:
            if activity in query:
                entities['activities'].append(activity)
        
        # Metrics
        metric_keywords = ['casualty', 'casualties', 'killed', 'wounded', 'damage', 'destroyed']
        for metric in metric_keywords:
            if metric in query:
                entities['metrics'].append(metric)
        
        # Extract explicit table names and column names
        self._extract_explicit_references(query, entities)
        
        return entities
    
    def _extract_explicit_references(self, query: str, entities: Dict[str, List[str]]) -> None:
        """Extract explicit table and column references from query."""
        query_upper = query.upper()
        available_tables = self.rag_system.get_available_tables()
        
        # Check for explicit table references
        for table in available_tables:
            table_upper = table.upper()
            table_base = table_upper.replace('_TX', '').replace('_NARA', '').replace('_SCHEMA', '')
            
            # Check for exact table name or base name
            if table_upper in query_upper or table_base in query_upper:
                if table not in entities['explicit_tables']:
                    entities['explicit_tables'].append(table)
                continue
                
            # Check for common table abbreviations/aliases
            table_patterns = {
                'VCIIA': ['vciia'],
                'HOSTA': ['hosta'],
                'KHMER': ['khmer'],
                'INCDA': ['incda'],
                'CONGA': ['conga'],
                'AIMS': ['aims'],
                'PSYOPSA': ['psyopsa'],
                'VSSG': ['vssg'],
                'TIRSA': ['tirsa'],
                'SEAFA': ['seafa'],
                'BASFA': ['basfa'],
                'GORS': ['gors']
            }
            
            for pattern, aliases in table_patterns.items():
                if any(alias.upper() in query_upper for alias in aliases):
                    # Find the actual table with this pattern
                    matching_tables = [t for t in available_tables if pattern in t.upper()]
                    if matching_tables:
                        # Prefer unified tables first, then _tx tables, then _nara, then others
                        all_tx_tables = [t for t in matching_tables if '_all_tx' in t.lower()]
                        if all_tx_tables:
                            if all_tx_tables[0] not in entities['explicit_tables']:
                                entities['explicit_tables'].append(all_tx_tables[0])
                        else:
                            tx_tables = [t for t in matching_tables if '_tx' in t.lower()]
                            if tx_tables:
                                if tx_tables[0] not in entities['explicit_tables']:
                                    entities['explicit_tables'].append(tx_tables[0])
                            else:
                                if matching_tables[0] not in entities['explicit_tables']:
                                    entities['explicit_tables'].append(matching_tables[0])
                    break
        
        # Extract explicit column references
        # First, check all tables for explicit column mentions
        for table in available_tables:
            schema = self.rag_system.get_table_schema(table)
            if schema:
                columns = schema.get('columns', [])
                for column in columns:
                    column_upper = column.upper()
                    # Check for exact column name (must be separated by word boundaries)
                    import re
                    column_pattern = r'\b' + re.escape(column_upper) + r'\b'
                    if re.search(column_pattern, query_upper):
                        if column not in entities['explicit_columns']:
                            entities['explicit_columns'].append(column)
                        # If we found a column match, also add this table if not already found
                        if table not in entities['explicit_tables']:
                            entities['explicit_tables'].append(table)
                    
                    # Check for column name without underscores (but still require word boundaries)
                    column_no_underscore = column_upper.replace('_', '')
                    if len(column_no_underscore) > 5:  # Increase minimum length
                        no_underscore_pattern = r'\b' + re.escape(column_no_underscore) + r'\b'
                        if re.search(no_underscore_pattern, query_upper.replace('_', '').replace(' ', '')):
                            if column not in entities['explicit_columns']:
                                entities['explicit_columns'].append(column)
                            # If we found a column match, also add this table if not already found
                            if table not in entities['explicit_tables']:
                                entities['explicit_tables'].append(table)
    
    def _extract_temporal_info(self, query: str) -> Dict[str, Any]:
        """Extract temporal information from query."""
        temporal_info = {
            'has_temporal': False,
            'years': [],
            'months': [],
            'date_ranges': [],
            'relative_time': []
        }
        
        # Year extraction
        year_pattern = r'\\b(19[6-9]\\d|20[0-2]\\d)\\b'
        years = re.findall(year_pattern, query)
        temporal_info['years'] = [int(year) for year in years]
        
        # Month names
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                 'july', 'august', 'september', 'october', 'november', 'december']
        for i, month in enumerate(months, 1):
            if month in query:
                temporal_info['months'].append(i)
        
        # Relative time expressions
        relative_patterns = ['over time', 'timeline', 'temporal', 'chronological', 'during']
        for pattern in relative_patterns:
            if pattern in query:
                temporal_info['relative_time'].append(pattern)
        
        # Date range patterns
        range_patterns = [
            r'\\b(19[6-9]\\d)\\s*-\\s*(19[6-9]\\d)\\b',  # 1970-1975
            r'\\bbetween\\s+(19[6-9]\\d)\\s+and\\s+(19[6-9]\\d)\\b'  # between 1970 and 1975
        ]
        
        for pattern in range_patterns:
            matches = re.findall(pattern, query)
            for match in matches:
                temporal_info['date_ranges'].append((int(match[0]), int(match[1])))
        
        temporal_info['has_temporal'] = bool(
            temporal_info['years'] or 
            temporal_info['months'] or 
            temporal_info['date_ranges'] or 
            temporal_info['relative_time']
        )
        
        return temporal_info
    
    def _extract_spatial_info(self, query: str) -> Dict[str, Any]:
        """Extract spatial/geographic information from query."""
        spatial_info = {
            'has_spatial': False,
            'countries': [],
            'provinces': [],
            'coordinates': [],
            'spatial_keywords': []
        }
        
        # Countries
        countries = ['vietnam', 'cambodia', 'laos', 'thailand']
        for country in countries:
            if country in query:
                spatial_info['countries'].append(country)
        
        # Common provinces (this could be expanded with a full list)
        provinces = ['binh_dinh', 'quang_nam', 'thua_thien', 'quang_tri', 'phong_dinh']
        for province in provinces:
            if province.replace('_', ' ') in query or province in query:
                spatial_info['provinces'].append(province)
        
        # Spatial keywords
        spatial_keywords = ['map', 'geographic', 'spatial', 'location', 'where', 'coordinates']
        for keyword in spatial_keywords:
            if keyword in query:
                spatial_info['spatial_keywords'].append(keyword)
        
        # Coordinate patterns (basic)
        coord_pattern = r'(-?\\d+\\.\\d+),\\s*(-?\\d+\\.\\d+)'
        coords = re.findall(coord_pattern, query)
        spatial_info['coordinates'] = [(float(lat), float(lon)) for lat, lon in coords]
        
        spatial_info['has_spatial'] = bool(
            spatial_info['countries'] or 
            spatial_info['provinces'] or 
            spatial_info['coordinates'] or 
            spatial_info['spatial_keywords']
        )
        
        return spatial_info
    
    def _determine_visualization_type(self, query: str, entities: Dict[str, List[str]]) -> str:
        """Determine the best visualization type for the query."""
        # Explicit visualization type mentions
        if any(word in query for word in ['map', 'geographic', 'spatial', 'location']):
            return 'folium_map'
        
        if any(word in query for word in ['heatmap', 'heat', 'density', 'intensity']):
            return 'heatmap'
        
        if any(word in query for word in ['scatter', 'correlation', 'vs', 'versus', 'against']):
            return 'scatter_plot'
        
        if any(word in query for word in ['over time', 'timeline', 'temporal', 'trend']):
            return 'line_chart'
        
        if any(word in query for word in ['compare', 'comparison', 'by type', 'by province']):
            return 'bar_chart'
        
        # Default based on data characteristics
        if entities['operations'] or entities['activities']:
            return 'line_chart'  # Good for showing operations over time
        
        return 'bar_chart'  # Safe default
    
    def _select_best_table(self, entities: Dict[str, List[str]], temporal_info: Dict[str, Any], spatial_info: Dict[str, Any]) -> str:
        """Select the most appropriate table based on query characteristics."""
        available_tables = self.rag_system.get_available_tables()
        
        # HIGHEST PRIORITY: If explicit table names are found, use them (prefer _tx tables)
        if entities.get('explicit_tables'):
            # Filter to _tx tables first
            tx_tables = [t for t in entities['explicit_tables'] if '_tx' in t.lower()]
            if tx_tables and tx_tables[0] in available_tables:
                return tx_tables[0]
            
            # Fallback to first explicit table if no _tx tables found
            explicit_table = entities['explicit_tables'][0]
            if explicit_table in available_tables:
                return explicit_table
        
        # SECOND PRIORITY: If explicit columns are found, find tables containing those columns (prefer _tx)
        if entities.get('explicit_columns'):
            explicit_columns = entities['explicit_columns']
            column_matches = {}
            
            for table in available_tables:
                schema = self.rag_system.get_table_schema(table)
                if schema:
                    table_columns = [col.upper() for col in schema.get('columns', [])]
                    matches = sum(1 for col in explicit_columns if col.upper() in table_columns)
                    if matches > 0:
                        column_matches[table] = matches
            
            if column_matches:
                # Prefer _tx tables among those with column matches
                tx_matches = {k: v for k, v in column_matches.items() if '_tx' in k.lower()}
                if tx_matches:
                    # Return _tx table with most column matches
                    best_table = max(tx_matches, key=tx_matches.get)
                    return best_table
                else:
                    # No _tx tables have the explicit columns - fall through to other priorities
                    # This ensures we still try to find a _tx table rather than settling for lookup tables
                    pass
        
        # THIRD PRIORITY: Score tables based on other relevance factors
        table_scores = {}
        
        for table in available_tables:
            score = 0
            table_lower = table.lower()
            
            # HIGHEST PREFERENCE: Give unified tables (like aims_all_tx) maximum boost
            if '_all_tx' in table_lower:
                score += 50
            
            # STRONG PREFERENCE: Give _tx tables a significant boost
            elif '_tx' in table_lower:
                score += 20
            
            # Operation type matching
            for operation in entities['operations']:
                if operation in table_lower:
                    score += 10
            
            # Activity matching
            for activity in entities['activities']:
                if activity in table_lower:
                    score += 5
            
            # Geographic matching
            for country in spatial_info['countries']:
                if country in table_lower:
                    score += 8
            
            # Check if table has required fields
            schema = self.rag_system.get_table_schema(table)
            if schema:
                columns = [col.lower() for col in schema.get('columns', [])]
                
                # Temporal requirements
                if temporal_info['has_temporal']:
                    if any('date' in col or 'time' in col for col in columns):
                        score += 5
                
                # Spatial requirements  
                if spatial_info['has_spatial']:
                    if any('lat' in col or 'lon' in col for col in columns):
                        score += 5
            
            table_scores[table] = score
        
        # Return table with highest score, or default if no good matches (prefer _tx tables)
        if table_scores:
            # Filter to tables with scores > 0
            scored_tables = {k: v for k, v in table_scores.items() if v > 0}
            if scored_tables:
                # Prefer _tx tables among those with good scores
                tx_scored = {k: v for k, v in scored_tables.items() if '_tx' in k.lower()}
                if tx_scored:
                    best_table = max(tx_scored, key=tx_scored.get)
                    return best_table
                else:
                    # Fallback to any table with a good score
                    best_table = max(scored_tables, key=scored_tables.get)
                    return best_table
        
        # Default fallback
        default_tables = ['khmer_tx', 'hosta_tx', 'incda_tx', 'conga_tx']
        for default in default_tables:
            if default in available_tables:
                return default
        
        # Last resort - return first _tx table available, or any table
        tx_tables = [t for t in available_tables if '_tx' in t.lower()]
        if tx_tables:
            return tx_tables[0]
        
        return available_tables[0] if available_tables else 'military_events'
    
    def _generate_sql_query(self, table_name: str, entities: Dict[str, List[str]], 
                           temporal_info: Dict[str, Any], spatial_info: Dict[str, Any], 
                           viz_type: str, original_query: str = '') -> str:
        """Generate SQL query based on extracted information."""
        
        # Get table schema
        schema = self.rag_system.get_table_schema(table_name)
        if not schema:
            return f"SELECT * FROM {table_name} LIMIT 100"
        
        columns = schema.get('columns', [])
        columns_lower = [col.lower() for col in columns]
        
        # Build WHERE conditions
        conditions = []
        
        # Temporal conditions
        date_field = self._find_date_field(columns, entities.get('explicit_columns', []))
        if temporal_info['has_temporal'] and date_field:
            if temporal_info['years']:
                if len(temporal_info['years']) == 1:
                    conditions.append(f"EXTRACT(year FROM {date_field}) = {temporal_info['years'][0]}")
                else:
                    year_list = ','.join(map(str, temporal_info['years']))
                    conditions.append(f"EXTRACT(year FROM {date_field}) IN ({year_list})")
            
            if temporal_info['date_ranges']:
                for start_year, end_year in temporal_info['date_ranges']:
                    conditions.append(f"EXTRACT(year FROM {date_field}) BETWEEN {start_year} AND {end_year}")
        
        # Era filtering for unified tables (do this BEFORE geographic filtering)
        era_applied = False
        if '_all_tx' in table_name.lower() and 'era' in [col.lower() for col in columns]:
            era_keywords = {
                'early': 'early_wars',
                'korea': 'korea_era', 
                'vietnam': 'vietnam_era',
                'post': 'post_vietnam',
                'gulf': 'gulf_war_era'
            }
            
            query_lower = original_query.lower()
            for keyword, era_value in era_keywords.items():
                if keyword in query_lower:
                    conditions.append(f"era = '{era_value}'")
                    era_applied = True
                    break

        # Geographic conditions (skip if era filtering is applied)
        if spatial_info['countries'] and not era_applied:
            country_conditions = []
            for country in spatial_info['countries']:
                # Look for country-related columns
                country_columns = [col for col in columns if 'country' in col.lower() or 'region' in col.lower()]
                if country_columns:
                    country_conditions.append(f"LOWER({country_columns[0]}) LIKE '%{country}%'")
            
            if country_conditions:
                conditions.append(f"({' OR '.join(country_conditions)})")

        # Operation type conditions
        if entities['operations']:
            operation_conditions = []
            operation_columns = [col for col in columns if 'operation' in col.lower() or 'type' in col.lower()]
            
            for operation in entities['operations']:
                for col in operation_columns:
                    operation_conditions.append(f"LOWER({col}) LIKE '%{operation}%'")
            
            if operation_conditions:
                conditions.append(f"({' OR '.join(operation_conditions)})")
        
        # Ship/unit conditions
        if entities['units']:
            unit_conditions = []
            unit_columns = [col for col in columns if 'ship' in col.lower() or 'unit' in col.lower()]
            
            for unit in entities['units']:
                for col in unit_columns:
                    unit_conditions.append(f"UPPER({col}) LIKE '%{unit.upper()}%'")
            
            if unit_conditions:
                conditions.append(f"({' OR '.join(unit_conditions)})")
        
        # Build SELECT clause based on visualization type
        if viz_type == 'folium_map':
            lat_field, lon_field = self._find_coordinate_fields(columns)
            if lat_field and lon_field:
                select_fields = f"{lat_field}, {lon_field}, *"
            else:
                select_fields = "*"
        elif viz_type == 'line_chart' and date_field:
            select_fields = f"{date_field}, COUNT(*) as count"
        else:
            select_fields = "*"
        
        # Combine into SQL query
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        if viz_type == 'line_chart' and date_field:
            sql = f"SELECT {date_field}, COUNT(*) as count FROM {table_name} WHERE {where_clause} GROUP BY {date_field} ORDER BY {date_field}"
        elif viz_type == 'bar_chart':
            category_field = self._find_category_field(columns, entities.get('explicit_columns', []))
            if category_field:
                sql = f"SELECT {category_field}, COUNT(*) as count FROM {table_name} WHERE {where_clause} GROUP BY {category_field} ORDER BY count DESC LIMIT 20"
            else:
                sql = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT 1000"
        else:
            sql = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT 1000"
        
        return sql
    
    def _find_date_field(self, columns: List[str], explicit_columns: List[str] = None) -> Optional[str]:
        """Find the primary date field in columns, prioritizing explicit columns."""
        if explicit_columns:
            # First check if any explicit columns are date-like
            date_patterns = ['date', 'time', 'incident', 'event', 'occurred']
            for explicit_col in explicit_columns:
                if explicit_col in columns:  # Make sure column exists in table
                    if any(pattern in explicit_col.lower() for pattern in date_patterns):
                        return explicit_col
        
        # Fallback to standard date field detection
        date_patterns = ['date', 'time', 'incident_date', 'event_date', 'occurred']
        
        for pattern in date_patterns:
            for col in columns:
                if pattern in col.lower():
                    return col
        
        return None
    
    def _find_coordinate_fields(self, columns: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """Find latitude and longitude fields."""
        lat_patterns = ['lat', 'latitude', 'y']
        lon_patterns = ['lon', 'lng', 'longitude', 'x']
        
        lat_field = None
        lon_field = None
        
        for col in columns:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in lat_patterns):
                lat_field = col
            elif any(pattern in col_lower for pattern in lon_patterns):
                lon_field = col
        
        return lat_field, lon_field
    
    def _find_category_field(self, columns: List[str], explicit_columns: List[str] = None) -> Optional[str]:
        """Find a good categorical field for grouping, prioritizing explicit columns."""
        if explicit_columns:
            # First check if any explicit columns are categorical
            for explicit_col in explicit_columns:
                if explicit_col in columns:  # Make sure column exists in table
                    return explicit_col
        
        # Fallback to standard category field detection
        category_patterns = ['province', 'operation', 'type', 'unit', 'ship', 'category']
        
        for pattern in category_patterns:
            for col in columns:
                if pattern in col.lower():
                    return col
        
        return None
    
    def _calculate_confidence(self, entities: Dict[str, List[str]], temporal_info: Dict[str, Any], 
                            spatial_info: Dict[str, Any]) -> float:
        """Calculate confidence score for the query processing."""
        score = 0.0
        
        # Explicit references give highest confidence
        if entities.get('explicit_tables'):
            score += 0.4
        if entities.get('explicit_columns'):
            score += 0.3
        
        # Entity extraction confidence
        other_entities = {k: v for k, v in entities.items() if k not in ['explicit_tables', 'explicit_columns']}
        total_entities = sum(len(entity_list) for entity_list in other_entities.values())
        if total_entities > 0:
            score += 0.2
        
        # Temporal information confidence
        if temporal_info['has_temporal']:
            score += 0.2
        
        # Spatial information confidence
        if spatial_info['has_spatial']:
            score += 0.2
        
        # Base confidence for any recognized patterns
        if score == 0.0:
            score += 0.2
        
        return min(score, 1.0)
    
    def _load_military_terms(self) -> Dict[str, Any]:
        """Load military terminology mapping."""
        terms_file = self.config_dir / "military_terms.json"
        
        if terms_file.exists():
            with open(terms_file, 'r') as f:
                return json.load(f)
        
        # Default terms if file doesn't exist
        return {
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