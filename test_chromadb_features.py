#!/usr/bin/env python3
"""
Test ChromaDB enhanced features
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
    
    print("ChromaDB Enhanced Features Test")
    print("=" * 50)
    
    # Test 1: Semantic Query Understanding
    print("\n🧠 Test 1: Semantic Query Understanding")
    print("-" * 40)
    
    semantic_queries = [
        "Show me temporal patterns in combat data",
        "I want to see spatial distribution of events", 
        "Display correlations between different metrics",
        "Create intensity visualization over time periods"
    ]
    
    for query in semantic_queries:
        result = viz_interface.process_query(query, save_output=False)
        if result['success']:
            processed = result['metadata']['processed_query']
            confidence = processed['confidence']
            viz_type = processed['visualization_type']
            table = processed['table_name']
            print(f"✅ '{query}'")
            print(f"   → {viz_type} from {table} (confidence: {confidence:.2f})")
        else:
            print(f"❌ '{query}' failed")
    
    # Test 2: Pattern Matching Comparison
    print(f"\n🔍 Test 2: Vector vs Keyword Pattern Matching")
    print("-" * 40)
    
    test_phrase = "show temporal trends"
    
    # Get patterns using vector search
    vector_patterns = viz_interface.rag_system.query_visualization_patterns(test_phrase, n_results=3)
    print(f"Vector search for '{test_phrase}':")
    for i, pattern in enumerate(vector_patterns, 1):
        print(f"  {i}. {pattern['name']} - {pattern['description']}")
    
    # Compare with keyword fallback
    print(f"\nKeyword fallback would find:")
    keyword_patterns = viz_interface.rag_system._fallback_pattern_matching(test_phrase)
    for i, pattern in enumerate(keyword_patterns, 1):
        print(f"  {i}. {pattern['name']} (score: {pattern.get('score', 0)})")
    
    # Test 3: Enhanced Query Suggestions
    print(f"\n💡 Test 3: Enhanced Query Suggestions")
    print("-" * 40)
    
    suggestion_tests = [
        "time analysis",
        "map visualization", 
        "compare categories",
        "correlation study"
    ]
    
    for test_query in suggestion_tests:
        suggestions = viz_interface.get_suggestions(test_query)
        print(f"Suggestions for '{test_query}':")
        for suggestion in suggestions[:2]:  # Show top 2
            print(f"  • {suggestion['query']}")
    
    # Test 4: Confidence Scoring
    print(f"\n🎯 Test 4: Confidence Scoring with ChromaDB")
    print("-" * 40)
    
    confidence_tests = [
        ("Show HOSTA incidents over time", "High confidence expected"),
        ("Analyze temporal patterns", "Medium confidence expected"),
        ("Display some data", "Low confidence expected")
    ]
    
    for query, expectation in confidence_tests:
        result = viz_interface.process_query(query, save_output=False)
        if result['success']:
            confidence = result['metadata']['processed_query']['confidence']
            print(f"'{query}': {confidence:.2f} - {expectation}")
        else:
            print(f"'{query}': Failed")
    
    viz_interface.close()
    print(f"\n✅ ChromaDB enhanced features test completed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()