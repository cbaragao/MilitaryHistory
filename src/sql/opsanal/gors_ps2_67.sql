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
,remove_nan_decimals(ps2.OBJEC) AS OBJEC
,remove_nan_decimals(ps2.OBJDS) AS OBJDS
FROM opsanal.main.gors_ps2_67_nara ps2