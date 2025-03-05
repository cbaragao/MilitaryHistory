SELECT
	s.UNITO,
	s.YEAR,
	s.MONTH,
	s.UNAME,
	s.PROV,
	l.province_name AS PROVINCE_NAME,
	l.viet_cong_military_region AS VIET_CONG_MILITARY_REGION,
	l.corps_area AS CORPS_AREA,
	s.UTMQD,
	s.UTMES,
	s.UTMNO,
	v.value AS VCMR,
	c.value AS CORPS_TACTICAL_ZONE,
	sv.value AS SERVICE,
	s.MISSN,
	cn.value AS COUNTRY,
	ut.value AS UNIT_TYPE,
	s.CTLHQ,
	s.STATN,
	s.DIAID,
	s.CORDS,
	un.value AS UNIT_TYPE_STALA,
	s.RSRVD
FROM
	seafa_nara s
LEFT JOIN seafa_locations l 
ON
	s.PROV = l.province_code
LEFT JOIN seafa_vcmr v 
ON
	s.VCMR = v.code
LEFT JOIN seafa_ctz c
ON
	s.CTZ = c.code
LEFT JOIN seafa_serv sv 
ON
	s.SERV = sv.code
LEFT JOIN seafa_cntry cn 
ON
	s.CNTRY = cn.code
LEFT JOIN seafa_utype ut 
ON
	s.UTYPE = ut.code
LEFT JOIN seafa_untyp un 
ON
	s.UNTYP = un.code