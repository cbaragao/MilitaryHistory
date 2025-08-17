-- PSYOPSA Periodic Set 1: Psychological Operations Activities
-- Leaflet distribution, loudspeaker operations, and publication activities

SELECT
    -- Primary and foreign keys
    TRIM(p.USID) AS usid,
    TRIM(p.PCN) AS pcn,
    
    -- Date and reporting information
    TRIM(p.DATE1) AS report_date,
    TRIM(p.CONAG) AS conducting_agency_code,
    COALESCE(conag_lookup.description, TRIM(p.CONAG)) AS conducting_agency_description,
    TRIM(p.REPORT) AS reporting_unit_code,
    COALESCE(report_lookup.description, TRIM(p.REPORT)) AS reporting_unit_description,
    
    -- Operation classification
    TRIM(p.OP) AS operation_code,
    COALESCE(op_lookup.description, TRIM(p.OP)) AS operation_description,
    TRIM(p.CAMPN) AS campaign_code,
    COALESCE(campn_lookup.description, TRIM(p.CAMPN)) AS campaign_description,
    
    -- Message themes
    TRIM(p.THEM) AS theme_code,
    COALESCE(them_lookup.description, TRIM(p.THEM)) AS theme_description,
    TRIM(p.STHEM) AS subtheme_code,
    COALESCE(sthem_lookup.description, TRIM(p.STHEM)) AS subtheme_description,
    
    -- System field
    p.VSZ1 AS vsz1,
    
    -- Distribution activities
    p.LEAFLET AS leaflets_distributed,
    p.SPRHRS AS loudspeaker_hours,
    p.POSTERS AS posters_handbills,
    p.PUBLS AS other_publications,
    
    -- Activity counts (meanings TBD from LOOKUP_TABLES.pdf)
    p.APT AS apt_activities,
    p.CAP AS cap_activities,
    p.CDT AS cdt_activities,
    p.CVC AS cvc_activities,
    p.HB AS hb_activities,
    p.HE AS he_activities,
    p.MDC AS mdc_activities,
    p.RDC AS rdc_activities,
    p.SLT AS slt_activities,
    p.VIS AS vis_activities,
    
    -- Target audience
    TRIM(p.AUD) AS audience_code,
    COALESCE(aud_lookup.description, TRIM(p.AUD)) AS audience_description

FROM psyopsa_ps1_nara p
LEFT JOIN psyopsa_lookup_conag AS conag_lookup ON 
    UPPER(TRIM(p.CONAG)) = UPPER(conag_lookup.code) AND p.CONAG IS NOT NULL AND p.CONAG != 'nan' AND p.CONAG != ''
LEFT JOIN psyopsa_lookup_report AS report_lookup ON 
    UPPER(TRIM(p.REPORT)) = UPPER(report_lookup.code) AND p.REPORT IS NOT NULL AND p.REPORT != 'nan' AND p.REPORT != ''
LEFT JOIN psyopsa_lookup_op AS op_lookup ON 
    UPPER(TRIM(p.OP)) = UPPER(op_lookup.code) AND p.OP IS NOT NULL AND p.OP != 'nan' AND p.OP != ''
LEFT JOIN psyopsa_lookup_campn AS campn_lookup ON 
    UPPER(TRIM(p.CAMPN)) = UPPER(campn_lookup.code) AND p.CAMPN IS NOT NULL AND p.CAMPN != 'nan' AND p.CAMPN != ''
LEFT JOIN psyopsa_lookup_them AS them_lookup ON 
    UPPER(TRIM(p.THEM)) = UPPER(them_lookup.code) AND p.THEM IS NOT NULL AND p.THEM != 'nan' AND p.THEM != ''
LEFT JOIN psyopsa_lookup_sthem AS sthem_lookup ON 
    UPPER(TRIM(p.STHEM)) = UPPER(sthem_lookup.code) AND p.STHEM IS NOT NULL AND p.STHEM != 'nan' AND p.STHEM != ''
LEFT JOIN psyopsa_lookup_aud AS aud_lookup ON 
    UPPER(TRIM(p.AUD)) = UPPER(aud_lookup.code) AND p.AUD IS NOT NULL AND p.AUD != 'nan' AND p.AUD != ''

WHERE p.USID IS NOT NULL 
    AND TRIM(p.USID) != '' 
    AND TRIM(p.USID) != 'nan'
ORDER BY TRIM(p.USID), TRIM(p.PCN)