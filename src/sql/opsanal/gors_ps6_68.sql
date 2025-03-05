SELECT 
	ps6."DATE"
	,format_date(ps6."DATE",6) AS DATE_C
	,ps6.DATAT
	,get_gors_datat(ps6.DATAT) AS DATAT_C
	,ps6.SERAL
	,remove_nan_decimals(ps6.CORP) AS CORP
	,remove_nan_decimals(ps6.PART) AS PART
	,get_gors_part(remove_nan_decimals(ps6.PART),remove_nan_decimals(ps6.PART))  AS PART_C
	,ps6.PCN
	,ps6.PSSQ6
	,ps6.VSZ6
	,remove_nan_decimals(ps6.RTWER) AS RTWER
	,remove_nan_decimals(ps6.RTPER) AS RTPER
	,remove_nan_decimals(ps6.RVNRR) AS RVNRR
	,remove_nan_decimals(ps6.RVNRL) AS RVNRL
	,remove_nan_decimals(ps6.RVNPR) AS RVNPR
	,remove_nan_decimals(ps6.LINSS) AS LINSS
FROM opsanal.main.gors_ps6_68_nara ps6