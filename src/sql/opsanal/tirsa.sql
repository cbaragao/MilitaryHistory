SELECT
	t.MYM,
	t.WEEK,
	t.SRONO,
	c.value AS CORPS,
	pc.value AS PROVN,
	t.DIST,
	t.VILGE,
	t.HAMLT,
	t.YEAR,
	t.MONTH,
	t.DAY,
	t.TODAY,
	t.UTMC,
	t.NEAR,
	t.QTR,
	m1.value AS PMEANS,
	v1.value AS PACT,
	o1.value AS POBJ,
	e.value AS ESTRT,
	t.SGCNT,
	t.PSC,
	t.PRIME,
	m2.value AS MEANS,
	o2.value AS VCOBJ,
	v2.value AS VCACT,
	t.RSCNT,
	t.PRIME2,
	m3.value AS MEANS2,
	o3.value AS VCOBJ2,
	v3.value AS VCACT2,
	t.RSCNT_1 AS RSCNT2
FROM
	tirsa_nara t
LEFT JOIN tirsa_corps c 
ON
	t.CORPS = c.code
LEFT JOIN tirsa_estrt e 
ON
	t.ESTRT = e.code
LEFT JOIN tirsa_means m1 
ON
	t.PMEANS = m1.code
LEFT JOIN tirsa_means m2
ON
	t.MEANS = m2.code
LEFT JOIN tirsa_means m3 
ON
	t.MEANS2 = m3.code
LEFT JOIN tirsa_vcact v1
ON
	t.PACT = v1.code
LEFT JOIN tirsa_vcact v2
ON
	t.VCACT = v2.code
LEFT JOIN tirsa_vcact v3
ON
	t.VCACT2 = v3.code
LEFT JOIN tirsa_objectives o1 
ON
	t.POBJ = o1.code
LEFT JOIN tirsa_objectives o2 
ON
	t.VCOBJ = o2.code
LEFT JOIN tirsa_objectives o3 
ON
	t.VCOBJ2 = o3.code
LEFT JOIN tirsa_province_codes pc 
ON
	CAST(t.PROVN AS VARCHAR) = pc.code 
