SELECT 
	ps3."DATE"
	,format_date(ps3."DATE",6) AS DATE_C
	,ps3.DATAT
	,get_gors_datat(ps3.DATAT) AS DATAT_C
	,ps3.SERAL
	,remove_nan_decimals(ps3.CORP) AS CORP
	,remove_nan_decimals(ps3.PART) AS PART
	,get_gors_part(remove_nan_decimals(ps3.PART),remove_nan_decimals(ps3.PART))  AS PART_C
	,ps3.PCN
	,ps3.PSSQ3
	,ps3.VSZ3
	,ps3.NOOF
	,ps3.LINFS
	,ps3.SVNAT
	,gs.value AS SVNAT_C
	,remove_nan_decimals(ps3.SMTH) AS SMTH
	, fw.value AS SMTH_C
	,remove_nan_decimals(ps3.COMPY) AS COMPY
	,remove_nan_decimals(ps3.BNID) AS BNID
	,remove_nan_decimals(ps3.BRDES) AS BRDES
	,remove_nan_decimals(ps3.DVDES) AS DVDES
	,remove_nan_decimals(ps3.MVRSP) AS MVRSP
	,remove_nan_decimals(ps3.RESAC) AS RESAC
	, CASE WHEN remove_nan_decimals(ps3.RESAC) = 'A' THEN 'Active' WHEN remove_nan_decimals(ps3.RESAC) = 'R' THEN 'Reserve' ELSE remove_nan_decimals(ps3.RESAC) END AS RESAC_C
FROM opsanal.main.gors_ps3_67_nara ps3
LEFT JOIN opsanal.main.gors_67_gsvcs gs
	ON ps3.SVNAT = gs.code
LEFT JOIN opsanal.main.gors_67_fwszs fw
	ON remove_nan_decimals(ps3.SMTH) = fw.code
