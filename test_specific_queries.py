#!/usr/bin/env python3
"""
Test specific table and column selection as requested
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
    
    # Test the exact query from the user request
    print("Testing Specific Query: 'Analyze VCIIA by INCDATE'")
    print("=" * 60)
    
    result = viz_interface.process_query("Analyze VCIIA by INCDATE", save_output=False)
    
    if result['success']:
        processed = result['metadata']['processed_query']
        entities = processed['entities']
        
        print(f"Query: {result['query']}")
        print(f"✅ Success: {result['success']}")
        print(f"📊 Data Shape: {result['metadata']['data_shape']}")
        print(f"🎯 Selected Table: {processed['table_name']}")
        print(f"📋 Explicit Tables Found: {entities.get('explicit_tables', [])[:3]}...")  # Show first 3
        print(f"📋 Explicit Columns Found: {entities.get('explicit_columns', [])}")
        print(f"🎪 Confidence Score: {processed['confidence']:.2f}")
        print(f"💾 SQL Query: {processed['sql_query']}")
        print(f"📈 Visualization Type: {processed['visualization_type']}")
        
        # Show sample data
        if not result['data'].empty:
            print(f"\n📋 Sample Data:")
            print(result['data'].head())
        
    else:
        print(f"❌ Failed: {result['errors']}")
    
    print("\n" + "=" * 60)
    print("Additional Tests - Table Selection by Column")
    print("=" * 60)
    
    # More specific tests
    specific_tests = [
        ("Show HOSTA by DATE_INCIDENT", "Should select HOSTA table using DATE_INCIDENT column"),
        ("Map KHMER incidents", "Should select KHMER table"),
        ("Analyze AIMS data by PRIM_TYPE", "Should select AIMS table using PRIM_TYPE column"),
        ("Show VSSG records by PROV_NAME", "Should select VSSG table using PROV_NAME column")
    ]
    
    for query, description in specific_tests:
        print(f"\nTest: {query}")
        print(f"Expected: {description}")
        
        result = viz_interface.process_query(query, save_output=False)
        
        if result['success']:
            processed = result['metadata']['processed_query']
            entities = processed['entities']
            print(f"  ✅ Selected Table: {processed['table_name']}")
            print(f"  📋 Explicit Columns: {entities.get('explicit_columns', [])}")
            print(f"  🎪 Confidence: {processed['confidence']:.2f}")
        else:
            print(f"  ❌ Failed: {result['errors']}")
    
    viz_interface.close()
    print("\n✅ Specific query tests completed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()