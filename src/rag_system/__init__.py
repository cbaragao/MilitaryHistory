"""
Military History Visualization RAG System
==========================================

A RAG (Retrieval-Augmented Generation) system that generates Vega-Lite specifications 
and Folium maps from natural language queries over military historical data.
"""

from .military_viz_rag import MilitaryVizRAG
from .vega_generator import VegaLiteGenerator  
from .folium_generator import FoliumMapGenerator
from .query_processor import QueryProcessor
from .main_interface import MilitaryVizInterface

__version__ = "1.0.0"
__all__ = [
    "MilitaryVizRAG",
    "VegaLiteGenerator", 
    "FoliumMapGenerator",
    "QueryProcessor",
    "MilitaryVizInterface"
]