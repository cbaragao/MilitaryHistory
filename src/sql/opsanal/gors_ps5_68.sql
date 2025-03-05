SELECT 
	ps5."DATE"
	,format_date(ps5."DATE",6) AS DATE_C
	,ps5.DATAT
	,get_gors_datat(ps5.DATAT) AS DATAT_C
	,ps5.SERAL
	,remove_nan_decimals(ps5.CORP) AS CORP
	,remove_nan_decimals(ps5.PART) AS PART
	,get_gors_part(remove_nan_decimals(ps5.PART),remove_nan_decimals(ps5.PART))  AS PART_C
	,ps5.PCN
	,ps5.PSSQ5 
	,ps5.VSZ5
	,ps5.IACTS 
	,ps5.IWCTD 
	,ps5.IWOCT 
	,ps5.IATT 
	,ps5.ITERR 
	,ps5.ISABT 
	,ps5.IPROP
	,ps5.IHARR 
	,ps5.IAA 
	,ps5.SFLIN 
	,remove_nan_decimals(ps5.INATL) AS INATL 
	, gs.value AS INATL_C
	,remove_nan_decimals(ps5.ISIZE) AS ISIZE
	, fw.value AS ISIZE_C
	,remove_nan_decimals(ps5.ICTZ) AS ICTZ
FROM opsanal.main.gors_ps5_68_nara ps5
LEFT JOIN opsanal.main.gors_68_gsvcs gs
	ON remove_nan_decimals(ps5.INATL) = gs.code
LEFT JOIN opsanal.main.gors_68_fwszs fw
	ON remove_nan_decimals(ps5.ISIZE) = fw.code