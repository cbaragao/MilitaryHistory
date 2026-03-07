#!/usr/bin/env python3
"""
HES (Hamlet Evaluation System) Data Processing Script
Reads local CSV, uploads to Data.world, and ingests into SQL Server.
"""

import os
import sys
import math
import numpy as np
import pandas as pd

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

DATASET     = "hes"
DDW_PROJECT = "aragaocb/hes"
CSV_PATH    = os.path.join(parent_dir, '..', 'opsanal', 'hes', 'HES_gazateer_v1.csv')
SQL_CONN    = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=vietnam;"
    "Trusted_Connection=yes;"
)

print(f"🚀 Processing {DATASET}...")

# --- Read source CSV ---
df = pd.read_csv(CSV_PATH)
df_clean = df.replace('nan', np.nan).infer_objects()
print(f"   Loaded {len(df_clean):,} rows, {len(df_clean.columns)} columns")

# --- Ingest into SQL Server ---
def sql_type(dtype):
    s = str(dtype)
    if 'int' in s:      return 'BIGINT'
    if 'float' in s:    return 'FLOAT'
    if 'bool' in s:     return 'BIT'
    if 'datetime' in s: return 'DATETIME2'
    return 'NVARCHAR(MAX)'

def clean_val(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    if hasattr(v, 'item'):
        return v.item()
    return v

col_defs     = ', '.join(f'[{c}] {sql_type(t)}' for c, t in df_clean.dtypes.items())
col_names    = ', '.join(f'[{c}]' for c in df_clean.columns)
placeholders = ', '.join('?' for _ in df_clean.columns)
records = [tuple(clean_val(v) for v in row) for row in df_clean.itertuples(index=False)]

import pyodbc
print(f"   Ingesting {len(records):,} rows into SQL Server 'vietnam.dbo.{DATASET}'...")
with pyodbc.connect(SQL_CONN, autocommit=False) as conn:
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.execute(f"IF OBJECT_ID('dbo.{DATASET}', 'U') IS NOT NULL DROP TABLE dbo.{DATASET}")
    cursor.execute(f"CREATE TABLE dbo.{DATASET} ({col_defs})")
    cursor.executemany(f"INSERT INTO dbo.{DATASET} ({col_names}) VALUES ({placeholders})", records)
    conn.commit()

print(f"✅ {DATASET} processing complete!")
