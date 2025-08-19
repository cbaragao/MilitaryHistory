#!/usr/bin/env python3
"""
Test script for the enhanced table selection functionality
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from rag_system import MilitaryVizInterface
    
    # Test initialization
    db_path = "src/ddb/opsanal.db"
    viz_interface = MilitaryVizInterface(db_path)
    
    # Test cases for explicit table and column selection
    test_queries = [
        "Analyze VCIIA by INCDATE",
        "Show HOSTA incidents over time", 
        "Map KHMER locations",
        "Compare PSYOPSA by theme",
        "Plot AIMS casualties by year",
        "Show VSSG data by province",
        "Analyze incidents by DATE_INCIDENT",
        "Show data by PROV_CODE"
    ]
    
    print("Testing Enhanced Table Selection")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        
        # Process the query without saving files
        result = viz_interface.process_query(query, save_output=False)
        
        if result['success']:
            processed = result['metadata']['processed_query']
            
            # Show what was detected
            entities = processed['entities']
            print(f"  Explicit Tables: {entities.get('explicit_tables', [])}")
            print(f"  Explicit Columns: {entities.get('explicit_columns', [])}")
            print(f"  Selected Table: {processed['table_name']}")
            print(f"  Confidence: {processed['confidence']:.2f}")
            print(f"  Data Shape: {result['metadata']['data_shape']}")
            print(f"  SQL: {processed['sql_query'][:100]}...")
        else:
            print(f"  ❌ Failed: {result['errors']}")
    
    # Test some edge cases
    print("\n" + "=" * 50)
    print("Testing Edge Cases")
    print("=" * 50)
    
    edge_cases = [
        "Show data",  # No explicit references
        "Plot vciia data by incdate",  # Lowercase
        "HOSTA table analysis",  # Different phrasing
        "Map coordinates from khmer_tx",  # Full table name
    ]
    
    for query in edge_cases:
        print(f"\nEdge Case: '{query}'")
        result = viz_interface.process_query(query, save_output=False)
        
        if result['success']:
            processed = result['metadata']['processed_query']
            entities = processed['entities']
            print(f"  Selected Table: {processed['table_name']}")
            print(f"  Explicit Tables: {entities.get('explicit_tables', [])}")
            print(f"  Confidence: {processed['confidence']:.2f}")
        else:
            print(f"  ❌ Failed: {result['errors']}")
    
    viz_interface.close()
    print("\n✅ Enhanced table selection test completed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()