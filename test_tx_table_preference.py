#!/usr/bin/env python3
"""
Test that table selection always prefers _tx tables
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
    
    print("Testing _tx Table Preference")
    print("=" * 50)
    
    # Test various queries to ensure _tx tables are always selected
    test_queries = [
        "Analyze VCIIA by INCDATE",
        "Show HOSTA incidents over time", 
        "Map KHMER locations",
        "Compare PSYOPSA by theme",
        "Plot AIMS casualties by year",
        "Show VSSG data by province",
        "Analyze incidents by DATE_INCIDENT",
        "Show data by PROV_CODE",
        "Show data",  # Generic query
        "Map coordinates",  # Generic spatial query
        "Show events over time",  # Generic temporal query
        "Compare by type"  # Generic categorical query
    ]
    
    all_tx_tables = True
    
    for query in test_queries:
        result = viz_interface.process_query(query, save_output=False)
        
        if result['success']:
            processed = result['metadata']['processed_query']
            selected_table = processed['table_name']
            is_tx_table = '_tx' in selected_table.lower()
            
            status = "✅" if is_tx_table else "❌"
            print(f"{status} Query: '{query}'")
            print(f"    Selected: {selected_table} (TX: {is_tx_table})")
            
            if not is_tx_table:
                all_tx_tables = False
                # Show what tables were considered
                entities = processed['entities']
                explicit_tables = entities.get('explicit_tables', [])
                tx_options = [t for t in explicit_tables if '_tx' in t.lower()]
                print(f"    TX Options Available: {tx_options}")
        else:
            print(f"❌ FAILED: '{query}' - {result['errors']}")
            all_tx_tables = False
    
    print("\n" + "=" * 50)
    if all_tx_tables:
        print("✅ SUCCESS: All queries selected _tx tables!")
    else:
        print("❌ ISSUE: Some queries did not select _tx tables")
    
    # Show available _tx tables for reference
    data_info = viz_interface.get_available_data()
    tx_tables = [table for table in data_info['tables'].keys() if '_tx' in table.lower()]
    print(f"\nAvailable _tx tables: {len(tx_tables)}")
    for table in sorted(tx_tables)[:10]:  # Show first 10
        row_count = data_info['tables'][table].get('row_count', 0)
        print(f"  - {table}: {row_count:,} rows")
    
    viz_interface.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()