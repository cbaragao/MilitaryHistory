SELECT
	v.SITRP,
	replace(v.PCN,
	'nan',
	'') AS PCN,
	replace(v.SC0,
	'nan',
	'') AS SC0,
	CAST(v.VSZ AS float) AS VSZ,
	CAST(v.EKIAC AS float) AS EKIAC,
	CAST(v.EWIAC AS float) AS EWIAC,
	CAST(v.EPOWC AS float) EPOWC,
	CAST(replace(v.QUART,
	'nan',
	'0') AS INT) AS QUART,
	replace(split_part(v.ZNDIV,
	'.',
	1),'nan','') AS ZNDIV,
	x.value AS XNAME,
	p.value AS PROVN,
	r.value AS REGON,
	split_part(v.CORPS,
	'.',
	1) AS CORPS,
	v.COORX AS COORX_UTM,
	split_part(CASE
		WHEN length(v.SDATE) = 8 then concat('19',
		left(split_part(v.SDATE,
		'.',
		1),
		2),
		'-',
		substring(split_part(v.SDATE, '.', 1), 3, 2),
		'-',
		right(split_part(v.SDATE,
		'.',
		1),
		2))
		ELSE v.SDATE
	END,
	'.',
	1) AS SDATE,
	split_part(v.STIME,
	'.',
	1) AS STIME
FROM
	vciia_nara v
LEFT JOIN vciia_xname x
ON
	split_part(v.XNAME,
	'.',
	1) = x.code
LEFT JOIN vciia_province_codes p 
ON
	split_part(v.PROVN,
	'.',
	1) = p.code
LEFT JOIN vciia_regon r 
ON
	lpad(split_part(v.REGON,
	'.',
	1),
	2,
	'0')= r.code