WITH filled_data AS (
    SELECT 
        h.*,
        ROW_NUMBER() OVER (ORDER BY rowid) as row_num,
        -- Forward fill the date field
        LAST_VALUE(
            CASE 
                WHEN replace(CAST(h.DATE_INCIDENT AS VARCHAR), 'nan', '') != '' 
                THEN replace(CAST(h.DATE_INCIDENT AS VARCHAR), 'nan', '')
                ELSE NULL 
            END IGNORE NULLS
        ) OVER (ORDER BY rowid ROWS UNBOUNDED PRECEDING) AS filled_date,
        -- Forward fill the time field  
        LAST_VALUE(
            CASE 
                WHEN replace(CAST(h.TIME_INCIDENT AS VARCHAR), 'nan', '') != '' 
                THEN replace(CAST(h.TIME_INCIDENT AS VARCHAR), 'nan', '')
                ELSE NULL 
            END IGNORE NULLS
        ) OVER (ORDER BY rowid ROWS UNBOUNDED PRECEDING) AS filled_time,
        -- Forward fill the operation name
        LAST_VALUE(
            CASE 
                WHEN replace(CAST(h.OPERATION_NAME AS VARCHAR), 'nan', '') != '' 
                THEN replace(CAST(h.OPERATION_NAME AS VARCHAR), 'nan', '')
                ELSE NULL 
            END IGNORE NULLS
        ) OVER (ORDER BY rowid ROWS UNBOUNDED PRECEDING) AS filled_operation
    FROM hosta_nara h
)
SELECT
    CASE 
        WHEN length(filled_date) = 8 
        THEN concat('19', right(filled_date, 2), '-', 
                   substring(filled_date, 1, 2), '-',
                   substring(filled_date, 4, 2))
        ELSE filled_date
    END AS DATE_INCIDENT,
    replace(CAST(f.BLANK1 AS VARCHAR), 'nan', '') AS BLANK1,
    COALESCE(filled_time, '') AS TIME_INCIDENT,
    replace(CAST(f.BLANK2 AS VARCHAR), 'nan', '') AS BLANK2,
    TRY_CAST(replace(CAST(f.NUM_HOSTILE_GUNS AS VARCHAR), 'nan', '') AS INTEGER) AS NUM_HOSTILE_GUNS,
    replace(CAST(f.SLASH1 AS VARCHAR), 'nan', '') AS SLASH1,
    replace(CAST(f.CALIBRE_HOSTILE_GUNS AS VARCHAR), 'nan', '') AS CALIBRE_HOSTILE_GUNS,
    replace(CAST(f.BLANK3 AS VARCHAR), 'nan', '') AS BLANK3,
    TRY_CAST(replace(CAST(f.ROUNDS_FIRED AS VARCHAR), 'nan', '') AS INTEGER) AS ROUNDS_FIRED,
    replace(CAST(f.ACCURACY_ENEMY_FIRE AS VARCHAR), 'nan', '') AS ACCURACY_ENEMY_FIRE,
    TRY_CAST(replace(CAST(f.TARGET_RANGE_YARDS AS VARCHAR), 'nan', '') AS INTEGER) AS TARGET_RANGE_YARDS,
    replace(CAST(f.SLASH_BLANK1 AS VARCHAR), 'nan', '') AS SLASH_BLANK1,
    TRY_CAST(replace(CAST(f.UNKNOWN_NUMERIC AS VARCHAR), 'nan', '') AS INTEGER) AS UNKNOWN_NUMERIC,
    replace(CAST(f.BLANK4 AS VARCHAR), 'nan', '') AS BLANK4,
    replace(CAST(f.SHIP_NAME AS VARCHAR), 'nan', '') AS SHIP_NAME,
    replace(CAST(f.DAMAGE_SHIP AS VARCHAR), 'nan', '') AS DAMAGE_SHIP,
    replace(CAST(f.BLANK5 AS VARCHAR), 'nan', '') AS BLANK5,
    replace(CAST(f.FRIENDLY_KIA AS VARCHAR), 'nan', '') AS FRIENDLY_KIA,
    replace(CAST(f.SLASH2 AS VARCHAR), 'nan', '') AS SLASH2,
    TRY_CAST(replace(CAST(f.FRIENDLY_WIA AS VARCHAR), 'nan', '') AS INTEGER) AS FRIENDLY_WIA,
    replace(CAST(f.BLANK6 AS VARCHAR), 'nan', '') AS BLANK6,
    COALESCE(f.filled_operation, '') AS OPERATION_NAME
FROM 
    filled_data f