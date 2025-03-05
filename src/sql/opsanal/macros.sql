CREATE OR REPLACE MACRO format_date(a,
b)  AS TRY_CAST((CASE
	WHEN length(trim(a)) = b then CONCAT('19',
	left(split_part(CAST(a AS char(6)),
	'.',
	1),
	2),
	'-',
	substring(split_part(CAST(a AS char(6)), '.', 1), 3, 2),
	'-',
	right(split_part(CAST(a AS char(6)),
	'.',
	1),
	2))
	WHEN a = 'nan' THEN ''
	else a
end) AS DATE);

CREATE OR REPLACE MACRO format_time(a) AS 
CASE
	WHEN a <> 'nan' AND length(a) >=3 then lpad(split_part(a,
	'.',
	1),
	4,
	'0')
	WHEN a = 'nan' THEN NULL
	ELSE a
END ;

CREATE OR REPLACE MACRO julian_to_calendar(julian,
year_digits,
day_digits) AS 
TRY_CAST(CONCAT('19',
LEFT(julian,
year_digits),
'-01-01') AS DATE) + (TRY_CAST(CASE WHEN LEFT(RIGHT(julian,
day_digits),1)='0' THEN RIGHT(julian,
day_digits-1) ELSE RIGHT(julian,
day_digits) END  AS INT)-1);

CREATE OR REPLACE MACRO get_gors_part(part,
datat) AS 
CASE
	WHEN part='nan' then NULL 
	WHEN part = '1' and UPPER(datat) <> 'W' THEN 'U.S. forces'
	WHEN part = '2'and UPPER(datat) <> 'W' THEN 'F.W. forces'
	WHEN part = '3'and UPPER(datat) <> 'W' THEN 'RVN forces'
	WHEN part = '4'and UPPER(datat) <> 'W' THEN 'Enemy incidents'
	ELSE part
END;

CREATE OR REPLACE MACRO get_gors_datat(datat) AS 
CASE
	WHEN UPPER(datat) = 'W' THEN 'Weekly Statistical Summary'
	WHEN UPPER(datat) = 'E' THEN 'Enemy Initiated Incident'
	WHEN UPPER(datat) = 'S' THEN 'Small Unit Action or Summary'
	WHEN UPPER(datat) = 'L' THEN 'Large Scale Operation'
	ELSE datat
END;

CREATE OR REPLACE MACRO remove_nan_decimals(str) AS 
CASE WHEN str = 'nan' THEN NULL WHEN INSTR(str,'.')>0 THEN split_part(str,'.',1) ELSE str END;
