SELECT
g."DATE"
,format_date(g."DATE", 6) AS DATE_C
,g.DATAT
,get_gors_datat(g.DATAT) AS DATAT_C
,g.SERAL
,remove_nan_decimals(g.CORP) AS CORP
,remove_nan_decimals(g.PART) AS PART
,get_gors_part(remove_nan_decimals(g.PART), g.DATAT) AS PART_C
,g.PCN
,replace(g.SC0,'nan', null) AS SC0
,g.VSZ
,g.OPDAY
,g.CTDAY
,gs.value AS FNATL
,CASE WHEN g.CNTRY = 'nan' THEN NULL else g.CNTRY END AS CNTRY
,remove_nan_decimals(g.OPNAM) AS OPNAM
,fw.value AS OPCOD
,remove_nan_decimals(g.UDATE) AS UDATE
,julian_to_calendar(remove_nan_decimals(g.UDATE),2,3) AS UDATE_C
,prov1.value AS PRVC1
,prov2.value AS PRVC2
,prov3.value AS PRVC3
,remove_nan_decimals(g.DTEI) AS DTEI
,format_date(g.DTEI,8) AS DTEI_C
,split_part(g.HOURI,'.',1) AS HOURI
,format_time(g.HOURI) AS HOURI_C
,remove_nan_decimals(g.DTET) AS DTET
,format_date(g.DTET,8) AS DTET_C
,remove_nan_decimals(g.HOURT) AS HOURT
,format_time(g.HOURT) AS HOURT_C
FROM opsanal.main.gors_71_72_nara g
LEFT JOIN opsanal.main.gors_71_72_gsvcs gs
ON g.FNATL = gs.code
LEFT JOIN opsanal.main.gors_71_72_fwops fw
ON g.OPCOD = fw.code
LEFT JOIN opsanal.main.gors_71_72_provs prov1
ON split_part(CAST(g.PRVC1 AS char),'.',1)  = prov1.code
LEFT JOIN opsanal.main.gors_71_72_provs prov2
ON split_part(CAST(g.PRVC2 AS char),'.',1)  = prov2.code
LEFT JOIN opsanal.main.gors_71_72_provs prov3
ON split_part(CAST(g.PRVC3 AS char),'.',1)  = prov3.code