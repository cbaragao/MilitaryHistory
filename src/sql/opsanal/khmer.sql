SELECT
    k.MSGDAT,
    k.ITEMNO,
    k.FLG1,
    k.FLG2,
    k.FLG3_FLG4,
    k.MRSD,
    k.ADCT,
    k.ADCR,
    k.INCDATE,
    k.QTR,
    k.HY,
    k.INIT,
    k.EF,
    k.IACT,
    k.OBJECT,
    k.RACT,
    k.EWEAP,
    k.FACT,
    k.EACT,
    k.UTM,
    k.CORD,
    -- Parse latitude from LATLONG field in format ddmmssxDDDMMSSX
    CASE
        WHEN k.LATLONG IS NULL OR k.LATLONG = '' OR LENGTH(TRIM(k.LATLONG)) < 15 THEN NULL
        WHEN SUBSTRING(k.LATLONG, 7, 1) = 'N' THEN 
            CAST(SUBSTRING(k.LATLONG, 1, 2) AS FLOAT) + 
            CAST(SUBSTRING(k.LATLONG, 3, 2) AS FLOAT) / 60.0 + 
            CAST(SUBSTRING(k.LATLONG, 5, 2) AS FLOAT) / 3600.0
        WHEN SUBSTRING(k.LATLONG, 7, 1) = 'S' THEN 
            -(CAST(SUBSTRING(k.LATLONG, 1, 2) AS FLOAT) + 
              CAST(SUBSTRING(k.LATLONG, 3, 2) AS FLOAT) / 60.0 + 
              CAST(SUBSTRING(k.LATLONG, 5, 2) AS FLOAT) / 3600.0)
        ELSE NULL
    END AS LATLONG_LAT,
    -- Parse longitude from LATLONG field in format ddmmssxDDDMMSSX
    CASE
        WHEN k.LATLONG IS NULL OR k.LATLONG = '' OR LENGTH(TRIM(k.LATLONG)) < 15 THEN NULL
        WHEN SUBSTRING(k.LATLONG, 15, 1) = 'E' THEN 
            CAST(SUBSTRING(k.LATLONG, 8, 3) AS FLOAT) + 
            CAST(SUBSTRING(k.LATLONG, 11, 2) AS FLOAT) / 60.0 + 
            CAST(SUBSTRING(k.LATLONG, 13, 2) AS FLOAT) / 3600.0
        WHEN SUBSTRING(k.LATLONG, 15, 1) = 'W' THEN 
            -(CAST(SUBSTRING(k.LATLONG, 8, 3) AS FLOAT) + 
              CAST(SUBSTRING(k.LATLONG, 11, 2) AS FLOAT) / 60.0 + 
              CAST(SUBSTRING(k.LATLONG, 13, 2) AS FLOAT) / 3600.0)
        ELSE NULL
    END AS LATLONG_LONG,
    k.LATLONG,
    k.ITIME,
    k.WK,
    k.FNUMB,
    k.FTYPE,
    k.FSIZE,
    k.FNAT,
    k.ESIZE,
    k.ENAT,
    k.LOCNM,
    k.COMMENT,
    k.SETCD,
    k.SETEF,
    k.ASSOC,
    k.KIA,
    k.WIA,
    k.CAP,
    k.RAL,
    k.PERCOM
FROM
    khmer_nara k
ORDER BY k.MSGDAT, k.ITEMNO