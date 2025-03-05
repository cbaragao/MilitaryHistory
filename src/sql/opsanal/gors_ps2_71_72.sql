SELECT
ps2."DATE"
,format_date(ps2."DATE",6) AS DATE_C
,ps2.DATAT
,get_gors_datat(ps2.DATAT) AS DATAT_C
,ps2.SERAL
,remove_nan_decimals(ps2.CORP) AS CORP
,remove_nan_decimals(ps2.PART) AS PART
,get_gors_part(remove_nan_decimals(ps2.PART),remove_nan_decimals(ps2.PART))  AS PART_C
,ps2.PCN
,ps2.PSSQ2
,ps2.VSZ2
,ps2.SSLIN
,remove_nan_decimals(ps2.UTM) AS UTM
,remove_nan_decimals(ps2.TYPAT) AS TYPAT
, COALESCE(fw.value, ac.value) AS TYPAT_C
,remove_nan_decimals(ps2.OBJEC) AS OBJEC
, obj.value AS OBJEC_C
,remove_nan_decimals(ps2.OBJDS) AS OBJDS
, obd.value AS OBJDS_C
FROM opsanal.main.gors_ps2_71_72_nara ps2
LEFT JOIN opsanal.main.gors_71_72_fwops fw
	ON remove_nan_decimals(ps2.TYPAT) = fw.code 
LEFT JOIN opsanal.main.gors_71_72_actns ac
	ON remove_nan_decimals(ps2.TYPAT) = ac.code 
LEFT JOIN opsanal.main.gors_71_72_objes obj
	ON remove_nan_decimals(ps2.OBJEC) = obj.code
LEFT JOIN opsanal.main.gors_71_72_obdes obd
	ON remove_nan_decimals(ps2.OBJDS) = obd.code