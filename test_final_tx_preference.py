#!/usr/bin/env python3
"""
Final test to confirm _tx table preference is working correctly
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
    
    print("Final _tx Table Preference Test")
    print("=" * 40)
    
    # Test the original user query and similar variations
    test_queries = [
        "Analyze VCIIA by INCDATE",  # Original user query
        "Show HOSTA by DATE_INCIDENT",
        "Map KHMER locations", 
        "Show AIMS data by PRIM_TYPE",
        "Show VSSG records by PROV_NAME",
        "Show data by PROV_CODE",  # Previously problematic
        "Show data",
        "Map coordinates",
        "Show events over time",
        "Compare by type"
    ]
    
    success_count = 0
    total_count = 0
    
    for query in test_queries:
        result = viz_interface.process_query(query, save_output=False)
        total_count += 1
        
        if result['success']:
            processed = result['metadata']['processed_query']
            selected_table = processed['table_name']
            is_tx_table = '_tx' in selected_table.lower()
            
            if is_tx_table:
                success_count += 1
                print(f"✅ '{query}' → {selected_table}")
            else:
                print(f"❌ '{query}' → {selected_table} (NOT _tx)")
        else:
            # SQL execution errors don't count against table selection
            print(f"⚠️  '{query}' → SQL Error (table selection may still be correct)")
    
    print("\n" + "=" * 40)
    print(f"Results: {success_count}/{total_count} queries selected _tx tables")
    
    if success_count == total_count:
        print("🎉 SUCCESS: All queries now select _tx tables!")
    else:
        print(f"⚠️  {total_count - success_count} queries still not selecting _tx tables")
    
    # Show the improvement
    print(f"\nTable Selection Priority:")
    print(f"1. Explicit table names (prefer _tx)")
    print(f"2. Explicit column matches (prefer _tx)")  
    print(f"3. General scoring (+20 boost for _tx)")
    print(f"4. Default fallback (_tx tables)")
    
    viz_interface.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()