SELECT
    a.SERPX,
    a.SERNO,
    TRY_CAST(replace(CAST(a.SEQNO AS VARCHAR), 'nan', '') AS INTEGER) AS SEQNO,
    replace(CAST(a.NAME AS VARCHAR), 'nan', '') AS NAME,
    replace(CAST(a.GRDCD AS VARCHAR), 'nan', '') AS GRDCD,
    replace(CAST(a.CMD AS VARCHAR), 'nan', '') AS CMD,
    cmd.value AS CMD_NAME,
    replace(CAST(a.CMDNM AS VARCHAR), 'nan', '') AS CMDNM,
    replace(CAST(a.SVC AS VARCHAR), 'nan', '') AS SVC,
    svc.value AS SVC_NAME,
    replace(CAST(a.SVCNM AS VARCHAR), 'nan', '') AS SVCNM,
    CASE 
        WHEN length(replace(CAST(a.DEROS AS VARCHAR), 'nan', '')) = 5 
        THEN concat('19', left(replace(CAST(a.DEROS AS VARCHAR), 'nan', ''), 2), '-', 
                   substring(replace(CAST(a.DEROS AS VARCHAR), 'nan', ''), 3, 2), '-',
                   right(replace(CAST(a.DEROS AS VARCHAR), 'nan', ''), 2))
        ELSE replace(CAST(a.DEROS AS VARCHAR), 'nan', '')
    END AS DEROS,
    replace(CAST(a.AWDRC AS VARCHAR), 'nan', '') AS AWDRC,
    awd_rec.value AS AWDRC_NAME,
    CASE 
        WHEN length(replace(CAST(a.DTDRC AS VARCHAR), 'nan', '')) = 5 
        THEN concat('19', left(replace(CAST(a.DTDRC AS VARCHAR), 'nan', ''), 2), '-', 
                   substring(replace(CAST(a.DTDRC AS VARCHAR), 'nan', ''), 3, 2), '-',
                   right(replace(CAST(a.DTDRC AS VARCHAR), 'nan', ''), 2))
        ELSE replace(CAST(a.DTDRC AS VARCHAR), 'nan', '')
    END AS DTDRC,
    replace(CAST(a.DTDAC AS VARCHAR), 'nan', '') AS DTDAC,
    replace(CAST(a.AWDPV AS VARCHAR), 'nan', '') AS AWDPV,
    awd_app.value AS AWDPV_NAME,
    replace(CAST(a.CLUS AS VARCHAR), 'nan', '') AS CLUS,
    replace(CAST(a.BRDNO AS VARCHAR), 'nan', '') AS BRDNO,
    replace(CAST(a.MACRC AS VARCHAR), 'nan', '') AS MACRC,
    awd_mac.value AS MACRC_NAME,
    replace(CAST(a.LEASS AS VARCHAR), 'nan', '') AS LEASS,
    replace(CAST(a.GONO AS VARCHAR), 'nan', '') AS GONO,
    CASE 
        WHEN length(replace(CAST(a.DTDFW AS VARCHAR), 'nan', '')) = 5 
        THEN concat('19', left(replace(CAST(a.DTDFW AS VARCHAR), 'nan', ''), 2), '-', 
                   substring(replace(CAST(a.DTDFW AS VARCHAR), 'nan', ''), 3, 2), '-',
                   right(replace(CAST(a.DTDFW AS VARCHAR), 'nan', ''), 2))
        ELSE replace(CAST(a.DTDFW AS VARCHAR), 'nan', '')
    END AS DTDFW,
    replace(CAST(a.PVN AS VARCHAR), 'nan', '') AS PVN,
    replace(CAST(a.POSTHU AS VARCHAR), 'nan', '') AS POSTHU,
    replace(CAST(a.SPAR1 AS VARCHAR), 'nan', '') AS SPAR1,
    TRY_CAST(replace(CAST(a.SPAR2 AS VARCHAR), 'nan', '') AS INTEGER) AS SPAR2,
    TRY_CAST(replace(CAST(a.SPAR3 AS VARCHAR), 'nan', '') AS INTEGER) AS SPAR3,
    replace(CAST(a.SPAR4 AS VARCHAR), 'nan', '') AS SPAR4,
    replace(CAST(a.SPAR5 AS VARCHAR), 'nan', '') AS SPAR5,
    replace(CAST(a.SPAR6 AS VARCHAR), 'nan', '') AS SPAR6,
    TRY_CAST(replace(CAST(a.SPAR7 AS VARCHAR), 'nan', '') AS INTEGER) AS SPAR7,
    TRY_CAST(replace(CAST(a.SPAR8 AS VARCHAR), 'nan', '') AS INTEGER) AS SPAR8,
    replace(CAST(a.SPAR9 AS VARCHAR), 'nan', '') AS SPAR9
FROM 
    awardsdecorations_nara a
LEFT JOIN awardsdecorations_command_staff_codes cmd 
    ON UPPER(replace(CAST(a.CMD AS VARCHAR), 'nan', '')) = UPPER(cmd.code)
LEFT JOIN awardsdecorations_service_country_codes svc 
    ON UPPER(replace(CAST(a.SVC AS VARCHAR), 'nan', '')) = UPPER(svc.code)
LEFT JOIN awardsdecorations_awards_decoration_codes awd_rec 
    ON UPPER(replace(CAST(a.AWDRC AS VARCHAR), 'nan', '')) = UPPER(awd_rec.code)
LEFT JOIN awardsdecorations_awards_decoration_codes awd_app 
    ON UPPER(replace(CAST(a.AWDPV AS VARCHAR), 'nan', '')) = UPPER(awd_app.code)
LEFT JOIN awardsdecorations_awards_decoration_codes awd_mac 
    ON UPPER(replace(CAST(a.MACRC AS VARCHAR), 'nan', '')) = UPPER(awd_mac.code)