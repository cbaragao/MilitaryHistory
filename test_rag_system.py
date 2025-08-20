#!/usr/bin/env python3
"""
Test script for the Military Visualization RAG System
"""

import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    print("🔄 Importing RAG system components...")
    from src.rag_system.main_interface import MilitaryVizInterface
    print("✅ RAG system imports successful")
    
    # Test initialization
    db_path = "src/ddb/opsanal.db"
    print(f"🔄 Initializing with database: {db_path}")
    viz_interface = MilitaryVizInterface(db_path)
    print("✅ RAG system initialization successful")
    
    # Test data availability
    data_info = viz_interface.get_available_data()
    print(f"✅ Found {data_info['total_tables']} tables with {data_info['total_records']} total records")
    
    # List available tables
    print("\nAvailable tables:")
    for table, info in data_info['tables'].items():
        if 'error' not in info:
            print(f"  - {table}: {info['row_count']} rows, {len(info['columns'])} columns")
    
    # Test query suggestions
    suggestions = viz_interface.get_suggestions()
    print(f"\n✅ Generated {len(suggestions)} query suggestions")
    print("Sample suggestions:")
    for suggestion in suggestions[:3]:
        print(f"  - {suggestion['query']}")
    
    # Test a simple query if we have data
    if data_info['total_records'] > 0:
        result = viz_interface.process_query("Show data over time", save_output=False)
        if result['success']:
            print(f"✅ Query processing successful - returned {result['metadata']['data_shape'][0]} rows")
        else:
            print(f"⚠️  Query failed: {result['errors']}")
    
    viz_interface.close()
    print("✅ RAG system test completed successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()