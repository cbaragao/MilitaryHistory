---
priority: 1
description: "Combined accessibility compliance and UX standards"
replaces: ["508-compliance-instructions.md", "ux-validation.md"]
applyTo: "**/*.{js,ts,json,md}"
---

# Accessible UX Standards

## SECTION 1: Legal Requirements (MANDATORY - Non-negotiable)

### WCAG 2.1 Success Criteria Implementation

**1.1.1 Non-text Content (Level A)** - MANDATORY
- Every chart MUST have `description` field
- Use Amy Cesal formula: "Chart type of [data type] where [reason]"

**1.4.1 Use of Color (Level A)** - MANDATORY
- Never rely solely on color for information
- Always include alternative encodings (patterns, shapes, direct labels)

**1.4.3 Contrast (Level AA)** - MANDATORY
- Graphics: minimum 3:1 contrast ratio
- Add white stroke borders to bars/points
- Use Paul Tol palettes (pre-tested for contrast)

**2.5.1 Pointer Gestures (Level A)** - MANDATORY
- Single-point activation for all interactions
- Keyboard alternatives: `"view": {"keyboard": true}`

### Legal Compliance Validation Template

```javascript
function validateLegalCompliance(spec) {
  const compliance = {
    hasDescription: !!spec.description,
    hasColorAlternatives: hasAlternativeEncodings(spec.encoding),
    usesAccessibleColors: isAccessiblePalette(spec.encoding.color?.scale?.range),
    hasProperContrast: hasStrokeBorders(spec.mark),
    keyboardAccessible: !!spec.view?.keyboard
  };
  
  // ALL must be true for legal compliance
  return Object.values(compliance).every(Boolean);
}
```

## SECTION 2: Accessibility Excellence Standards (Beyond minimum compliance)

### Accessibility Excellence Checklist (HIGHLY PREFERRED)
Before generating ANY visualization, validate:
- [ ] Can users with color vision deficiency distinguish all data?
- [ ] Are there at least 3 ways to distinguish categories (color + pattern + shape)?
- [ ] Can screen readers interpret all information?
- [ ] Is the chart navigable by keyboard only?
- [ ] Would a user with cognitive disabilities understand this?

### Cognitive Accessibility Assessment (HIGHLY PREFERRED)

**HIGH Load (AVOID)**
- 4+ overlapping time series
- Multiple legends for same dimension
- Color-only differentiation
- Dense overlapping data points

**MEDIUM Load (CAUTION)**
- 3 time series with clear separation
- Single legend with 4+ items
- Mixed chart types in single view

**LOW Load (PREFERRED)**
- 1-2 data series
- Clear visual hierarchy
- Direct labeling when possible
- Single focused insight

### Multi-Series Decision Framework

When user requests 4+ data series:

1. **Check patterns**: Similar trends? → Small multiples (PREFERRED)
2. **Check importance**: One primary? → Highlight primary, gray others
3. **Check task**: Comparing values? → Horizontal bar chart
4. **Check temporal**: Trends essential? → Limit to 3 most important

#### Small Multiples Template (PREFERRED)
```json
{
  "facet": {
    "field": "category",
    "type": "nominal", 
    "columns": 2
  },
  "spec": {
    "mark": {"type": "line", "color": "#4477AA", "stroke": "white", "strokeWidth": 1},
    "encoding": {
      "x": {"field": "date", "type": "temporal"},
      "y": {"field": "value", "type": "quantitative"}
    }
  }
}
```

#### Highlight + Context Template
```json
{
  "layer": [
    {
      "mark": {"type": "line", "color": "#CCCCCC", "strokeWidth": 1},
      "encoding": {
        "detail": {"field": "series", "type": "nominal"},
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "value", "type": "quantitative"}
      }
    },
    {
      "mark": {"type": "line", "color": "#4477AA", "strokeWidth": 3, "stroke": "white", "strokeOpacity": 1},
      "transform": [{"filter": "datum.series == 'Primary'"}],
      "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "value", "type": "quantitative"}
      }
    }
  ]
}
```

## SECTION 3: Unified Validation System

### Comprehensive Accessibility & UX Checker

```javascript
function validateAccessibleUX(spec) {
  // STEP 1: Legal compliance (must pass all)
  const legal = validateLegalCompliance(spec);
  if (!legal) {
    return { valid: false, reason: "Legal compliance failure" };
  }
  
  // STEP 2: UX validation (warnings only)
  const ux = {
    cognitiveLoad: assessCognitiveLoad(spec),
    legendCount: countLegends(spec),
    seriesCount: countDataSeries(spec),
    fiveSecondTest: canUnderstandInFiveSeconds(spec)
  };
  
  // STEP 3: Consolidate legends if multiple exist
  if (ux.legendCount > 1) {
    spec = consolidateLegends(spec);
  }
  
  return { 
    valid: true, 
    compliance: legal,
    ux: ux,
    spec: spec
  };
}

function consolidateLegends(spec) {
  const legendFields = [];
  
  if (spec.encoding.color?.legend !== null) legendFields.push('color');
  if (spec.encoding.shape?.legend !== null) legendFields.push('shape');
  if (spec.encoding.strokeDash?.legend !== null) legendFields.push('strokeDash');
  
  // Keep only the highest priority legend: Color > Shape > StrokeDash
  if (legendFields.length > 1) {
    if (legendFields.includes('color')) {
      if (spec.encoding.shape) spec.encoding.shape.legend = null;
      if (spec.encoding.strokeDash) spec.encoding.strokeDash.legend = null;
    } else if (legendFields.includes('shape')) {
      if (spec.encoding.strokeDash) spec.encoding.strokeDash.legend = null;
    }
  }
  
  return spec;
}
```

## SECTION 4: Decision Priority Framework (ACCESSIBILITY-FIRST)

```
PRIORITY HIERARCHY:
┌─────────────────────────────────────┐
│ 1. Legal Compliance (MANDATORY)    │
│    - WCAG 2.1 requirements         │
│    - Section 508 standards         │
│    - Cannot be overridden          │
├─────────────────────────────────────┤
│ 2. Accessibility Excellence        │
│    - Beyond minimum compliance     │
│    - Color vision deficiency       │
│    - Motor/cognitive disabilities  │
│    - Screen reader optimization    │
├─────────────────────────────────────┤
│ 3. Inclusive Design Patterns       │
│    - Alternative encodings         │
│    - Multiple information channels │
│    - Redundant visual cues         │
│    - Clear information hierarchy   │
├─────────────────────────────────────┤
│ 4. UX Preferences (When Compatible)│
│    - Cognitive load reduction      │
│    - Visual aesthetics            │
│    - Clean design                 │
│    - ONLY if accessibility maintained│
└─────────────────────────────────────┘
```

### Implementation Rules (ACCESSIBILITY-FIRST):
- **IF** accessibility feature conflicts with UX preference → **Choose accessibility**
- **ALWAYS** provide redundant information channels (color + pattern + shape)
- **PREFER** more accessible option even if visually "busier"
- **OPTIMIZE** for screen readers and assistive technology first
- **ENHANCE** with UX improvements only after accessibility is maximized
- **NEVER** sacrifice any accessibility feature for aesthetics

### Conflict Resolution Examples:
- **UX wants**: Clean single-color line chart
- **Accessibility needs**: Color + pattern + shape encoding
- **Decision**: Use all three encodings (accessibility wins)

- **UX wants**: Minimal legend
- **Accessibility needs**: Comprehensive legend with patterns
- **Decision**: Include full accessible legend (accessibility wins)

## SECTION 5: Required Chart Elements

### Mandatory Elements (Legal Compliance)
```json
{
  "description": "Chart type of data type where key insight",
  "title": {
    "text": "Clear, descriptive title",
    "fontSize": 16,
    "anchor": "start",
    "fontWeight": "normal"
  },
  "view": {"keyboard": true},
  "mark": {
    "stroke": "white",
    "strokeWidth": 1,
    "strokeOpacity": 1
  }
}
```

### Preferred Enhancements (UX)
```json
{
  "config": {
    "view": {"stroke": null},
    "axis": {
      "domain": false,
      "ticks": false,
      "grid": false
    },
    "legend": {
      "orient": "bottom",
      "direction": "horizontal"
    }
  }
}
```

## SECTION 6: Color System (ENFORCE STRICTLY - LEGAL REQUIREMENT)

### 🚨 CRITICAL: Complete Color Vision Deficiency Protection MANDATORY 🚨

**COMPREHENSIVE CVD PROTECTION REQUIRED:**
- **RED-GREEN combinations NEVER** (affects 8% of men)
- **BLUE-YELLOW combinations NEVER** (affects 1-2% of population)  
- **BLUE-PURPLE combinations NEVER** (age-related issues)
- **MONOCHROMACY support ALWAYS** (pattern + shape alternatives required)

### Approved Palette - ONLY THESE COLORS ALLOWED
```json
{
  "color": {
    "scale": {
      "range": ["#4477AA", "#CC6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"]
    }
  }
}
```

### 🚫 ABSOLUTELY FORBIDDEN Color Combinations (ALL CVD TYPES)

**PROTANOPIA/DEUTERANOPIA (RED-GREEN BLIND - 8% of men):**
- `#CC6677` + `#228833` - FORBIDDEN
- `#EE6677` + `#228833` - FORBIDDEN  
- `#FF0000` + `#00FF00` - FORBIDDEN
- ANY red shade + ANY green shade - FORBIDDEN

**TRITANOPIA (BLUE-YELLOW BLIND - 1-2% of population):**
- `#4477AA` + `#CCBB44` - FORBIDDEN
- `#0066CC` + `#FFDD00` - FORBIDDEN
- ANY blue shade + ANY yellow shade - FORBIDDEN

**AGE-RELATED COLOR DISCRIMINATION (Growing population):**
- `#4477AA` + `#AA3377` - FORBIDDEN (blue + purple)
- `#4477AA` + `#000000` - FORBIDDEN (blue + black)
- Dark blue + Dark purple combinations - FORBIDDEN

**MONOCHROMACY (Complete color blindness - 0.01%):**
- REQUIRES: Pattern + Shape alternatives for ALL color encodings
- Color alone NEVER sufficient

### Comprehensive Color Vision Deficiency Validation (MANDATORY)
```javascript
function validateAllCVDTypes(colors) {
  // RED-GREEN VIOLATIONS (Protanopia/Deuteranopia)
  const redGreenViolations = [
    ['#CC6677', '#228833'], ['#EE6677', '#228833'], 
    ['#FF0000', '#00FF00'], ['#DD3333', '#228833'],
    ['#CC6677', '#00AA44'], ['#EE3333', '#228833'],
    ['#AA3333', '#228833'], ['#CC3333', '#44AA44']
  ];
  
  // BLUE-YELLOW VIOLATIONS (Tritanopia)
  const blueYellowViolations = [
    ['#4477AA', '#CCBB44'], ['#0066CC', '#FFDD00'],
    ['#4477AA', '#DDDD77'], ['#3366BB', '#CCBB44'],
    ['#2255AA', '#FFCC00'], ['#4477AA', '#EECC44']
  ];
  
  // AGE-RELATED VIOLATIONS
  const ageRelatedViolations = [
    ['#4477AA', '#AA3377'], ['#4477AA', '#000000'],
    ['#3366BB', '#883366'], ['#2255AA', '#772255']
  ];
  
  // Check all violation types
  const hasRedGreen = redGreenViolations.some(combo => 
    colors.includes(combo[0]) && colors.includes(combo[1])
  );
  
  const hasBlueYellow = blueYellowViolations.some(combo => 
    colors.includes(combo[0]) && colors.includes(combo[1])
  );
  
  const hasAgeRelated = ageRelatedViolations.some(combo => 
    colors.includes(combo[0]) && colors.includes(combo[1])
  );
  
  if (hasRedGreen) {
    throw new Error("CVD VIOLATION: Red-green combination detected (affects 8% of men)");
  }
  if (hasBlueYellow) {
    throw new Error("CVD VIOLATION: Blue-yellow combination detected (affects 1-2% of population)");
  }
  if (hasAgeRelated) {
    throw new Error("CVD VIOLATION: Age-related color discrimination issue detected");
  }
  
  return true;
}

// Verify Paul Tol palette safety for all CVD types
function validatePaulTolCombinations(colors) {
  const paulTolSafe = ["#4477AA", "#CC6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"];
  
  // Only allow Paul Tol colors
  const hasUnsafeColors = colors.some(color => !paulTolSafe.includes(color));
  if (hasUnsafeColors) {
    throw new Error("FORBIDDEN: Use only approved Paul Tol palette colors");
  }
  
  // Even within Paul Tol, some combinations are problematic
  validateAllCVDTypes(colors);
  
  return true;
}

// MANDATORY: Check monochromacy support
function requireMonochromacySupport(spec) {
  const hasColorEncoding = !!spec.encoding?.color;
  const hasPatternEncoding = !!spec.encoding?.strokeDash;
  const hasShapeEncoding = !!spec.encoding?.shape;
  
  if (hasColorEncoding && !hasPatternEncoding && !hasShapeEncoding) {
    throw new Error("MONOCHROMACY VIOLATION: Color encoding requires pattern OR shape alternative");
  }
  
  return true;
}

// MUST RUN before any chart generation
function enforceComprehensiveCVDSafety(spec) {
  const colors = spec.encoding?.color?.scale?.range || [];
  
  // Validate all CVD types
  validatePaulTolCombinations(colors);
  
  // Ensure monochromacy support
  requireMonochromacySupport(spec);
  
  return spec;
}
```

### Paul Tol Palette CVD Safety Analysis

**SAFE WITHIN PAUL TOL PALETTE:**
- `#4477AA` (blue) + `#66CCEE` (cyan) ✅ Safe
- `#CC6677` (pink) + `#AA3377` (purple) ✅ Safe  
- `#228833` (green) + `#66CCEE` (cyan) ✅ Safe
- `#BBBBBB` (gray) + ANY color ✅ Safe

**PROBLEMATIC WITHIN PAUL TOL:**
- `#4477AA` + `#CCBB44` ❌ Blue-Yellow (tritanopia)
- `#4477AA` + `#AA3377` ❌ Blue-Purple (age-related)
- `#CC6677` + `#228833` ❌ Pink-Green (red-green blind)

### Safe Paul Tol Combinations (Pre-validated)
```json
{
  "safe_3_color": ["#4477AA", "#CC6677", "#66CCEE"],
  "safe_4_color": ["#4477AA", "#CC6677", "#66CCEE", "#BBBBBB"],
  "safe_5_color": ["#4477AA", "#CC6677", "#66CCEE", "#AA3377", "#BBBBBB"]
}
```

### Alternative Encodings for ALL Categories (MANDATORY FOR MONOCHROMACY)
```json
{
  "encoding": {
    "color": {
      "field": "category",
      "scale": {"range": ["#4477AA", "#CC6677", "#66CCEE"]},
      "legend": {"title": "Category"}
    },
    "strokeDash": {
      "field": "category", 
      "scale": {"range": [[1,0], [8,4], [4,4]]},
      "legend": null
    },
    "shape": {
      "field": "category",
      "scale": {"range": ["circle", "square", "triangle-up"]},
      "legend": null
    }
  }
}
```

## SECTION 7: Chart Type Selection Matrix

### Data Relationship → Chart Type Mapping

**Temporal Analysis (Change Over Time)**
- **Use**: Line charts, area charts
- **Pattern**: Temporal x-axis with time series data
- **Template**: `time-series.json`
- **Examples**: Air mission trends, casualty rates over time

**Ranking Comparisons (Ordered position)**  
- **Use**: Horizontal bar charts (preferred over vertical)
- **Pattern**: Ordered categorical data
- **Template**: `horizontal-bar.json`  
- **Examples**: Top 10 countries by casualties, equipment by effectiveness

**Correlation Analysis (Relationships between variables)**
- **Use**: Scatterplots with accessible shapes
- **Pattern**: Two quantitative variables
- **CVD Requirements**: Multiple shapes + colors
- **Examples**: Cost vs. effectiveness, casualties vs. duration

**Part-to-Whole (Component breakdown)**
- **Use**: Stacked bar charts (NEVER pie charts)
- **Pattern**: Categories summing to total
- **Max Categories**: 5 for accessibility
- **Examples**: Budget allocation, force composition

**Multi-Series Comparison (4+ data series)**
- **Use**: Small multiples (preferred)
- **Pattern**: Same chart type repeated across categories
- **Template**: `small-multiples.json`
- **Examples**: Mission patterns by military branch

**Magnitude Comparison (Size differences)**
- **Use**: Column charts, horizontal bars
- **Pattern**: Comparing absolute values
- **Examples**: Equipment quantities, personnel numbers

### Chart Selection Decision Tree

```
What is the primary data relationship?
├── Temporal component exists?
│   ├── YES → Use time-series template
│   └── NO → Continue to next decision
├── Ranking/ordering most important?
│   ├── YES → Use horizontal-bar template  
│   └── NO → Continue to next decision
├── 4+ data series or categories?
│   ├── YES → Use small-multiples template
│   └── NO → Continue to next decision
├── Part-to-whole relationship?
│   ├── YES → Use stacked bar (max 5 categories)
│   └── NO → Use horizontal-bar template (default)
```

### Implementation Standards for All Chart Types

**Required Elements (ALL Charts)**:
```json
{
  "title": {"text": "Insight-focused title", "fontSize": 16},
  "description": "Amy Cesal formula alt text",
  "mark": {"stroke": "white", "strokeWidth": 1},
  "config": {"view": {"keyboard": true}}
}
```

**Forbidden Chart Types (Accessibility Violations)**:
- Pie charts (difficult for screen readers)
- Donut charts (cognitive load issues)
- Violin plots (pattern recognition problems)
- 3D charts (depth perception barriers)

## SECTION 8: Visual Creation Workflow

### Step-by-Step Process for New Visualizations

1. **Reference Visual Knowledge Base FIRST**
   - Check `/visuals/` directory examples in `visual-knowledge-base.md`
   - Find similar data patterns or chart types
   - Identify proven accessibility techniques to adapt

2. **Assess Data and Requirements**
   - Understand data structure and relationships
   - Identify primary insight to communicate
   - Determine cognitive load requirements

3. **Select Pattern or Template**
   - Use knowledge base example as starting point
   - Fall back to templates if no similar example exists
   - Adapt proven accessibility patterns

4. **Apply Comprehensive Accessibility**
   - Implement CVD-safe colors from examples
   - Add alternative encodings (patterns/shapes)
   - Include proper alt text and keyboard navigation

5. **Validate and Test**
   - Run through all accessibility validation functions
   - Check against forbidden patterns
   - Ensure compliance with legal requirements

**PRIORITY ORDER**:
1. Visual knowledge base examples (preferred)
2. Existing templates (fallback)
3. Error handling guide (for conflicts)
4. Custom solutions (last resort)