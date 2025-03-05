SELECT 
	ps4."DATE"
	,format_date(ps4."DATE",6) AS DATE_C
	,ps4.DATAT
	,get_gors_datat(ps4.DATAT) AS DATAT_C
	,ps4.SERAL
	,remove_nan_decimals(ps4.CORP) AS CORP
	,remove_nan_decimals(ps4.PART) AS PART
	,get_gors_part(remove_nan_decimals(ps4.PART),remove_nan_decimals(ps4.PART))  AS PART_C
	,ps4.PCN
	,ps4.PSSQ4
	,ps4.VSZ4
	,remove_nan_decimals(ps4.NODES)AS NODES
	,remove_nan_decimals(ps4.NODAM)AS NODAM
	,remove_nan_decimals(ps4.NOCAP)AS NOCAP
	,remove_nan_decimals(ps4.TSLIN)AS NOCAP
	,remove_nan_decimals(ps4.LNATL) AS LNATL
	,gs.value AS LNATL_C
	,remove_nan_decimals(ps4.LSCAT) AS LSCAT
	,remove_nan_decimals(ps4.LSCLS) AS LSCLS 
	,ca.value  AS LCODE_C
	,remove_nan_decimals(ps4.LSDSC) AS LSDSC
	,remove_nan_decimals(ps4.LUNIT) AS LUNIT
FROM opsanal.main.gors_ps4_70_nara ps4
LEFT JOIN opsanal.main.gors_70_gsvcs gs
	ON remove_nan_decimals(ps4.LNATL) = gs.code
LEFT JOIN opsanal.main.gors_70_catrs ca
ON CONCAT(remove_nan_decimals(ps4.LSCAT), remove_nan_decimals(ps4.LSCLS)) = ca.code