-- VSSG (Vietnam Special Studies Group) Data Processing
-- Hamlet evaluation data from July 1969 to January 1974
-- Source: https://catalog.archives.gov/id/4658149

SELECT
    -- Date fields with standardization
    CASE 
        WHEN length(CAST(v.DATE AS VARCHAR)) = 6 THEN 
            concat('19', left(CAST(v.DATE AS VARCHAR), 2), '-', substring(CAST(v.DATE AS VARCHAR), 3, 2), '-', right(CAST(v.DATE AS VARCHAR), 2))
        WHEN length(CAST(v.DATE AS VARCHAR)) = 4 THEN
            concat('19', left(CAST(v.DATE AS VARCHAR), 2), '-', right(CAST(v.DATE AS VARCHAR), 2), '-01')
        ELSE CAST(v.DATE AS VARCHAR)
    END AS assessment_date,
    
    -- Unit and location identifiers
    replace(CAST(v.USID AS VARCHAR), 'nan', '') AS unit_id,
    replace(CAST(v."+PCN" AS VARCHAR), 'nan', '') AS province_code,
    replace(CAST(v."+SC0" AS VARCHAR), 'nan', '') AS district_code,
    
    -- Village and hamlet characteristics
    TRY_CAST(replace(CAST(v.VSZ AS VARCHAR), 'nan', '') AS INT) AS village_size_code,
    vsz.value AS village_size_description,
    TRY_CAST(replace(CAST(v.HPOP AS VARCHAR), 'nan', '') AS INT) AS hamlet_population,
    
    -- Security assessments
    TRY_CAST(replace(CAST(v.HMB1 AS VARCHAR), 'nan', '') AS INT) AS hamlet_security_night,
    hmb1.value AS hamlet_security_night_description,
    TRY_CAST(replace(CAST(v.HMB4 AS VARCHAR), 'nan', '') AS INT) AS hamlet_security_day,
    hmb4.value AS hamlet_security_day_description,
    
    -- Quality assessments
    TRY_CAST(replace(CAST(v.HQC2 AS VARCHAR), 'nan', '') AS INT) AS hamlet_quality_2,
    hqc2.value AS hamlet_quality_2_description,
    TRY_CAST(replace(CAST(v.HQC3 AS VARCHAR), 'nan', '') AS INT) AS hamlet_quality_3,
    hqc3.value AS hamlet_quality_3_description,
    TRY_CAST(replace(CAST(v.HQC4 AS VARCHAR), 'nan', '') AS INT) AS hamlet_quality_4,
    hqc4.value AS hamlet_quality_4_description,
    TRY_CAST(replace(CAST(v.HQC5 AS VARCHAR), 'nan', '') AS INT) AS hamlet_quality_5,
    hqc5.value AS hamlet_quality_5_description,
    
    -- Additional quality indicators
    TRY_CAST(replace(CAST(v.HQE2 AS VARCHAR), 'nan', '') AS INT) AS hamlet_quality_e2,
    TRY_CAST(replace(CAST(v.HQZ1 AS VARCHAR), 'nan', '') AS INT) AS hamlet_quality_z1,
    
    -- Village assessments
    TRY_CAST(replace(CAST(v.VMB1 AS VARCHAR), 'nan', '') AS INT) AS village_military_activity,
    vma.value AS village_military_activity_description,
    TRY_CAST(replace(CAST(v.VQE2 AS VARCHAR), 'nan', '') AS INT) AS village_quality_e2,
    
    -- Overall assessment
    TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', NULL) AS FLOAT) AS overall_score,
    CASE 
        WHEN TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', '0') AS FLOAT) >= 90 THEN 'EXCELLENT'
        WHEN TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', '0') AS FLOAT) >= 80 THEN 'VERY GOOD'
        WHEN TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', '0') AS FLOAT) >= 70 THEN 'GOOD'
        WHEN TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', '0') AS FLOAT) >= 60 THEN 'SATISFACTORY'
        WHEN TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', '0') AS FLOAT) >= 50 THEN 'MARGINAL'
        WHEN TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', '0') AS FLOAT) >= 40 THEN 'POOR'
        WHEN TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', '0') AS FLOAT) >= 30 THEN 'VERY POOR'
        WHEN TRY_CAST(replace(CAST(v.SCORE AS VARCHAR), 'nan', '0') AS FLOAT) > 0 THEN 'CRITICAL'
        ELSE 'UNKNOWN'
    END AS score_category,
    
    -- Additional fields
    replace(CAST(v.XTRA AS VARCHAR), 'nan', '') AS extra_data

FROM vssg_nara v

-- Join with lookup tables for security codes
LEFT JOIN vssg_hamlet_security_codes hmb1 
    ON CAST(replace(CAST(v.HMB1 AS VARCHAR), 'nan', '') AS VARCHAR) = hmb1.code
    
LEFT JOIN vssg_hamlet_security_codes hmb4 
    ON CAST(replace(CAST(v.HMB4 AS VARCHAR), 'nan', '') AS VARCHAR) = hmb4.code

-- Join with lookup tables for quality codes  
LEFT JOIN vssg_hamlet_quality_codes hqc2 
    ON CAST(replace(CAST(v.HQC2 AS VARCHAR), 'nan', '') AS VARCHAR) = hqc2.code
    
LEFT JOIN vssg_hamlet_quality_codes hqc3 
    ON CAST(replace(CAST(v.HQC3 AS VARCHAR), 'nan', '') AS VARCHAR) = hqc3.code
    
LEFT JOIN vssg_hamlet_quality_codes hqc4 
    ON CAST(replace(CAST(v.HQC4 AS VARCHAR), 'nan', '') AS VARCHAR) = hqc4.code
    
LEFT JOIN vssg_hamlet_quality_codes hqc5 
    ON CAST(replace(CAST(v.HQC5 AS VARCHAR), 'nan', '') AS VARCHAR) = hqc5.code

-- Join with village size codes
LEFT JOIN vssg_village_size_codes vsz 
    ON CAST(replace(CAST(v.VSZ AS VARCHAR), 'nan', '') AS VARCHAR) = vsz.code

-- Join with village military activity codes
LEFT JOIN vssg_village_military_activity_codes vma 
    ON CAST(replace(CAST(v.VMB1 AS VARCHAR), 'nan', '') AS VARCHAR) = vma.code

-- Filter out completely empty records
WHERE v.DATE IS NOT NULL 
   OR v.USID IS NOT NULL 
   OR v.HPOP IS NOT NULL

-- Order by date and unit
ORDER BY 
    assessment_date ASC,
    unit_id ASC,
    province_code ASC;
