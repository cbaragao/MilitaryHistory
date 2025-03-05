SELECT 
	ps7."DATE"
	,format_date(ps7."DATE",6) AS DATE_C
	,ps7.DATAT
	,get_gors_datat(ps7.DATAT) AS DATAT_C
	,ps7.SERAL
	,remove_nan_decimals(ps7.CORP) AS CORP
	,remove_nan_decimals(ps7.PART) AS PART
	,get_gors_part(remove_nan_decimals(ps7.PART),remove_nan_decimals(ps7.PART))  AS PART_C
	,ps7.PCN
	,ps7.PSSQ7
	,ps7.VSZ7
	,remove_nan_decimals(ps7.LCTZ1) AS LCTZ1
	,remove_nan_decimals(ps7.LCTZ2) AS LCTZ2
	,remove_nan_decimals(ps7.LCTZ3) AS LCTZ3
	,remove_nan_decimals(ps7.LCTZ4) AS LCTZ4
	,remove_nan_decimals(ps7.SLINS) AS SLINS
	,remove_nan_decimals(ps7.LNAT) AS LNAT
	, gs1.value AS LNAT_C
	,remove_nan_decimals(ps7.LTYPE) AS LTYPE
	,remove_nan_decimals(ps7.LNATI) AS LNATI
	,gs2.value AS LNATI_C
FROM opsanal.main.gors_ps7_71_72_nara ps7
LEFT JOIN opsanal.main.gors_71_72_gsvcs gs1
	ON remove_nan_decimals(ps7.LNAT)  = gs1.code
LEFT JOIN opsanal.main.gors_71_72_gtyps gt 
	ON remove_nan_decimals(ps7.LTYPE) = gt.code
LEFT JOIN opsanal.main.gors_71_72_gsvcs gs2
	ON remove_nan_decimals(ps7.LNATI)  = gs2.code