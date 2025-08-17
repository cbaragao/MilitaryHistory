SELECT
    c.SDATE,
    c.STIME,
    c.ETIME,
    c.UIC,
    c.SERIES,
    c.UDATE,
    c.SHNME,
    c.SHFTP,
    c.HLLNO,
    ac.value AS ARCOD,
    c.COARD AS COARD_utm,
    ot.value AS OPCOD,
    c.OPNAM,
    c.FCSUP,
    pd.value AS TCODE,
    tt.value AS TGCOD,
    pc.value AS PCODE,
    si.value AS SPOTS,
    dm.value AS DEDMS,
    c.NPKIA,
    c.NPWIA,
    c.NPMIA,
    wi.value AS WDI,
    c.PARA1,
    c.CALSR,
    c.ORDTYP,
    c.QTYEX,
    c.RANGE,
    c.PARA2,
    c.ACTYP,
    c.NACFT,
    c.TSORT,
    c.NSEXP,
    c.PARA3,
    lc.value AS LCODE,
    c.MLQTY,
    c.MLUNT,
    c.MLDDD,
    c.EPKIL
FROM
    conga_nara c
LEFT JOIN conga_area_codes ac 
    ON c.ARCOD = ac.code
LEFT JOIN conga_operation_types ot 
    ON c.OPCOD = ot.code
LEFT JOIN conga_period_of_day pd 
    ON c.TCODE = pd.code
LEFT JOIN conga_target_type_codes tt 
    ON c.TGCOD = tt.code
LEFT JOIN conga_province_codes pc 
    ON c.PCODE = pc.code
LEFT JOIN conga_spotter_info si 
    ON c.SPOTS = si.code
LEFT JOIN conga_dedms_codes dm 
    ON c.DEDMS = dm.code
LEFT JOIN conga_wdi_codes wi 
    ON c.WDI = wi.code
LEFT JOIN conga_target_type_codes lc 
    ON c.LCODE = lc.code
