SELECT
	CAST('19' || i.YEAR || '-' || lpad(i.MONTH,2,'0') || '-' || lpad(i.DAY,2,'0') AS DATE) AS REPORT_DATE,
	i.INSEQ,
	i.PCN,
	remove_nan_decimals(i.SC0) AS SC0,
	i.VSZ,
	CAST(CASE
		WHEN i.ILOC = '000000S0000000E' then null
		WHEN contains(i.ILOC,
		'N')= TRUE THEN left(i.ILOC,
		2) || '.' || substring(i.ILOC, 3, 4)
		WHEN contains(i.ILOC,
		'S')= TRUE THEN '-' || left(i.ILOC,
		2) || '.' || substring(i.ILOC, 3, 4)
		else i.ILOC
	end AS float) AS ILOC_LAT,
	CAST(CASE
		WHEN i.ILOC = '000000S0000000E' then null
		WHEN right(i.ILOC,
		1)= 'E' THEN LEFT(substring(i.ILOC, 8, 7),
		3) || '.' || right(substring(i.ILOC, 8, 7),
		4)
		WHEN right(i.ILOC,
		1)= 'W' THEN '-' || LEFT(substring(i.ILOC, 8, 7),
		3) || '.' || right(substring(i.ILOC, 8, 7),
		4)
		ELSE i.ILOC
	END AS float) AS ILOC_LONG,
	i.ILOC,
	i.NOINC,
	ic.value AS CAT,
	ia.value AS TYPAC,
	i.CNTRY,
	im.value AS REGION,
	ip.value AS PROV,
	format_time(remove_nan_decimals(i.ITIME)) AS ITIME,
	format_date(remove_nan_decimals(i.TDATE),6) AS TDATE,
	format_time(remove_nan_decimals(i.TTIME)) AS TTIME,
	in1.value AS INTFOR,
	in2.value AS FORATK,
	remove_nan_decimals(i.PLACE) AS PLACE,
	remove_nan_decimals(i.PLACD) AS PLACD
FROM
	opsanal.main.incda_nara i
LEFT JOIN opsanal.main.incda_catab ic
	ON remove_nan_decimals(i.CAT) = ic.code
LEFT JOIN opsanal.main.incda_actab ia 
	ON remove_nan_decimals(i.TYPAC) = ia.code 
LEFT JOIN opsanal.main.incda_mrtab im 
	ON remove_nan_decimals(i.REGION) = im.code
LEFT JOIN opsanal.main.incda_provtab ip 
	ON remove_nan_decimals(i.PROV) = ip.code
LEFT JOIN opsanal.main.incda_natab in1
	ON remove_nan_decimals(i.INTFOR) = in1.code
LEFT JOIN opsanal.main.incda_natab in2 
	ON remove_nan_decimals(i.FORATK) = in2.code