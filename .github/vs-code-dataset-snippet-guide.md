# VS Code Dataset Ingestion Snippet Implementation Guide

## Overview
This guide explains how to use the VS Code snippet template created from lessons learned during the VSSG dataset ingestion. The snippet provides a comprehensive template that addresses all the key issues and requirements discovered during the process.

## Installation and Setup

### 1. Snippet Location
The snippet file is already created at:
```
/home/chris/Documents/MilitaryHistory/.vscode/dataset-ingestion.code-snippets
```

### 2. VS Code Configuration
The snippet will automatically be available when you're working in this workspace. To use it:

1. Open any file in the MilitaryHistory workspace
2. Type `dataset-ingestion-prompt` 
3. Press `Tab` or `Enter` to expand the template
4. Use `Tab` to navigate between the placeholders

### 3. Alternative: Global Installation
If you want this snippet available in all workspaces:
```bash
# Copy to global VS Code snippets directory
cp .vscode/dataset-ingestion.code-snippets ~/.config/Code/User/snippets/
```

## How to Use the Snippet

### Step 1: Create New Dataset Request File
1. Create a new file: `opsanal/[dataset-name]/prompt/[dataset-name].prompt`
2. Type `dataset-ingestion-prompt` and press Tab
3. Fill in all the placeholder values

### Step 2: Fill Out the Template
The snippet includes 23 configurable parameters. Here's what each one represents:

#### Basic Information
- `${1:DATASET_NAME}` - Short dataset identifier (e.g., "vssg", "aims", "khmer")
- `${2:Full Dataset Title}` - Complete official title
- `${3:Start Date}` - Dataset temporal coverage start
- `${4:End Date}` - Dataset temporal coverage end
- `${5:NAID_NUMBER}` - NARA identifier number

#### Data Files
- `${6:filename.txt}` - Primary data file name
- `${7:https://s3.amazonaws.com/...}` - Full download URL
- `${8|format|}` - File format (tab-delimited/pipe-delimited/fixed-width/CSV)
- `${9|true/false|}` - Whether file is zipped

#### Documentation
- `${10:schema_file}` - Main schema documentation file
- `${11:lookup_file}` - Lookup table documentation
- `${12:additional_docs}` - Other documentation files

#### Configuration
- `${13:dataworld-project-name}` - Data.world project identifier
- `${14|size|}` - Expected dataset size category
- `${15|coordinates|}` - Whether dataset contains geographic data
- `${16:coordinate_format}` - Format of coordinate data
- `${17:coordinate_fields}` - Names of coordinate fields

#### Processing Requirements
- `${18|lookup_needed|}` - Whether lookup tables are required
- `${19:date_fields}` - Names of date/time fields
- `${20:special_processing}` - Any special requirements
- `${21:lookup_types}` - Types of lookup tables needed
- `${22|delimiter|}` - Delimiter type for datasets.json
- `${23:lat_lon_pairs}` - Coordinate pairs for transformation

## Lessons Learned Integration

### Key Issues Addressed in the Template

#### 1. Schema Structure Problems
**Issue**: VSSG initially had incorrect schema format that didn't match DatasetProcessor expectations
**Solution**: Template includes explicit field format requirements:
- All fields must have `field_group: "FIELD"`
- Correct data_values types (Numeric vs Alphanumeric)
- Proper length specifications

#### 2. SQL Type Conversion Errors
**Issue**: SQL failed with type conversion errors (BIGINT to VARCHAR, etc.)
**Solution**: Template mandates:
- Use `TRY_CAST` instead of `CAST` for robustness
- Cast all fields to VARCHAR before string operations
- Explicit type handling for all operations

#### 3. Table Name Mismatch
**Issue**: SQL referenced wrong table name (`vssg_data` vs `vssg_nara`)
**Solution**: Template specifies correct pattern: `{dataset}_nara`

#### 4. Column Name Issues
**Issue**: SQL referenced fields without the '+' prefix that existed in actual data
**Solution**: Template emphasizes checking actual column headers and matching exactly

#### 5. Missing Lookup Table Integration
**Issue**: Original prompt didn't specify lookup table creation methodology
**Solution**: Template includes:
- Specific JSON format for lookup tables
- Case-insensitive JOIN patterns with UPPER()
- Proper null value handling

#### 6. Data.world Integration Missing
**Issue**: README upload failed because mapping wasn't configured
**Solution**: Template includes explicit step to update dataworld_mapping

#### 7. Incomplete Field Coverage
**Issue**: Schema only covered 18 of 32 actual fields
**Solution**: Template emphasizes examining actual data structure and including all fields

#### 8. Encoding and Error Handling
**Issue**: Various data quality and encoding issues
**Solution**: Template includes comprehensive troubleshooting section

## Best Practices for Implementation

### 1. Pre-Implementation Research
Before using the snippet:
- Download and examine the actual data file
- Count columns: `head -1 datafile.txt | wc -w`
- Review documentation thoroughly
- Check for similar datasets in the project

### 2. Systematic Execution
Follow the numbered steps exactly:
1. Documentation analysis first
2. Schema creation with all fields
3. Configuration updates
4. SQL development with proper type handling
5. Testing and validation
6. Integration and documentation

### 3. Validation Checkpoints
At each step, verify:
- Field counts match actual data
- Column names match exactly (including special characters)
- Data types are appropriate
- Lookup tables load correctly
- SQL executes without errors

### 4. Testing Strategy
- Test with small data samples first
- Verify coordinate transformation (if applicable)
- Check lookup table integration
- Validate date formatting
- Ensure clean null value handling

## Common Failure Patterns and Solutions

### 1. Schema Field Count Mismatch
**Error**: `ValueError: Length mismatch: Expected axis has X elements, new values have Y elements`
**Solution**: Count actual columns and ensure schema includes all fields

### 2. SQL Type Conversion Errors
**Error**: `No function matches the given name and argument types`
**Solution**: Add explicit CAST operations: `CAST(field AS VARCHAR)`

### 3. Missing Lookup Descriptions
**Error**: Seeing codes instead of descriptions in output
**Solution**: Check JOIN conditions use UPPER() and proper null handling

### 4. Encoding Problems
**Error**: Corrupted characters (â, î, ê) in output
**Solution**: Check encoding order in src/nara.py

### 5. Data.world Upload Failures
**Error**: README upload skipped or dataset not found
**Solution**: Verify dataworld_mapping is updated

## Snippet Maintenance

### When to Update the Snippet
- After successfully ingesting new dataset types
- When discovering new common failure patterns
- When project structure or requirements change

### How to Update
1. Edit `.vscode/dataset-ingestion.code-snippets`
2. Add new placeholder variables for new requirements
3. Update troubleshooting section with new issues
4. Test with next dataset ingestion

## Advanced Usage

### For Large Datasets (>1M records)
The template includes partitioning guidance:
- Time-based partitioning strategy
- PartitionedDatasetProcessor usage
- Performance optimization techniques
- Master script creation

### For Geographic Datasets
Special handling for coordinate data:
- UTM coordinate preservation
- Lat/Long parsing requirements
- MGRS handling
- WGS-1984 transformation setup

### For Complex Lookup Tables
Advanced lookup integration:
- Multiple lookup table handling
- Hierarchical code structures
- Case sensitivity management
- Performance optimization

## Conclusion

This snippet template encapsulates all the lessons learned from the VSSG dataset ingestion process and provides a systematic approach to future dataset additions. By following the template exactly and using the comprehensive troubleshooting guide, you should be able to successfully ingest new datasets while avoiding the common pitfalls encountered during VSSG development.

The template is designed to be:
- **Comprehensive**: Covers all aspects of dataset ingestion
- **Systematic**: Provides step-by-step guidance
- **Robust**: Includes error handling and troubleshooting
- **Maintainable**: Easy to update with new lessons learned

Use this template for all future dataset ingestions to ensure consistency and reliability in the military history data processing pipeline.
