"""
MilitaryVizRAG - Core RAG system for military visualization
"""

import os
import json
import duckdb
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("Warning: ChromaDB and sentence-transformers not available. Install with: pip install chromadb sentence-transformers")


class MilitaryVizRAG:
    """
    Core RAG system for military historical data visualization.
    Manages vector store, schema information, and visualization patterns.
    """
    
    def __init__(self, duckdb_path: str):
        """
        Initialize the Military Visualization RAG system.
        
        Args:
            duckdb_path: Path to the DuckDB database with military data
        """
        self.duckdb_path = duckdb_path
        self.db = duckdb.connect(duckdb_path)
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "src" / "config"
        self.templates_dir = self.project_root / "src" / "templates"
        
        # Initialize components
        self.embedding_model = None
        self.vector_store = None
        self.schemas = {}
        self.viz_patterns = []
        
        if CHROMA_AVAILABLE:
            self._initialize_vector_store()
        else:
            print("Vector store disabled - ChromaDB not available")
            
        self._load_schemas()
        self._build_viz_knowledge_base()
    
    def _initialize_vector_store(self) -> Optional[object]:
        """Initialize ChromaDB vector store for visualization patterns."""
        if not CHROMA_AVAILABLE:
            return None
            
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize ChromaDB
            chroma_client = chromadb.Client()
            
            # Create or get collection
            try:
                self.vector_store = chroma_client.get_collection("military_viz_patterns")
            except:
                self.vector_store = chroma_client.create_collection("military_viz_patterns")
                
            return self.vector_store
        except Exception as e:
            print(f"Warning: Could not initialize vector store: {e}")
            return None
    
    def _load_schemas(self) -> None:
        """Load database table schemas for query generation."""
        try:
            # Get all tables in the database
            tables_result = self.db.execute("SHOW TABLES").fetchdf()
            
            for _, row in tables_result.iterrows():
                table_name = row['name']
                try:
                    # Get schema for each table
                    schema_result = self.db.execute(f"DESCRIBE {table_name}").fetchdf()
                    self.schemas[table_name] = {
                        'columns': schema_result['column_name'].tolist(),
                        'types': schema_result['column_type'].tolist(),
                        'schema_df': schema_result
                    }
                except Exception as e:
                    print(f"Warning: Could not load schema for table {table_name}: {e}")
                    
        except Exception as e:
            print(f"Warning: Could not load database schemas: {e}")
    
    def _build_viz_knowledge_base(self) -> None:
        """Build knowledge base of visualization patterns."""
        # Load visualization patterns from config
        patterns_file = self.config_dir / "visualization_patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                config = json.load(f)
                self.viz_patterns = config.get('patterns', [])
        else:
            # Default patterns if config file doesn't exist
            self.viz_patterns = self._get_default_viz_patterns()
        
        # Add patterns to vector store if available
        if self.vector_store and self.embedding_model:
            self._populate_vector_store()
    
    def _get_default_viz_patterns(self) -> List[Dict]:
        """Get default visualization patterns."""
        return [
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
    
    def _populate_vector_store(self) -> None:
        """Populate vector store with visualization patterns."""
        if not self.vector_store or not self.embedding_model:
            return
            
        for i, pattern in enumerate(self.viz_patterns):
            # Create embedding text from pattern description and triggers
            text = f"{pattern['description']} {' '.join(pattern['triggers'])}"
            
            try:
                embedding = self.embedding_model.encode(text).tolist()
                
                # Convert lists to strings for ChromaDB compatibility
                metadata = {}
                for key, value in pattern.items():
                    if isinstance(value, list):
                        metadata[key] = ', '.join(map(str, value))
                    else:
                        metadata[key] = value
                
                self.vector_store.add(
                    embeddings=[embedding],
                    documents=[text],
                    metadatas=[metadata],
                    ids=[f"pattern_{i}"]
                )
            except Exception as e:
                print(f"Warning: Could not add pattern to vector store: {e}")
    
    def query_visualization_patterns(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Query vector store for relevant visualization patterns.
        
        Args:
            query: Natural language query
            n_results: Number of patterns to return
            
        Returns:
            List of relevant visualization patterns
        """
        if not self.vector_store or not self.embedding_model:
            # Fallback to simple keyword matching
            return self._fallback_pattern_matching(query)
        
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            
            results = self.vector_store.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            patterns = []
            for metadata in results['metadatas'][0]:
                # Convert string values back to lists where appropriate
                pattern = {}
                for key, value in metadata.items():
                    if key in ['triggers', 'data_requirements', 'best_for', 'examples'] and isinstance(value, str):
                        pattern[key] = [item.strip() for item in value.split(',')]
                    else:
                        pattern[key] = value
                patterns.append(pattern)
                
            return patterns
            
        except Exception as e:
            print(f"Warning: Vector store query failed: {e}")
            return self._fallback_pattern_matching(query)
    
    def _fallback_pattern_matching(self, query: str) -> List[Dict]:
        """Fallback pattern matching using keywords."""
        query_lower = query.lower()
        matched_patterns = []
        
        for pattern in self.viz_patterns:
            score = 0
            for trigger in pattern['triggers']:
                if trigger in query_lower:
                    score += 1
                    
            if score > 0:
                pattern_copy = pattern.copy()
                pattern_copy['score'] = score
                matched_patterns.append(pattern_copy)
        
        # Sort by score and return top matches
        matched_patterns.sort(key=lambda x: x.get('score', 0), reverse=True)
        return matched_patterns[:3]
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Get schema information for a specific table.
        
        Args:
            table_name: Name of the database table
            
        Returns:
            Schema information including columns and types
        """
        return self.schemas.get(table_name, {})
    
    def get_available_tables(self) -> List[str]:
        """Get list of available tables in the database."""
        return list(self.schemas.keys())
    
    def execute_query(self, sql_query: str) -> pd.DataFrame:
        """
        Execute SQL query against the database.
        
        Args:
            sql_query: SQL query string
            
        Returns:
            Query results as pandas DataFrame
        """
        try:
            return self.db.execute(sql_query).fetchdf()
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()
    
    def close(self) -> None:
        """Close database connection."""
        if self.db:
            self.db.close()