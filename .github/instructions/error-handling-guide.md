---
priority: 2
description: "Error handling and edge case resolution for GitHub Copilot"
applyTo: "**/*.{js,ts,json}"
---

# Error Handling & Edge Case Resolution Guide

## Critical Rule: NEVER Compromise Accessibility

**When in doubt, ALWAYS choose the more accessible option.** No aesthetic preference overrides accessibility requirements.

## Decision Trees for Common Conflicts

### 1. Too Many Data Series (>4)

```
User requests visualization with 5+ data series
├── Are series showing similar patterns?
│   ├── YES → Use small multiples template (preferred)
│   └── NO → Continue to next decision
├── Is one series clearly primary/most important?
│   ├── YES → Highlight primary series, gray out others
│   └── NO → Continue to next decision
├── Are users comparing specific values?
│   ├── YES → Use horizontal bar chart (rank by importance)
│   └── NO → Continue to next decision
└── FALLBACK: Limit to 3 most important series
    └── Explain in alt text which series were excluded and why
```

**Implementation:**
```json
{
  "layer": [
    {
      "mark": {"type": "line", "color": "#CCCCCC", "strokeWidth": 1},
      "transform": [{"filter": "datum.series != 'Primary'"}],
      "encoding": {"detail": {"field": "series"}}
    },
    {
      "mark": {"type": "line", "color": "#4477AA", "strokeWidth": 3},
      "transform": [{"filter": "datum.series == 'Primary'"}]
    }
  ]
}
```

### 2. Insufficient Safe Colors

```
Need more colors than Paul Tol palette allows safely
├── Can categories be grouped/consolidated?
│   ├── YES → Group similar categories, use "Other" category
│   └── NO → Continue to next decision
├── Can you use small multiples instead?
│   ├── YES → Use faceting to reduce colors per chart
│   └── NO → Continue to next decision
├── Can you use patterns/shapes only (no color distinction)?
│   ├── YES → Use grayscale + patterns + shapes
│   └── NO → FALLBACK: Use safe 4-color subset
└── NEVER use unsafe color combinations
```

**Safe Color Limits:**
- 3 colors: `["#4477AA", "#CC6677", "#66CCEE"]`
- 4 colors: `["#4477AA", "#CC6677", "#66CCEE", "#BBBBBB"]`
- 5+ categories: **MUST use small multiples or patterns**

### 3. Missing Required Data Fields

```
Template variable has no matching field in data
├── Is there a similar field that could work?
│   ├── YES → Use closest equivalent, document in alt text
│   └── NO → Continue to next decision
├── Can the visualization work without this field?
│   ├── YES → Use simpler template, maintain accessibility
│   └── NO → Continue to next decision
└── FALLBACK: Request user provide correct data structure
    └── Explain which fields are required and why
```

### 4. Template Selection Conflicts

```
Multiple templates could work for the data
├── Does data have temporal component?
│   ├── YES → Use time-series template
│   └── NO → Continue to next decision
├── Is this primarily about ranking/comparison?
│   ├── YES → Use horizontal bar template
│   └── NO → Continue to next decision
├── Are there 4+ categories/series?
│   ├── YES → Use small multiples template
│   └── NO → Use simplest appropriate template
```

## Fallback Patterns

### When Accessibility Requirements Conflict with User Requests

**User Request**: "Make it clean - remove the patterns and shapes"
**Copilot Response**: 
```
I need to keep the patterns and shapes for accessibility compliance. 
These ensure users with color vision deficiency can distinguish the data. 
I can make them more subtle while maintaining accessibility.
```

**Implementation**: Use subtle patterns that maintain distinction:
```json
{
  "strokeDash": {
    "scale": {"range": [[1,0], [4,2], [2,2]]},
    "legend": null
  }
}
```

### When Data Doesn't Match Any Template

**Scenario**: Complex data structure that doesn't fit standard templates

**Resolution Process**:
1. **Identify core insight** user wants to show
2. **Select closest template** that maintains accessibility
3. **Adapt data** through transforms to fit template
4. **Document limitations** in alt text

**Example**:
```json
{
  "transform": [
    {"filter": "datum.year >= 1965"},
    {"aggregate": [{"op": "sum", "field": "missions", "as": "total_missions"}],
     "groupby": ["year"]},
    {"window": [{"op": "rank", "as": "rank"}], 
     "sort": [{"field": "total_missions", "order": "descending"}]},
    {"filter": "datum.rank <= 10"}
  ]
}
```

### When Color Validation Fails

**Scenario**: User data requires color combinations that fail CVD validation

**Resolution Steps**:
1. **NEVER override color safety** - accessibility is non-negotiable
2. **Explain the issue** clearly
3. **Offer safe alternatives**

**Response Template**:
```
I cannot use red and green together as this creates accessibility barriers 
for 8% of men with color vision deficiency. Instead, I'll use:
- Blue (#4477AA) and pink (#CC6677) for color distinction
- Plus patterns and shapes for redundant encoding
This ensures everyone can read your visualization.
```

## Error Recovery Strategies

### When Validation Functions Throw Errors

```javascript
function safeChartGeneration(spec) {
  try {
    // Apply all validation
    enforceComprehensiveCVDSafety(spec);
    requireMonochromacySupport(spec);
    return spec;
  } catch (error) {
    // Log error for debugging
    console.warn('Accessibility validation failed:', error.message);
    
    // Apply safe fallback
    return applyAccessibilityFallback(spec);
  }
}

function applyAccessibilityFallback(spec) {
  // Force safe color palette
  if (spec.encoding?.color?.scale?.range) {
    spec.encoding.color.scale.range = ["#4477AA", "#BBBBBB"];
  }
  
  // Add required alternative encodings
  if (spec.encoding?.color && !spec.encoding?.strokeDash) {
    spec.encoding.strokeDash = {
      "field": spec.encoding.color.field,
      "scale": {"range": [[1,0], [8,4]]},
      "legend": null
    };
  }
  
  // Ensure keyboard navigation
  spec.config = spec.config || {};
  spec.config.view = spec.config.view || {};
  spec.config.view.keyboard = true;
  
  return spec;
}
```

### When User Requests Override Safety

**Never Allow**:
- Red-green color combinations
- Missing alt text
- Color-only data distinction
- Removal of keyboard navigation

**Response Strategy**:
```
I understand you'd prefer [user request], but this would create accessibility 
barriers for users with disabilities. Federal Section 508 compliance requires 
[specific requirement]. I can achieve your visual goals while maintaining 
accessibility by [alternative approach].
```

## Emergency Fallbacks (Last Resort)

### Universal Safe Visualization
When all else fails, use this minimal accessible pattern:

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {"text": "Data visualization (simplified for accessibility)"},
  "description": "Chart showing data with accessibility compliance",
  "mark": {"type": "bar", "color": "#4477AA", "stroke": "white", "strokeWidth": 2},
  "encoding": {
    "x": {"field": "category", "type": "nominal"},
    "y": {"field": "value", "type": "quantitative"}
  },
  "config": {"view": {"keyboard": true}}
}
```

### When Data is Completely Incompatible

**Response**: 
```
This data structure doesn't match our accessible visualization templates. 
To create an accessible chart, I need data with [specific requirements]. 
Would you like me to:
1. Suggest data restructuring, or
2. Create a simple accessible chart with available fields?
```

## Testing Edge Case Responses

Before implementing any solution, verify:
- [ ] Passes all CVD validation functions
- [ ] Includes required alternative encodings  
- [ ] Has proper alt text and keyboard navigation
- [ ] Maintains core data insight
- [ ] Provides clear explanation to user