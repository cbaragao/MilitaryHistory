SELECT
    b.BASNO
    , cprvs.value AS PRCNY
    , vcmrs.value AS VCMR
    , b.UTMC
    , b.UTM1
    , b.UTM2
    , b.UTM3
    , b.UTM4
    , b.UTM5
    , b.UTM6
    , b.UTM7
    , b.UTM8
    , b.UTM9
    , b.PR67
    , b.PR68
    , b.PR69
    , b.PR70
    , b.PR71
    , b.PR72
    , b.PR73
    , b.PR74
    , b.PR75
    , b.INDAT
    , b.IDATE
    , cstat.value AS CSTAT
    , b.CDATE
    , b.UDATE
    , b.LLC
    , b.LL1
    , b.LL2
    , b.LL3
    , b.LL4
    , b.LL5
    , b.LL6
    , b.LL7
    , b.LL8
    , b.LL9
    , b.ACYR
    , actions1.value AS ACJAN
    , conditions1.value AS CNJAN
    , actions2.value AS ACFEB
    , conditions2.value AS CNFEB
    , actions3.value AS ACMAR
    , conditions3.value AS CNMAR
    , actions4.value AS ACAPR
    , conditions4.value AS CNAPR
    , actions5.value AS ACMAY
    , conditions5.value AS CNMAY
    , actions6.value AS ACJUN
    , conditions6.value AS CNJUN
    , actions7.value AS ACJUL
    , conditions7.value AS CNJUL
    , actions8.value AS ACAUG
    , conditions8.value AS CNAUG
    , actions9.value AS ACSEP
    , conditions9.value AS CNSEP
    , actions10.value AS ACOCT
    , conditions10.value AS CNOCT
    , actions11.value AS ACNOV
    , conditions11.value AS CNNOV
    , actions12.value AS ACDEC
    , conditions12.value AS CNDEC
FROM  basfa_nara AS b
LEFT JOIN basfa_cprvs AS cprvs
    ON b.PRCNY = cprvs.code
LEFT JOIN basfa_vcmrs AS vcmrs
    ON b.VCMR = vcmrs.code
LEFT JOIN basfa_cstat AS cstat
    ON b.CSTAT = cstat.code
LEFT JOIN basfa_actions AS actions1
    ON b.ACJAN = actions1.code
LEFT JOIN basfa_conditions AS conditions1
    ON b.CNJAN = conditions1.code
LEFT JOIN basfa_actions AS actions2
    ON b.ACFEB = actions2.code
LEFT JOIN basfa_conditions AS conditions2
    ON b.CNFEB = conditions2.code
LEFT JOIN basfa_actions AS actions3
    ON b.ACMAR = actions3.code
LEFT JOIN basfa_conditions AS conditions3
    ON b.CNMAR = conditions3.code
LEFT JOIN basfa_actions AS actions4 
    ON b.ACAPR = actions4.code
LEFT JOIN basfa_conditions AS conditions4
    ON b.CNAPR = conditions4.code
LEFT JOIN basfa_actions AS actions5
    ON b.ACMAY = actions5.code
LEFT JOIN basfa_conditions AS conditions5
    ON b.CNMAY = conditions5.code
LEFT JOIN basfa_actions AS actions6
    ON b.ACJUN = actions6.code
LEFT JOIN basfa_conditions AS conditions6
    ON b.CNJUN = conditions6.code
LEFT JOIN basfa_actions AS actions7
    ON b.ACJUL = actions7.code
LEFT JOIN basfa_conditions AS conditions7
    ON b.CNJUL = conditions7.code
LEFT JOIN basfa_actions AS actions8
    ON b.ACAUG = actions8.code
LEFT JOIN basfa_conditions AS conditions8
    ON b.CNAUG = conditions8.code
LEFT JOIN basfa_actions AS actions9
    ON b.ACSEP = actions9.code
LEFT JOIN basfa_conditions AS conditions9
    ON b.CNSEP = conditions9.code
LEFT JOIN basfa_actions AS actions10
    ON b.ACOCT = actions10.code
LEFT JOIN basfa_conditions AS conditions10
    ON b.CNOCT = conditions10.code
LEFT JOIN basfa_actions AS actions11
    ON b.ACNOV = actions11.code
LEFT JOIN basfa_conditions AS conditions11
    ON b.CNNOV = conditions11.code
LEFT JOIN basfa_actions AS actions12
    ON b.ACDEC = actions12.code
LEFT JOIN basfa_conditions AS conditions12
    ON b.CNDEC = conditions12.code