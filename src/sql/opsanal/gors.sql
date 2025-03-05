SELECT
format_date(g."DATE", 6) AS "DATE"
,get_gors_datat(g.DATAT) AS DATAT
,g.SERAL
,split_part(g.CORP,'.',1) AS CORP
,get_gors_part(split_part(g.PART,'.',1), g.DATAT, format_date(g."DATE", 6)) AS PART
,g.PCN
,replace(g.SC0,'nan', null) AS SC0
,g.VSZ
,g.OPDAY
,g.CTDAY
,gs.value AS FNATL
,g.CNTRY
,g.OPNAM
,fw.value AS OPCOD
,julian_to_calendar(g.UDATE,2,3) AS UDATE
,prov1.value AS PRVC1
,prov2.value AS PRVC2
,prov3.value AS PRVC3
,format_date(g.DTEI,8) AS DTEI
,format_time(g.HOURI) AS HOURI
,format_date(g.DTET,8) AS DTET
,format_time(g.HOURT) AS HOURT
FROM opsanal.main.gors_67_nara g
LEFT JOIN opsanal.main.gors_67_gsvcs gs
ON g.FNATL = gs.code
LEFT JOIN opsanal.main.gors_67_fwops fw
ON g.OPCOD = fw.code
LEFT JOIN opsanal.main.gors_67_provs prov1
ON split_part(CAST(g.PRVC1 AS char),'.',1)  = prov1.code
LEFT JOIN opsanal.main.gors_67_provs prov2
ON split_part(CAST(g.PRVC2 AS char),'.',1)  = prov2.code
LEFT JOIN opsanal.main.gors_67_provs prov3
ON split_part(CAST(g.PRVC3 AS char),'.',1)  = prov3.code