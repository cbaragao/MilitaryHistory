# MilitaryHistory Project Setup

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/cbaragao/MilitaryHistory.git
cd MilitaryHistory
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
# Core dependencies
pip install -r src/requirements.txt

# Development dependencies (optional)
pip install -r requirements-dev.txt
```

### 4. Environment Configuration
Create a `.env` file with your Data.world API token:
```
DW_AUTH_TOKEN=your_dataworld_token_here
```

### 5. Test Installation
```bash
python -c "import pandas, duckdb, datadotworld, folium; print('✅ Setup complete!')"
```

## Project Structure

```
MilitaryHistory/
├── src/
│   ├── scripts/
│   │   ├── generate_dataset_readmes.py  # Main README generator
│   │   └── dataset_summary.py           # Dataset overview
│   ├── common.py                        # Shared utilities
│   └── requirements.txt                 # Core dependencies
├── opsanal/                            # Dataset directories with READMEs
├── datasets/                           # Processed data files
├── visuals/                           # Generated visualizations
└── requirements-dev.txt               # Development dependencies
```

## Key Commands

### Generate Dataset Documentation
```bash
# Generate all READMEs
python src/scripts/generate_dataset_readmes.py

# Generate specific dataset
python src/scripts/generate_dataset_readmes.py --dataset khmer

# Upload to Data.world
python src/scripts/generate_dataset_readmes.py --upload-to-dataworld

# Dry run (test without changes)
python src/scripts/generate_dataset_readmes.py --dry-run
```

### Dataset Summary
```bash
python src/scripts/dataset_summary.py
```

## Dependencies Overview

### Core Data Processing
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **duckdb**: Fast analytical database

### Data Integration
- **datadotworld**: Data.world API client
- **requests**: HTTP library for API calls

### Visualization
- **folium**: Interactive maps
- **matplotlib**: Plotting library

### Geographic/Spatial
- **pyproj**: Coordinate transformations
- **mgrs**: Military Grid Reference System

### Development
- **jupyter**: Interactive notebooks
- **ruff**: Fast Python linter
- **pydantic**: Data validation

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure virtual environment is activated
2. **Data.world Auth**: Check your API token configuration
3. **Missing Dependencies**: Run `pip install -r src/requirements.txt`

### Platform-Specific Notes

- **Windows**: Use `.venv\Scripts\activate` to activate virtual environment
- **Linux/Mac**: Use `source .venv/bin/activate`
- **M1 Mac**: Some packages may require additional compilation

For detailed documentation, see individual README files in the `opsanal/` directory.
