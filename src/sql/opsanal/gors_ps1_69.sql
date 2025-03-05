SELECT
ps1."DATE"
,format_date(ps1."DATE",6) AS DATE_C
,ps1.DATAT
,get_gors_datat(ps1.DATAT) AS DATAT_C
,ps1.SERAL
,remove_nan_decimals(ps1.CORP) AS CORP
,remove_nan_decimals(ps1.PART) AS PART
, get_gors_part(remove_nan_decimals(ps1.PART),ps1.DATAT) AS PART_C
,ps1.PCN
,ps1.PSSQ1
,ps1.VSZ1
,ps1.FSLIN
,CASE WHEN ps1.NGFS = '999' THEN NULL ELSE ps1.NGFS END AS NGFS
,gs1.value AS CONAT
,remove_nan_decimals(ps1.CONAM) AS CONAM
,gs2.value AS ARSVC
,remove_nan_decimals(ps1.ARCFT) AS ARCFT
FROM opsanal.main.gors_ps1_69_nara ps1
LEFT JOIN opsanal.main.gors_69_gsvcs gs1
	ON remove_nan_decimals(ps1.CONAT) = gs1.code
LEFT JOIN opsanal.main.gors_69_gsvcs gs2
	ON remove_nan_decimals(ps1.ARSVC) = gs2.code
