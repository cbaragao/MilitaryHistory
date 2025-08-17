# Dataset Documentation Management Instructions

You are working with the MilitaryHistory archival data processing pipeline that maintains comprehensive datasets from the National Archives (NARA) with automated Data.world integration. This guide details the process for creating and maintaining README documentation for each dataset.

## 🎯 Overview

The project contains 58+ historical military datasets in the `opsanal/` directory structure, each with dedicated README.md files providing comprehensive documentation. These datasets are automatically processed and published to Data.world with proper schema metadata.

## 📁 Repository Structure

```
MilitaryHistory/
├── opsanal/                    # Dataset directories
│   ├── aims/                   # Awards and decorations
│   │   ├── README.md          # Auto-generated documentation
│   │   ├── data/              # Processed data files
│   │   ├── docs/              # Original documentation
│   │   └── schema/            # Field definitions
│   ├── khmer/                 # Cambodia operations
│   ├── psyopsa/               # Psychological operations
│   └── [50+ other datasets]
├── src/
│   ├── config/
│   │   └── datasets.json      # Master metadata registry
│   └── scripts/
│       ├── generate_dataset_readmes.py  # README generator
│       └── [dataset].py       # Individual processors
└── .github/
    ├── copilot-instructions.md      # Data visualization standards
    └── dataset-documentation.md     # This file
```

## 🔧 README Generation Process

### Automated Generation

The README files are automatically generated using the comprehensive script:

```bash
# Generate all README files
python src/scripts/generate_dataset_readmes.py

# Generate specific dataset README
python src/scripts/generate_dataset_readmes.py --dataset khmer
```

### Data Sources for README Content

1. **datasets.json**: Master metadata registry containing:
   - NARA ID numbers
   - Original filenames
   - Catalog URLs
   - Source URLs
   - Availability status

2. **Schema files**: `opsanal/{dataset}/schema/schema.json`:
   - Field definitions
   - Data types
   - Field lengths
   - Comprehensive descriptions

3. **Documentation files**: `opsanal/{dataset}/docs/`:
   - PDF documentation
   - Lookup tables
   - Historical context files
   - Technical specifications

4. **Processing scripts**: `src/scripts/{dataset}.py`:
   - Data.world project mappings
   - Processing instructions
   - Transformation logic

## 📋 README Content Structure

Each generated README includes:

### 1. Dataset Overview
- Descriptive summary
- Data.world project link
- NARA source information

### 2. Data Structure
- Transaction file information
- Schema field counts
- Key field descriptions (first 10 fields)
- Processing status

### 3. Documentation Section
- Available documentation files with sizes
- Schema references
- Processing script locations

### 4. Data Processing
- ETL pipeline overview
- Command-line usage
- Dependencies

### 5. Data Access
- Data.world URLs
- Query examples
- API access information

### 6. Usage Examples
- Python code samples
- SQL query templates
- Spatial analysis (for geographic datasets)

### 7. Data Quality & Context
- Completeness status
- Known limitations
- Historical context

## 🗂️ Dataset Categories

### Major Dataset Groups

1. **GORS (Ground Operations Reporting System)**
   - 35 individual datasets (by year and phase)
   - Combat operations data
   - Spatial coordinates included

2. **Core Operational Datasets**
   - `aims`: Awards and decorations
   - `khmer`: Cambodia operations  
   - `psyopsa`: Psychological operations
   - `seafa`: Southeast Asia forces
   - `incda`: Republic of Vietnam incidents
   - `tirsa`: Terrorist incident reporting
   - `vciia`: Viet Cong initiated incidents

3. **Administrative Datasets**
   - `basfa`: Base facilities
   - `conga`: Congressional data
   - `hes`: Hamlet evaluation system

### Data.world Project Mapping

The datasets map to Data.world projects as follows:

```python
dataworld_mapping = {
    "psyopsa": "psyopsa",
    "khmer": "khmer", 
    "aims": "aimsawards",
    "seafa": "southeast-asia-forces-seafa",
    "gors": "ground-operations-reporting-system-gors",
    "incda": "republic-of-vietnam-incidents-files-incda",
    "tirsa": "terrorist-incident-reporting-system-tirsa",
    "vciia": "viet-cong-initiated-incidents-vciia",
    "basfa": "basfa",
    "conga": "conga"
}
```

## 🔄 Maintenance Process

### When Adding New Datasets

1. **Create dataset directory**: `opsanal/{dataset_name}/`
2. **Add metadata**: Update `src/config/datasets.json`
3. **Create schema**: Add `schema/schema.json` with field definitions
4. **Add documentation**: Place original docs in `docs/` folder
5. **Create processor**: Write `src/scripts/{dataset_name}.py`
6. **Generate README**: Run the README generator script
7. **Update Data.world mapping**: Add to project mapping if needed

### When Updating Existing Datasets

1. **Update metadata**: Modify `datasets.json` as needed
2. **Update schema**: Revise field definitions in schema.json
3. **Add documentation**: Include new docs files
4. **Regenerate README**: Run generator to update documentation
5. **Update Data.world**: Sync schema changes using the updater script

### README Regeneration

READMEs should be regenerated when:
- New documentation files are added
- Schema definitions change
- Metadata is updated in datasets.json
- Processing logic changes
- Data.world project information changes

## 📊 Schema Integration

### Schema Structure

Each dataset's schema.json follows this pattern:

```json
{
  "data": [
    {
      "field_group": "FIELD",
      "id": "FIELD_NAME",
      "definition": "Comprehensive field description",
      "data_values": "Data type information",
      "length": "Field length in characters"
    }
  ]
}
```

### Schema Usage in READMEs

- **Field Count**: Automatically calculated from schema
- **Key Fields**: First 10 fields displayed with descriptions
- **Data Types**: Extracted from schema metadata
- **Field Lengths**: Shown for fixed-width fields

## 🌐 Data.world Integration

### Published Datasets

All datasets are available at: `https://data.world/aragaocb/{project_name}`

### Transaction Files

Each dataset publishes a primary transaction file: `{dataset}_tx.csv`

### Schema Updates

Column descriptions are automatically synchronized using:

```bash
# Update all dataset schemas
python src/scripts/update_dataworld_descriptions.py --all

# Update specific dataset
python src/scripts/update_dataworld_descriptions.py khmer
```

## 🔍 Quality Assurance

### README Validation

Before committing README updates:

1. **Content Accuracy**: Verify all metadata matches source files
2. **Link Validity**: Confirm Data.world and NARA URLs work
3. **Schema Consistency**: Ensure field counts and descriptions match
4. **Documentation Coverage**: Check all docs files are listed
5. **Format Consistency**: Maintain standard structure across all READMEs

### Automated Checks

The generation script includes validation for:
- Missing schema files
- Invalid metadata references
- Broken file paths
- Inconsistent naming

## 📖 Usage Examples

### For Code Contributors

```bash
# Add new dataset "newdata"
mkdir opsanal/newdata/{data,docs,schema}
# Add metadata to datasets.json
# Create schema.json
# Write processing script
python src/scripts/generate_dataset_readmes.py --dataset newdata
```

### For Data Analysts

```python
import datadotworld as dw

# List all available datasets
datasets = [
    'aims', 'khmer', 'psyopsa', 'seafa', 'gors', 
    'incda', 'tirsa', 'vciia', 'basfa', 'conga'
]

# Access any dataset
df = dw.load_dataset('aragaocb/khmer').dataframes['khmer_tx']
```

### For Researchers

1. **Browse Datasets**: Check individual README files for overview
2. **Access Data**: Use Data.world links for direct access
3. **Understand Schema**: Review field definitions in README
4. **Query Data**: Use provided SQL examples
5. **Cite Properly**: Follow citation format in README

## 🤝 Contributing Guidelines

### README Updates

1. **Use Generator**: Always use the automated generator
2. **Update Sources**: Modify source files (datasets.json, schema.json) not READMEs directly
3. **Test Locally**: Verify generated content before committing
4. **Batch Updates**: Regenerate all READMEs when making structural changes

### Documentation Standards

- **Completeness**: Ensure all datasets have comprehensive documentation
- **Accuracy**: Verify all technical details and links
- **Consistency**: Maintain uniform structure and formatting
- **Accessibility**: Use clear language and proper markdown formatting

## 🚀 Quick Reference Commands

```bash
# Generate all README files
python src/scripts/generate_dataset_readmes.py

# Generate specific dataset README
python src/scripts/generate_dataset_readmes.py --dataset aims

# Update Data.world schemas
python src/scripts/update_dataworld_descriptions.py --all

# Update specific dataset schema
python src/scripts/update_dataworld_descriptions.py khmer --dry-run

# List available datasets
python src/scripts/update_dataworld_descriptions.py --list
```

---

**Note**: This is a living document. Update these instructions when the README generation process or dataset structure changes.

**Last Updated**: 2025-08-17 | **Automation Level**: High | **Maintenance**: Automated
