SELECT 
'19' || LEFT(sitra."DATE",2) || '-' ||SUBSTR(sitra."DATE",3,2) || '-' || RIGHT(sitra."DATE",2) AS "DATE", 
datat."value" AS DATAT, 
sitra.SERAL, 
corp."value" AS CORP, 
part."value" AS PART, 
fnatl."value" AS FNATL, 
cntry."value" AS CNTRY, 
sitra.OPNAM, 
opcod."value" AS OPCOD, 
sitra.UDATE, 
prvc1."value" AS PRVC1, 
prvc2."value" AS PRVC2, 
prvc3."value" AS PRVC3, 
CAST(sitra.OPDAY AS FLOAT) AS OPDAY, 
CAST(sitra.CTDAY AS FLOAT) AS CTDAY, 
'19' || LEFT(sitra.DTEI,2) || '-' ||SUBSTR(sitra.DTEI,3,2) || '-' || RIGHT(sitra.DTEI,2)  AS DTEI, 
sitra.HOURT, 
'19' || LEFT(sitra.DTET,2) || '-' ||SUBSTR(sitra.DTET,3,2) || '-' || RIGHT(sitra.DTET,2)  AS DTET, 
sitra.HOURI, 
remove_nan_decimals(sitra.FSLIN) AS FSLIN, 
conat."value" AS CONAT, 
sitra.CONAM, 
CAST(sitra.NGFS AS FLOAT) AS NGFS, 
arsvc."value" AS ARSVC, 
sitra.ARCFT, 
remove_nan_decimals(sitra.SSLIN) AS SSLIN, 
sitra.UTM, 
typat."value" AS TYPAT,
objec."value" AS OBJEC, 
objds."value" AS OBJDS, 
sitra.LINFS, 
svnat."value" AS SVNAT, 
CAST(sitra.NOOF AS FLOAT) AS NOOF, 
smth."value" AS SMTH, 
sitra.COMPY, 
sitra.BNID, 
sitra.BRDES, 
sitra.DVDES, 
sitra.MVRSP, 
resac."value" AS RESAC, 
sitra.TSLIN, 
lnatl."value" AS LNATL, 
lcode."value" AS LCODE,
sitra.LSDSC, 
CAST(sitra.NODES AS FLOAT) AS NODES, 
CAST(sitra.NODAM AS FLOAT) AS NODAM, 
CAST(sitra.NOCAP AS FLOAT) AS NOCAP, 
sitra.LUNIT, 
sitra.SFLIN, 
inatl."value" AS INATL,
isize."value" AS ISIZE, 
CAST(sitra.IACTS AS FLOAT) AS IACTS, 
CAST(sitra.IWCTD AS FLOAT) AS IWCTD, 
CAST(sitra.IWOCT AS FLOAT) AS IWOCT, 
CAST(sitra.IATT AS FLOAT) AS IATT, 
CAST(sitra.ITERR AS FLOAT) AS ITERR, 
CAST(sitra.ISABT AS FLOAT) AS ISABT, 
CAST(sitra.IPROP AS FLOAT) AS IPROP, 
CAST(sitra.IHARR AS FLOAT) AS IHARR, 
CAST(sitra.IAA AS FLOAT) AS IAA, 
ictz."value" AS ICTZ, 
sitra.LINSS, 
CAST(sitra.RTWER AS FLOAT) AS RTWER, 
CAST(sitra.RTPER AS FLOAT) AS RTPER, 
CAST(sitra.RVNRR AS FLOAT) AS RVNRR, 
CAST(sitra.RVNRL AS FLOAT) AS RVNRL, 
CAST(sitra.RVNPR AS FLOAT) AS RVNPR, 
sitra.SLINS, 
lnat."value" AS LNAT, 
ltype."value" AS LTYPE, 
CAST(sitra.LCTZ1 AS FLOAT) AS LCTZ1, 
CAST(sitra.LCTZ2 AS FLOAT) AS LCTZ2, 
CAST(sitra.LCTZ3 AS FLOAT) AS LCTZ3, 
CAST(sitra.LCTZ4 AS FLOAT) AS LCTZ4, 
lnati."value" AS LNATI
FROM opsanal.main.sitra_66_68_nara sitra
LEFT JOIN opsanal.main.sitra_66_68_cntry cntry 
	ON sitra.CNTRY = cntry.code 
LEFT JOIN opsanal.main.sitra_66_68_conat conat
	ON sitra.conat = conat.code 
LEFT JOIN opsanal.main.sitra_66_68_corp corp
	ON remove_nan_decimals(sitra.CORP) = corp.code
LEFT JOIN opsanal.main.sitra_66_68_datat datat
	ON sitra.DATAT = datat.code 
LEFT JOIN opsanal.main.sitra_66_68_fnatl fnatl 
	ON sitra.FNATL  = fnatl.code 
LEFT  JOIN opsanal.main.sitra_66_68_ictz ictz
	ON sitra.ICTZ = ictz.code 
LEFT JOIN opsanal.main.sitra_66_68_inatl inatl
	ON sitra.INATL = inatl.code 
LEFT JOIN opsanal.main.sitra_66_68_isize isize
	ON sitra.ISIZE = isize.code 
LEFT JOIN opsanal.main.sitra_66_68_lcode lcode 
	ON (sitra.LSCAT || sitra.LSCLS) = lcode.code 
LEFT JOIN opsanal.main.sitra_66_68_lnat lnat
	ON sitra.LNAT = lnat.code 
LEFT JOIN opsanal.main.sitra_66_68_lnati lnati
	ON sitra.lnati = lnati.code
LEFT JOIN opsanal.main.sitra_66_68_lnatl lnatl
	ON sitra.lnatl = lnatl.code 
LEFT JOIN opsanal.main.sitra_66_68_ltype ltype
	ON sitra.ltype = ltype.code 
LEFT JOIN opsanal.main.sitra_66_68_mvrsp mvsrp
	ON sitra.mvrsp = mvsrp.code
LEFT JOIN opsanal.main.sitra_66_68_objds objec
	ON remove_nan_decimals(sitra.objec) = objec.code
LEFT JOIN opsanal.main.sitra_66_68_objes objds
	ON remove_nan_decimals(sitra.objds) = objds.code 
LEFT JOIN opsanal.main.sitra_66_68_opcod opcod 
	ON sitra.OPCOD = opcod.code 
LEFT JOIN opsanal.main.sitra_66_68_part part 
	ON remove_nan_decimals(sitra.part) = part.code 
LEFT JOIN opsanal.main.sitra_66_68_prvc1 prvc1 
	ON sitra.prvc1 = prvc1.code 
LEFT JOIN opsanal.main.sitra_66_68_prvc2 prvc2
	ON sitra.prvc2 = prvc2.code 
LEFT JOIN opsanal.main.sitra_66_68_prvc3 prvc3 
	ON sitra.prvc3 = prvc3.code 
LEFT JOIN opsanal.main.sitra_66_68_resac resac
	ON sitra.resac =  resac.code
LEFT JOIN opsanal.main.sitra_66_68_smth smth 
	ON sitra.smth = smth.code 
LEFT JOIN opsanal.main.sitra_66_68_svnat svnat
	ON sitra.svnat = svnat.code 
LEFT JOIN opsanal.main.sitra_66_68_typat typat 
	ON sitra.typat = typat.code
LEFT JOIN opsanal.main.sitra_66_68_fnatl arsvc
	ON sitra.arsvc = typat.code
	;