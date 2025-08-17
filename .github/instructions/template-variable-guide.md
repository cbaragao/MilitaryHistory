---
priority: 2
description: "Complete template variable substitution guide for GitHub Copilot"
applyTo: "**/*.{js,ts,json}"
---

# Template Variable Substitution Guide

## How to Use Templates

**IMPORTANT**: Templates use `{{variable_name}}` placeholders that MUST be replaced with actual values. Never leave `{{}}` syntax in final output.

### Variable Substitution Process

1. **Identify data structure** - understand your data fields
2. **Map template variables** - match `{{variables}}` to your data columns  
3. **Replace ALL placeholders** - substitute with actual field names/values
4. **Validate accessibility** - ensure result passes CVD validation

## Complete Variable Reference

### Chart Metadata Variables

#### `{{chart_title}}`
- **Purpose**: Main chart title displayed at top
- **Format**: Sentence case, action-oriented
- **Examples**: 
  - ✅ "Monthly air missions increased 300% during 1968-1969"
  - ✅ "Top 10 countries by military casualties"
  - ❌ "Air Missions Chart" (not insight-focused)

#### `{{alt_text_following_cesal_formula}}`
- **Purpose**: Screen reader description following Amy Cesal formula
- **Format**: "Chart type of [data type] where [key insight]"
- **Examples**:
  - ✅ "Line chart of monthly air missions where South Vietnam peaked at 45,000 missions in March 1969"
  - ✅ "Horizontal bar chart of casualty counts where Vietnam War had highest losses at 58,000"
  - ❌ "Chart showing data" (not descriptive enough)

### Data Source Variables

#### `{{data_source_url}}`
- **Purpose**: URL or path to data file
- **Format**: Valid URL or relative file path
- **Examples**:
  - ✅ "data/vietnam-air-missions.csv"
  - ✅ "https://api.example.com/military-data.json"
  - ✅ "datasets/casualty-reports.tsv"

### Data Field Variables

#### `{{value_field}}`
- **Purpose**: Numeric field for quantitative data
- **Data Type**: Must be numeric (integer or float)
- **Examples**:
  - ✅ "mission_count", "casualties", "aircraft_deployed"
  - ❌ "date", "country_name" (not numeric)

#### `{{category_field}}`
- **Purpose**: Categorical field for grouping data  
- **Data Type**: String/text values
- **Examples**:
  - ✅ "country", "military_branch", "operation_name"
  - ❌ "casualty_count" (numeric, not categorical)

#### `{{date_field}}`
- **Purpose**: Temporal field for time series
- **Data Type**: Date/datetime format
- **Examples**:
  - ✅ "mission_date", "operation_start", "report_timestamp"
  - **Required Format**: ISO 8601 (YYYY-MM-DD) or parseable date

#### `{{series_field}}`
- **Purpose**: Field that creates multiple data series
- **Data Type**: Categorical with limited unique values (≤4 recommended)
- **Examples**:
  - ✅ "military_branch" (Army, Navy, Air Force, Marines)
  - ✅ "theater" (Europe, Pacific, Atlantic)

#### `{{facet_field}}`
- **Purpose**: Field for creating small multiples (separate charts)
- **Data Type**: Categorical
- **Examples**:
  - ✅ "operation_name", "year", "command_region"

### Axis and Legend Variables

#### `{{x_axis_title}}` / `{{y_axis_title}}`
- **Purpose**: Descriptive labels for chart axes
- **Format**: Noun phrases, units included if applicable
- **Examples**:
  - ✅ "Number of missions", "Casualties (thousands)", "Date"
  - ❌ "X", "Data" (not descriptive)

#### `{{legend_title}}`
- **Purpose**: Title for chart legend
- **Format**: Descriptive of what the colors/patterns represent
- **Examples**:
  - ✅ "Military branch", "Operation theater", "Aircraft type"

### Configuration Variables (with defaults)

#### `{{max_categories:10}}`
- **Purpose**: Limit number of categories shown (prevents overcrowding)
- **Default**: 10 if not specified
- **Examples**: `{{max_categories:5}}`, `{{max_categories:15}}`

#### `{{mark_type:line}}`
- **Purpose**: Specify chart mark type
- **Default**: "line" if not specified
- **Options**: "line", "bar", "point", "area"

#### `{{x_type:temporal}}` / `{{y_type:quantitative}}`
- **Purpose**: Specify data type for proper encoding
- **Options**: "temporal", "quantitative", "nominal", "ordinal"

#### `{{date_format:%Y-%m}}`
- **Purpose**: Format dates in chart display
- **Default**: "%Y-%m" (Year-Month)
- **Examples**: "%Y" (year only), "%b %Y" (Jan 2023)

## Data Structure Requirements

### Expected Data Format (CSV/JSON)

```csv
date,country,military_branch,mission_count,casualties
1968-01-01,South Vietnam,Air Force,1200,45
1968-01-01,South Vietnam,Army,3400,120
1968-02-01,South Vietnam,Air Force,1500,38
```

```json
[
  {
    "date": "1968-01-01",
    "country": "South Vietnam", 
    "military_branch": "Air Force",
    "mission_count": 1200,
    "casualties": 45
  }
]
```

## Template Substitution Examples

### Before Substitution (Template):
```json
{
  "title": {"text": "{{chart_title}}"},
  "description": "{{alt_text_following_cesal_formula}}",
  "data": {"url": "{{data_source_url}}"},
  "encoding": {
    "x": {"field": "{{date_field}}", "type": "temporal"},
    "y": {"field": "{{value_field}}", "type": "quantitative"}
  }
}
```

### After Substitution (Working Chart):
```json
{
  "title": {"text": "Monthly air missions peaked during Tet Offensive"},
  "description": "Line chart of monthly mission counts where peak occurred in March 1968 with 15,000 missions",
  "data": {"url": "data/vietnam-air-missions.csv"},
  "encoding": {
    "x": {"field": "mission_date", "type": "temporal"},
    "y": {"field": "mission_count", "type": "quantitative"}
  }
}
```

## Common Substitution Errors to Avoid

❌ **Leaving template syntax**: `"title": "{{chart_title}}"` in final output
❌ **Wrong data types**: Using text field for `{{value_field}}`
❌ **Missing required fields**: Not substituting mandatory variables
❌ **Invalid field names**: Using fields that don't exist in data
❌ **Non-accessible titles**: Generic titles instead of insight-focused

✅ **Correct approach**: All `{{}}` replaced with actual values matching your data structure

## Quick Reference by Template Type

### Time Series Template Variables:
- `{{chart_title}}`, `{{alt_text_following_cesal_formula}}`
- `{{data_source_url}}`
- `{{date_field}}`, `{{value_field}}`, `{{series_field}}`
- `{{y_axis_title}}`, `{{legend_title}}`
- `{{date_format:%Y-%m}}`

### Horizontal Bar Template Variables:
- `{{chart_title}}`, `{{alt_text_following_cesal_formula}}`
- `{{data_source_url}}`
- `{{category_field}}`, `{{value_field}}`
- `{{x_axis_title}}`
- `{{max_categories:10}}`

### Small Multiples Template Variables:
- `{{chart_title}}`, `{{alt_text_following_cesal_formula}}`
- `{{data_source_url}}`
- `{{facet_field}}`, `{{x_field}}`, `{{y_field}}`
- `{{mark_type:line}}`, `{{x_type:temporal}}`
- `{{y_axis_title}}`, `{{date_format:%Y}}`