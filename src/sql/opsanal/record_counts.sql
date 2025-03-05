WITH un AS (
SELECT
	'BASFA' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.basfa_tx
	UNION
SELECT
	'SEAFA' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.seafa_tx
	UNION
SELECT
	'TIRSA' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.tirsa_tx
	UNION
SELECT
	'VCIIA' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.vciia_tx
UNION
SELECT
	'GORS_67' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.gors_67_tx
UNION
SELECT
	'GORS_68' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.gors_68_tx
UNION
SELECT
	'GORS_69' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.gors_69_tx
UNION
SELECT
	'GORS_70' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.gors_70_tx
UNION
SELECT
	'GORS_71_72' AS Dataset,
	COUNT(*) AS "Count"
FROM
	opsanal.main.gors_71_72_tx
	)
SELECT 
		SUM(u."Count") AS row_count
FROM
	un u