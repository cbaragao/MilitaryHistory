-- AIMS Gulf War Era (1990-1994): Gulf War and Early 1990s Operations
-- Awards Information Management System Data Processing
-- Data has already been parsed into columns by nara.py using schema field positions
-- Time period: 1990-1994 (Gulf War, Desert Storm, Desert Shield, peacekeeping operations)

-- Return processed data with cleaned data and date conversions
-- Note: aims_nara table already has columns parsed from fixed-width format
SELECT
    -- Basic record identifiers (already parsed)
    INDV_UNIT AS indv_unit,
    PRIM_TYPE AS prim_type,
    "FOREIGN" AS foreign,
    COUNTRY AS country,
    CAMPAIGN AS campaign,
    COALESCE(camp_lookup.description, CAMPAIGN) AS campaign_description,
    
    -- Date fields - Convert from parsed ___MMDDYYYY format to proper dates
    CASE 
        WHEN SECBD_MTG IS NOT NULL AND LENGTH(TRIM(SECBD_MTG)) >= 8 AND TRIM(SECBD_MTG) != ''
        THEN 
            CASE 
                WHEN SUBSTR(TRIM(SECBD_MTG), -4) BETWEEN '1990' AND '1994'
                    AND LENGTH(TRIM(SECBD_MTG)) = 8
                    AND SUBSTR(TRIM(SECBD_MTG), 1, 2) BETWEEN '01' AND '12'
                    AND SUBSTR(TRIM(SECBD_MTG), 3, 2) BETWEEN '01' AND '31'
                THEN SUBSTR(TRIM(SECBD_MTG), -4) || '-' ||
                     SUBSTR(TRIM(SECBD_MTG), 1, 2) || '-' ||
                     SUBSTR(TRIM(SECBD_MTG), 3, 2)
                ELSE NULL
            END
        ELSE NULL
    END AS secbd_mtg,
    
    DUP AS dup,
    
    -- Personnel fields (already correctly parsed)
    SSN AS ssn,
    LNAME AS lname,
    FNAME AS fname,
    MNAME AS mname,
    SUFFIX AS suffix,
    
    -- Military service details (already parsed)
    COMPONENT AS component,
    OFF_ENL AS off_enl,
    GRADE_RATING AS grade_rating,
    COALESCE(grd_lookup.description, GRADE_RATING) AS grade_rating_description,
    PAY_GRADE AS pay_grade,
    DESIG_NEC_MOS AS desig_nec_mos,
    CORPS_MEM AS corps_mem,
    COALESCE(corp_lookup.description, CORPS_MEM) AS corps_mem_description,
    BUIC_RUC AS buic_ruc,
    
    -- Award information (already parsed)
    RECMD_AWD AS recmd_awd,
    COALESCE(awd_lookup_recmd.description, RECMD_AWD) AS recmd_awd_description,
    BILLET AS billet,
    ACTION_TYPE AS action_type,
    APPR_AWD_NUM AS appr_awd_num,
    
    -- Merit period dates with conversion
    CASE 
        WHEN MERIT_START IS NOT NULL AND LENGTH(TRIM(MERIT_START)) >= 8 AND TRIM(MERIT_START) != ''
        THEN 
            CASE 
                WHEN SUBSTR(TRIM(MERIT_START), -4) BETWEEN '1990' AND '1994'
                    AND LENGTH(TRIM(MERIT_START)) = 8
                    AND SUBSTR(TRIM(MERIT_START), 1, 2) BETWEEN '01' AND '12'
                    AND SUBSTR(TRIM(MERIT_START), 3, 2) BETWEEN '01' AND '31'
                THEN SUBSTR(TRIM(MERIT_START), -4) || '-' ||
                     SUBSTR(TRIM(MERIT_START), 1, 2) || '-' ||
                     SUBSTR(TRIM(MERIT_START), 3, 2)
                ELSE NULL
            END
        ELSE NULL
    END AS merit_start,
    
    CASE 
        WHEN MERIT_END IS NOT NULL AND LENGTH(TRIM(MERIT_END)) >= 8 AND TRIM(MERIT_END) != ''
        THEN 
            CASE 
                WHEN SUBSTR(TRIM(MERIT_END), -4) BETWEEN '1990' AND '1994'
                    AND LENGTH(TRIM(MERIT_END)) = 8
                    AND SUBSTR(TRIM(MERIT_END), 1, 2) BETWEEN '01' AND '12'
                    AND SUBSTR(TRIM(MERIT_END), 3, 2) BETWEEN '01' AND '31'
                THEN SUBSTR(TRIM(MERIT_END), -4) || '-' ||
                     SUBSTR(TRIM(MERIT_END), 1, 2) || '-' ||
                     SUBSTR(TRIM(MERIT_END), 3, 2)
                ELSE NULL
            END
        ELSE NULL
    END AS merit_end,
    
    MERIT_MOS AS merit_mos,
    SHOW_MERIT_DATE AS show_merit_date,
    ACTION_AREA AS action_area,
    COALESCE(act_lookup.description, ACTION_AREA) AS action_area_description,
    
    -- More date fields with conversion
    CASE 
        WHEN ORIG_RECMD_DATE IS NOT NULL AND LENGTH(TRIM(ORIG_RECMD_DATE)) >= 8 AND TRIM(ORIG_RECMD_DATE) != ''
        THEN 
            CASE 
                WHEN SUBSTR(TRIM(ORIG_RECMD_DATE), -4) BETWEEN '1990' AND '1994'
                    AND LENGTH(TRIM(ORIG_RECMD_DATE)) = 8
                    AND SUBSTR(TRIM(ORIG_RECMD_DATE), 1, 2) BETWEEN '01' AND '12'
                    AND SUBSTR(TRIM(ORIG_RECMD_DATE), 3, 2) BETWEEN '01' AND '31'
                THEN SUBSTR(TRIM(ORIG_RECMD_DATE), -4) || '-' ||
                     SUBSTR(TRIM(ORIG_RECMD_DATE), 1, 2) || '-' ||
                     SUBSTR(TRIM(ORIG_RECMD_DATE), 3, 2)
                ELSE NULL
            END
        ELSE NULL
    END AS orig_recmd_date,
    
    SEC_ENDRSR_RECMD AS sec_endrsr_recmd,
    COALESCE(awd_lookup_sec.description, SEC_ENDRSR_RECMD) AS sec_endrsr_recmd_description,
    
    CASE 
        WHEN ENDRSMT_DATE IS NOT NULL AND LENGTH(TRIM(ENDRSMT_DATE)) >= 8 AND TRIM(ENDRSMT_DATE) != ''
        THEN 
            CASE 
                WHEN SUBSTR(TRIM(ENDRSMT_DATE), -4) BETWEEN '1990' AND '1994'
                    AND LENGTH(TRIM(ENDRSMT_DATE)) = 8
                    AND SUBSTR(TRIM(ENDRSMT_DATE), 1, 2) BETWEEN '01' AND '12'
                    AND SUBSTR(TRIM(ENDRSMT_DATE), 3, 2) BETWEEN '01' AND '31'
                THEN SUBSTR(TRIM(ENDRSMT_DATE), -4) || '-' ||
                     SUBSTR(TRIM(ENDRSMT_DATE), 1, 2) || '-' ||
                     SUBSTR(TRIM(ENDRSMT_DATE), 3, 2)
                ELSE NULL
            END
        ELSE NULL
    END AS endrsmt_date,
    
    -- Final award details
    APPR_AWD AS appr_awd,
    COALESCE(awd_lookup_appr.description, APPR_AWD) AS appr_awd_description,
    AWD_AUTH AS awd_auth,
    COALESCE(auth_lookup.description, AWD_AUTH) AS awd_auth_description,
    
    CASE 
        WHEN APPR_AWD_DATE IS NOT NULL AND LENGTH(TRIM(APPR_AWD_DATE)) >= 8 AND TRIM(APPR_AWD_DATE) != ''
        THEN 
            CASE 
                WHEN SUBSTR(TRIM(APPR_AWD_DATE), -4) BETWEEN '1990' AND '1994'
                    AND LENGTH(TRIM(APPR_AWD_DATE)) = 8
                    AND SUBSTR(TRIM(APPR_AWD_DATE), 1, 2) BETWEEN '01' AND '12'
                    AND SUBSTR(TRIM(APPR_AWD_DATE), 3, 2) BETWEEN '01' AND '31'
                THEN SUBSTR(TRIM(APPR_AWD_DATE), -4) || '-' ||
                     SUBSTR(TRIM(APPR_AWD_DATE), 1, 2) || '-' ||
                     SUBSTR(TRIM(APPR_AWD_DATE), 3, 2)
                ELSE NULL
            END
        ELSE NULL
    END AS appr_awd_date,
    
    -- Administrative fields
    SEC_SER_NUM AS sec_ser_num,
    SECBD_RECMD_AWD AS secbd_recmd_awd,
    COALESCE(awd_lookup_secbd.description, SECBD_RECMD_AWD) AS secbd_recmd_awd_description,
    SECBD_EH AS secbd_eh,
    APPR_EH AS appr_eh,
    AWD_MUL_DATE AS awd_mul_date,
    TOTAL_MUL_DATE AS total_mul_date,
    SHIP AS ship,
    CNO_SER_NUM AS cno_ser_num,
    
    CASE 
        WHEN MAIL_DATE IS NOT NULL AND LENGTH(TRIM(MAIL_DATE)) >= 8 AND TRIM(MAIL_DATE) != ''
        THEN 
            CASE 
                WHEN SUBSTR(TRIM(MAIL_DATE), -4) BETWEEN '1990' AND '1994'
                    AND LENGTH(TRIM(MAIL_DATE)) = 8
                    AND SUBSTR(TRIM(MAIL_DATE), 1, 2) BETWEEN '01' AND '12'
                    AND SUBSTR(TRIM(MAIL_DATE), 3, 2) BETWEEN '01' AND '31'
                THEN SUBSTR(TRIM(MAIL_DATE), -4) || '-' ||
                     SUBSTR(TRIM(MAIL_DATE), 1, 2) || '-' ||
                     SUBSTR(TRIM(MAIL_DATE), 3, 2)
                ELSE NULL
            END
        ELSE NULL
    END AS mail_date,
    
    MAILED_TO AS mailed_to,
    AWD_REMARKS AS awd_remarks,
    PCMD_ID AS pcmd_id,
    MUL_ID AS mul_id,
    
    -- Administrative dates
    CASE 
        WHEN CMC_TO_MHM IS NOT NULL AND LENGTH(TRIM(CMC_TO_MHM)) >= 8 AND TRIM(CMC_TO_MHM) != ''
        THEN 
            CASE 
                WHEN SUBSTR(TRIM(CMC_TO_MHM), -4) BETWEEN '1990' AND '1994'
                    AND LENGTH(TRIM(CMC_TO_MHM)) = 8
                    AND SUBSTR(TRIM(CMC_TO_MHM), 1, 2) BETWEEN '01' AND '12'
                    AND SUBSTR(TRIM(CMC_TO_MHM), 3, 2) BETWEEN '01' AND '31'
                THEN SUBSTR(TRIM(CMC_TO_MHM), -4) || '-' ||
                     SUBSTR(TRIM(CMC_TO_MHM), 1, 2) || '-' ||
                     SUBSTR(TRIM(CMC_TO_MHM), 3, 2)
                ELSE NULL
            END
        ELSE NULL
    END AS cmc_to_mhm,
    
    -- Entry and change dates (keep as-is - they're in a different format)
    ENTRY_DATE AS entry_date,
    CHANGE_DATE AS change_date

FROM aims_nara
LEFT JOIN aims_lookup_camp AS camp_lookup ON 
    UPPER(TRIM(CAMPAIGN)) = UPPER(camp_lookup.code) AND CAMPAIGN IS NOT NULL AND CAMPAIGN != 'nan' AND CAMPAIGN != ''
LEFT JOIN aims_lookup_grd AS grd_lookup ON 
    UPPER(TRIM(GRADE_RATING)) = UPPER(grd_lookup.code) AND GRADE_RATING IS NOT NULL AND GRADE_RATING != 'nan' AND GRADE_RATING != ''
LEFT JOIN aims_lookup_corp AS corp_lookup ON 
    UPPER(TRIM(CORPS_MEM)) = UPPER(corp_lookup.code) AND CORPS_MEM IS NOT NULL AND CORPS_MEM != 'nan' AND CORPS_MEM != ''
LEFT JOIN aims_lookup_act AS act_lookup ON 
    UPPER(TRIM(ACTION_AREA)) = UPPER(act_lookup.code) AND ACTION_AREA IS NOT NULL AND ACTION_AREA != 'nan' AND ACTION_AREA != ''
LEFT JOIN aims_lookup_awd AS awd_lookup_recmd ON 
    UPPER(TRIM(RECMD_AWD)) = UPPER(awd_lookup_recmd.code) AND RECMD_AWD IS NOT NULL AND RECMD_AWD != 'nan' AND RECMD_AWD != ''
LEFT JOIN aims_lookup_awd AS awd_lookup_sec ON 
    UPPER(TRIM(SEC_ENDRSR_RECMD)) = UPPER(awd_lookup_sec.code) AND SEC_ENDRSR_RECMD IS NOT NULL AND SEC_ENDRSR_RECMD != 'nan' AND SEC_ENDRSR_RECMD != ''
LEFT JOIN aims_lookup_awd AS awd_lookup_appr ON 
    UPPER(TRIM(APPR_AWD)) = UPPER(awd_lookup_appr.code) AND APPR_AWD IS NOT NULL AND APPR_AWD != 'nan' AND APPR_AWD != ''
LEFT JOIN aims_lookup_auth AS auth_lookup ON 
    UPPER(TRIM(AWD_AUTH)) = UPPER(auth_lookup.code) AND AWD_AUTH IS NOT NULL AND AWD_AUTH != 'nan' AND AWD_AUTH != ''
LEFT JOIN aims_lookup_awd AS awd_lookup_secbd ON 
    UPPER(TRIM(SECBD_RECMD_AWD)) = UPPER(awd_lookup_secbd.code) AND SECBD_RECMD_AWD IS NOT NULL AND SECBD_RECMD_AWD != 'nan' AND SECBD_RECMD_AWD != ''
WHERE INDV_UNIT IS NOT NULL  -- Filter out potential null records
    AND APPR_AWD_DATE IS NOT NULL AND APPR_AWD_DATE != 'nan' AND APPR_AWD_DATE != ''
    AND CAST(SUBSTR(TRIM(APPR_AWD_DATE), -4) AS INTEGER) BETWEEN 1990 AND 1994
;