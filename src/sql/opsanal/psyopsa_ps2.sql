-- PSYOPSA Periodic Set 2: Radio and Television Programming Activities
-- Broadcast hours and programming content tracking

SELECT
    -- Primary and foreign keys
    TRIM(p.USID) AS usid,
    TRIM(p.PCN) AS pcn,
    
    -- Date and reporting information
    TRIM(p.DATE2) AS report_date,
    TRIM(p.REPUNIT) AS reporting_unit_code,
    COALESCE(repunit_lookup.description, TRIM(p.REPUNIT)) AS reporting_unit_description,
    
    -- System field
    p.VSZ2 AS vsz2,
    
    -- Radio programming (minutes or programs)
    p.RNEWS AS radio_news,
    p.RENT AS radio_entertainment,
    p.RIP AS radio_information_propaganda,
    
    -- Television programming (minutes or programs)
    p.TVNEWS AS tv_news,
    p.TVENT AS tv_entertainment,
    p.TVIP AS tv_information_propaganda

FROM psyopsa_ps2_nara p
LEFT JOIN psyopsa_lookup_repunit AS repunit_lookup ON 
    UPPER(TRIM(p.REPUNIT)) = UPPER(repunit_lookup.code) AND p.REPUNIT IS NOT NULL AND p.REPUNIT != 'nan' AND p.REPUNIT != ''

WHERE p.USID IS NOT NULL 
    AND TRIM(p.USID) != '' 
    AND TRIM(p.USID) != 'nan'
ORDER BY TRIM(p.USID), TRIM(p.PCN)