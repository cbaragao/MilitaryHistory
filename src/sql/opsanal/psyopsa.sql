-- PSYOPSA Fixed Set: Psychological Operation System Files (1970-1973)
-- District-level baseline information including population, security scores, and enemy strength

SELECT
    -- Primary identifiers
    TRIM(USID) AS usid,
    TRIM(PCN) AS pcn,
    TRIM(SC0) AS sc0,
    VSZ AS vsz,
    
    -- Population data
    POP AS district_population,
    GVNPOP AS gvn_controlled_population,
    HOICHN AS hoi_chanh_received,
    REF AS refugee_population,
    
    -- Enemy force estimates
    NVA AS nva_personnel,
    VCHAM AS vc_hamlet_guerrillas,
    VCI AS vc_infrastructure,
    
    -- Security and development scores (0-100 scale typical)
    SAS AS security_average_score,
    DAS AS development_average_score,
    PAS AS political_average_score,
    
    -- Communication infrastructure
    NUMRAD AS number_of_radios,
    NUMTV AS number_of_tvs

FROM psyopsa_nara
WHERE USID IS NOT NULL 
    AND TRIM(USID) != '' 
    AND TRIM(USID) != 'nan'
ORDER BY TRIM(USID)