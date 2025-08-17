# Dataset Addition Guide

This guide provides step-by-step instructions for adding new datasets to the MilitaryHistory project, based on the successful KHMER dataset integration.

## Prerequisites

- Claude Code access
- Virtual environment activated (`.venv/bin/activate`)
- Dataset schema documentation (PDF or other format)
- Dataset NAID and file information

## Step 1: Analyze Dataset Documentation

**Claude Prompt:**
```
I need to add a new dataset called [DATASET_NAME] to the military history project. 

The dataset has:
- NAID: [NAID_NUMBER]
- File name: [FILE_NAME]
- URL: [CATALOG_URL]

I have schema documentation at: [PATH_TO_DOCS]

Please analyze the documentation and examine existing dataset structures in the opsanal directory to understand the field layout and create a complete JSON schema specification. Also check for any lookup table files (like AIMS.8804.CD.*) that provide code-to-description mappings.
```

**Expected Actions:**
- Claude will read the schema documentation
- Examine existing dataset patterns in `opsanal/` subdirectories
- Identify any lookup table files for coded fields
- Create directory structure: `opsanal/[dataset]/schema/schema.json`
- Note any lookup tables in the schema `definition_file` field

## Step 2: Update Configuration

**Claude Prompt:**
```
Add [DATASET_NAME] to the src/config/datasets.json file with:
- NAID: [NAID_NUMBER]
- File name: [FILE_NAME]  
- URL: [FULL_DOWNLOAD_URL or CATALOG_URL]
- Catalog URL: https://catalog.archives.gov/id/[NAID_NUMBER]
- Available online: true
- Delimiter: [width/pipe/tab based on file format]
- is_zipped: true (if the file is a ZIP archive that needs extraction)
```

**Expected Actions:**
- Updates `src/config/datasets.json` with new dataset entry
- Follows existing naming and structure patterns
- Includes ZIP file handling configuration if needed

**File Reuse Behavior:**
The pipeline automatically checks for existing downloaded files before downloading:
- If the file already exists locally, it will be reused (saves time and bandwidth)
- For ZIP files, the pipeline checks for existing extracted directories and reuses them
- Only downloads/extracts when files don't exist or directories are empty
- Provides clear logging about whether files are being downloaded or reused

## Step 3: Create SQL Processing File

**Claude Prompt:**
```
Create a SQL file for [DATASET_NAME] in src/sql/opsanal/[dataset].sql that:

1. Processes the raw data according to the schema
2. Handles coordinate parsing if the dataset contains location data:
   - For LATLONG fields in format ddmmssxDDDMMSSX: Parse into separate LAT/LONG decimal degree columns
   - For UTM coordinates: Keep as-is for later conversion
   - For other coordinate formats: [specify format and parsing needs]
3. Formats dates properly (convert YYMMDD to YYYY-MM-DD format)
4. Includes all fields from the schema specification
5. Uses consistent naming patterns with other datasets
6. If lookup tables exist, include LEFT JOINs to decode coded fields:
   - Add both original code fields AND decoded description fields
   - Handle null/empty values properly (filter out 'nan' strings from pandas)
   - Use proper join conditions with TRIM() and null checks
   - **CRITICAL**: Always use UPPER() for case-insensitive matching to handle mixed case data

Consider the coordinate parsing issues we solved for KHMER - the LATLONG field needs to be split into LATLONG_LAT and LATLONG_LONG columns for WGS-1984 transformation later.

For lookup table integration (like AIMS), the pipeline automatically loads lookup tables from the docs folder, so include LEFT JOINs like:
```sql
LEFT JOIN [dataset]_lookup_[table] AS lookup_alias ON 
    UPPER(TRIM(FIELD_NAME)) = UPPER(lookup_alias.code) AND FIELD_NAME IS NOT NULL AND FIELD_NAME != 'nan' AND FIELD_NAME != ''
```

**Case Sensitivity Note**: Always use `UPPER()` on both sides of the JOIN condition. Source data often contains mixed case values (e.g., `'storm'`, `'Shield'`) while lookup tables may have consistent casing (e.g., `'STORM'`, `'SHIELD'`). Case-insensitive matching prevents failed lookups.
```

**Expected Actions:**
- Creates `src/sql/opsanal/[dataset].sql`
- Implements proper coordinate parsing for transformation pipeline
- Handles date formatting and field processing
- Includes lookup table joins if applicable

## Step 4: Create Processing Script

**Claude Prompt:**
```
Create a processing script at src/scripts/[dataset].py following the pattern of other scripts in that directory. 

The script should:
1. Import datasetprocessor 
2. Set up the correct data.world project name (aragaocb/[dataset-name])
3. Define lat_lon_pairs for any coordinate columns that need WGS-1984 transformation
4. Call the DatasetProcessor with proper parameters

For coordinate pairs, use the column names from the SQL file (e.g., ("LATLONG_LAT", "LATLONG_LONG") for parsed coordinates).
```

**Expected Actions:**
- Creates `src/scripts/[dataset].py` 
- Configures coordinate transformation pairs
- Sets up data.world integration

## Step 5: Test Data Processing Pipeline

**Claude Prompt:**
```
Test the [DATASET_NAME] processing pipeline by:

1. First, check if there are any encoding issues by reading a sample of the raw data file
2. Run the processing script to generate the transformed dataset
3. Verify the output for:
   - No corrupted characters (like â, î, ê that indicate encoding problems)
   - Proper coordinate parsing and transformation
   - Correct date formatting
   - Data completeness and quality

If there are encoding issues, fix the encoding order in src/nara.py by ensuring standard encodings (utf-8, latin-1) are tried before EBCDIC encodings.

Note: For large datasets, the pipeline will automatically reuse existing downloaded/extracted files, making subsequent runs much faster.

**Running Processing Scripts:**
```bash
# Activate virtual environment first
source .venv/bin/activate

# Run standard dataset
python src/scripts/[dataset].py

# Run partitioned dataset (like AIMS) - use master script
python src/scripts/aims.py

# Or run individual partitions
python src/scripts/aims_early_wars.py

# Run analysis/visualization scripts (outputs to visuals/)
python src/scripts/cambodia_folium.py
python src/scripts/create_choropleth_map.py
```
```

**Expected Actions:**
- Tests the complete processing pipeline
- Identifies and fixes any encoding issues
- Validates coordinate transformation
- Ensures data quality
- Benefits from file reuse for faster processing on subsequent runs

## Step 6: Handle Large Datasets (Partitioning)

**Claude Prompt:**
```
The [DATASET_NAME] dataset is too large for data.world (1M+ records). Please implement time-based partitioning:

1. Analyze the temporal distribution using date fields
2. Identify logical historical periods (wars, decades, etc.)
3. Create partitioned SQL files with date filters for each period
4. Create partition processing scripts using PartitionedDatasetProcessor
5. Test one small partition first, then process all partitions

For each partition:
- SQL file: `[dataset]_[period].sql` with appropriate WHERE clause
- Script file: `[dataset]_[period].py` using PartitionedDatasetProcessor class
- Output file: `[dataset]_[period]_tx.csv` uploaded to same data.world project
```

**Centralized PartitionedDatasetProcessor:**
The partitioned processor is now centralized in `src/partitioned_processor.py` for optimal performance:

```python
# src/partitioned_processor.py - Centralized processor with shared resources
class PartitionedDatasetProcessor:
    def __init__(self, dataset: str, datadotworld_project: str, lat_lon_pairs: list = None):
        # Initialize with shared resource management
    
    def process_all_partitions(self, partitions: list = None):
        # Efficiently process all partitions with shared DB connection
        # 1. Load source data ONCE
        # 2. Load lookup tables ONCE  
        # 3. Process all partitions sequentially
        # 4. Close connection ONCE
    
    def process_partition(self, sql_file: str, output_name: str, description: str):
        # Process single partition using existing shared resources
```

**Performance Benefits:**
- ~5x faster processing due to shared resource reuse
- Single database connection lifecycle vs multiple connections
- Source data loaded once and reused across all partitions
- Lookup tables loaded once and shared across partitions
- Minimal memory overhead and I/O operations

**Null Value Handling Requirement:**
All CSV exports MUST clean string 'nan' values and use `na_rep=''` parameter to ensure null values are exported as empty strings:
```python
# REQUIRED - Clean string 'nan' values and export properly
import numpy as np
df_clean = df.replace('nan', np.nan)  # Convert string 'nan' to actual NaN
df_clean.to_csv(csv_file, index=False, na_rep='')  # Export NaN as empty strings

# INCORRECT - Will export string 'nan' values as-is
df.to_csv(csv_file, index=False, na_rep='')
```

**Why This Matters:**
- Data.world receives string 'nan' values from pandas processing
- These appear as literal 'nan' text in data.world instead of proper null values
- The two-step process converts string 'nan' → NaN → empty string for clean uploads

**Expected Actions:**
- Creates multiple SQL files with date-based filtering
- Creates multiple processing scripts for each time period
- Each partition uploads as separate file to same data.world project
- Maintains all features: lookup tables, coordinate transformation, etc.

## Step 7: Handle Common Issues

### Lookup Table Case Sensitivity Problems  
If lookup descriptions aren't appearing or you see original codes in the output instead of descriptions:

**Claude Prompt:**
```
The lookup table integration isn't working correctly - I'm seeing raw codes like 'storm' instead of descriptions like 'DESERT STORM' in the output.

This is usually a case sensitivity issue. Please check all lookup JOIN conditions in the SQL files and ensure they use UPPER() on both sides:

CORRECT: UPPER(TRIM(FIELD_NAME)) = UPPER(lookup_table.code)
INCORRECT: TRIM(FIELD_NAME) = lookup_table.code

Test the fix by checking a small sample of the data to verify descriptions are appearing.
```

### Encoding Problems
If you see corrupted characters in the output:

**Claude Prompt:**
```
The dataset output shows corrupted characters (â, î, ê, etc.). This indicates an encoding issue. 

Please check the encoding order in src/nara.py and ensure that standard encodings (utf-8, latin-1, cp1252, iso-8859-1) are tried before EBCDIC encodings (cp037, cp500, cp1140) in the encodings_to_try list.

Test the fix by re-running the processing pipeline.
```

### Coordinate Parsing Issues
If coordinates aren't parsing correctly:

**Claude Prompt:**
```
The coordinate parsing for [DATASET_NAME] isn't working correctly. Please:

1. Examine the raw coordinate format in the data
2. Update the SQL parsing logic to handle the specific format
3. Ensure the coordinate columns are properly named for the transformation pipeline
4. Test the coordinate conversion with sample data
```

### Missing Schema Information
If schema documentation is incomplete:

**Claude Prompt:**
```
The schema documentation for [DATASET_NAME] is incomplete. Please:

1. Examine similar datasets in the opsanal directory
2. Analyze the raw data file structure to infer field meanings
3. Create a best-effort schema based on patterns from similar datasets
4. Document any assumptions made for future reference
```

## Step 7: Verify Integration

**Claude Prompt:**
```
Verify the complete [DATASET_NAME] integration by:

1. Running the processing script successfully
2. Checking that the output CSV has proper data formatting
3. Confirming coordinate transformation is working (if applicable)
4. Ensuring the dataset follows the same patterns as other datasets in the project

Generate a summary of what was created and any special considerations for this dataset.
```

## Common Dataset Types and Patterns

### Geographic Datasets (with coordinates)
- Usually need coordinate parsing and WGS-1984 transformation
- Common formats: UTM, MGRS, Lat/Long in various formats
- Require lat_lon_pairs configuration in processing script

### Incident/Event Datasets
- Usually have date/time fields requiring formatting
- Often have coded fields requiring lookup tables
- May have location information

### Personnel/Unit Datasets (like AIMS)
- Focus on categorical data and identifiers
- Less likely to need coordinate transformation
- Often have hierarchical relationships
- **Frequently include lookup tables** for coded fields (awards, ranks, campaigns, etc.)
- Benefit greatly from lookup table integration for human-readable output

### Lookup Table Integration
**Automatic Support**: The pipeline automatically detects and loads lookup table files in the `opsanal/[dataset]/docs/` folder:
- Supports various formats: code+description, code-only
- Creates `[dataset]_lookup_[suffix]` tables in DuckDB
- Examples: AIMS.8804.CD.AWD → aims_lookup_awd table
- No manual configuration needed - just place files in docs folder

## File Structure Summary

After completing these steps, you should have:

### Standard Dataset:
```
opsanal/[dataset]/
├── docs/
│   ├── [schema_documentation]
│   └── [lookup_tables] (if applicable)
├── schema/
│   └── schema.json
└── data/
    └── [dataset_file] (downloaded automatically)

src/
├── config/
│   └── datasets.json (updated)
├── sql/opsanal/
│   └── [dataset].sql
└── scripts/
    └── [dataset].py

datasets/
└── [dataset]_tx.csv (generated output)
```

### Partitioned Dataset (for large datasets):
```
opsanal/[dataset]/
├── docs/
│   ├── [schema_documentation]
│   └── [lookup_tables] (automatically loaded, *.DOC files excluded)
├── schema/
│   └── schema.json
└── data/
    └── [dataset_file] (downloaded automatically)

src/
├── partitioned_processor.py         # CENTRALIZED: Optimized processor with shared resources
├── config/
│   └── datasets.json               # Base dataset config
├── sql/opsanal/
│   ├── [dataset].sql               # Original (if needed)
│   ├── [dataset]_period1.sql       # Partition 1 SQL
│   ├── [dataset]_period2.sql       # Partition 2 SQL
│   └── [dataset]_periodN.sql       # Partition N SQL
└── scripts/
    ├── [dataset].py                # OPTIMIZED: Master script using centralized processor
    ├── [dataset]_period1.py        # SIMPLIFIED: Thin wrapper using centralized processor
    ├── [dataset]_period2.py        # SIMPLIFIED: Thin wrapper using centralized processor
    └── [dataset]_periodN.py        # SIMPLIFIED: Thin wrapper using centralized processor

Data.world project: [user]/[project]
├── [dataset]_period1_tx.csv
├── [dataset]_period2_tx.csv
└── [dataset]_periodN_tx.csv
```

**Key Optimizations:**
- **Centralized Processor**: Single `partitioned_processor.py` vs duplicated classes
- **Shared Resources**: Master script loads data once, processes all partitions
- **Thin Wrappers**: Individual scripts now use centralized processor
- **Performance**: ~5x faster processing with reduced memory overhead

## Tips for Success

1. **Follow Existing Patterns**: Always examine similar datasets first
2. **Test Early and Often**: Run the pipeline early to catch issues
3. **Document Assumptions**: Note any decisions made about ambiguous schema elements
4. **Verify Coordinates**: Geographic data requires special attention to coordinate systems
5. **Check Encoding**: Historical datasets often have encoding challenges
6. **Leverage File Reuse**: Large files are automatically reused between runs - no need to re-download
7. **Utilize Lookup Tables**: If the dataset has coded fields, look for lookup/reference files in the documentation
8. **Plan for Lookup Integration**: Include both original codes AND decoded descriptions in your SQL output
9. **Handle Null Values Properly**: Always use `na_rep=''` parameter in `to_csv()` calls to ensure null values upload as empty strings, not 'nan'
10. **Use Case-Insensitive Lookups**: Always use `UPPER()` on both sides of lookup JOINs to handle mixed case data in source files

## New Features Added

### Automatic File Reuse (Added 2025-08-16)
- **What**: Downloaded files and extracted ZIP contents are automatically reused
- **Why**: Prevents timeouts and saves bandwidth for large datasets
- **How**: Pipeline checks for existing files before downloading/extracting

### Lookup Table Integration (Added 2025-08-16)  
- **What**: Automatic loading and joining of lookup/reference tables
- **Why**: Provides human-readable descriptions for coded fields (awards, ranks, etc.)
- **How**: Place lookup files in `opsanal/[dataset]/docs/` folder, SQL automatically joins them
- **Note**: Documentation files (*.DOC) are automatically excluded from lookup table processing

### Time-Based Dataset Partitioning (Added 2025-08-16)
- **What**: Split large datasets into time-based partitions for manageable upload sizes
- **Why**: Enables processing of datasets too large for data.world (1M+ records)
- **How**: Create multiple SQL files with date filters and custom processing scripts
- **Example**: AIMS dataset partitioned into 5 historical periods (Early Wars, Korea, Vietnam, Post-Vietnam, Gulf War)

#### AIMS Master Script Usage:
The AIMS dataset includes an optimized master script that processes all partitions efficiently:

```bash
# Run all AIMS partitions (recommended - 5x faster than individual scripts)
python src/scripts/aims.py

# Or run individual partitions (less efficient due to resource reloading)
python src/scripts/aims_early_wars.py
python src/scripts/aims_vietnam_era.py
# etc.
```

**Optimized Master Script Features:**
- **Performance**: ~5x faster than running individual scripts sequentially
- **Resource Efficiency**: Loads 1.1M source file once, reuses across all 5 partitions
- **Database Optimization**: Single connection lifecycle eliminates overhead
- **Lookup Table Sharing**: Loads lookup tables once, shares across partitions
- **Progress Tracking**: Comprehensive logging with timestamps and partition details
- **Error Resilience**: Individual partition failures don't stop remaining processing
- **Memory Stability**: Consistent memory usage vs previous sawtooth pattern
- **Output**: 5 separate files uploaded to data.world (aims_early_wars_tx.csv, etc.)

**Performance Comparison:**
- **Old Approach**: ~25-50 minutes (5 × full resource loading)
- **New Approach**: ~5-10 minutes (1 × resource loading + 5 × partition processing)

#### When to Use Partitioning:
- Dataset exceeds 500K-1M records 
- Natural temporal divisions exist (wars, decades, etc.)
- Users would benefit from period-specific analysis

#### Partitioning Implementation:
1. **Create time-period SQL files**: `aims_vietnam_era.sql`, `aims_gulf_war_era.sql`, etc.
2. **Add date filters**: `WHERE CAST(SUBSTR(TRIM(DATE_FIELD), -4) AS INTEGER) BETWEEN 1965 AND 1975`
3. **Create partition scripts**: Use `PartitionedDatasetProcessor` class with custom SQL files
4. **Create master script**: Combine all partitions into a single executable script
5. **Upload separately**: Each partition uploads as separate file (`aims_vietnam_era_tx.csv`)

#### Optimized Master Script for Partitioned Datasets:
The master script now uses the centralized processor for maximum efficiency:

```python
#!/usr/bin/env python3
"""Optimized master script using centralized processor."""

from partitioned_processor import PartitionedDatasetProcessor

def main():
    # Create optimized processor with shared resources
    processor = PartitionedDatasetProcessor(
        dataset="dataset_name",
        datadotworld_project="user/project",
        lat_lon_pairs=[]
    )
    
    # Process all partitions efficiently (loads data once, processes all)
    exit_code = processor.process_all_partitions()
    return exit_code
```

**Optimized Master Script Benefits:**
- **5x Performance Improvement**: Shared resource reuse eliminates redundant operations
- **Single Resource Lifecycle**: Load → Process All → Close (vs Load → Process → Close × N)
- **Memory Efficiency**: Stable memory usage vs sawtooth pattern of previous approach
- **Comprehensive Logging**: Timestamped progress tracking with partition details
- **Automatic Error Handling**: Individual partition failures don't stop remaining processing
- **Database Safety**: No connection conflicts between partitions

This process should make adding new datasets much more systematic and reliable!