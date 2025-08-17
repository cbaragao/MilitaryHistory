import json
import csv
import os

def load_schema(schema_path):
    with open(schema_path, 'r') as f:
        return json.load(f)["data"]

def load_code_tables(tables_dir):
    code_tables = {}
    for fname in os.listdir(tables_dir):
        if fname.endswith('.json'):
            with open(os.path.join(tables_dir, fname), 'r') as f:
                table = json.load(f)
                col_id = table.get("column_id") or table.get("column_ids", [None])[0]
                if col_id:
                    code_tables[col_id] = {row["code"]: row["value"] for row in table["data"]}
    return code_tables

def parse_fixed_width_line(line, schema):
    record = {}
    pos = 0
    for field in schema:
        length = field["length"] if field["length"] else 0
        if length > 0:
            raw = line[pos:pos+length]
            record[field["id"]] = raw.strip()
            pos += length
    return record

def decode_record(record, schema, code_tables):
    for field in schema:
        col_id = field["id"]
        if col_id in code_tables and record.get(col_id):
            record[col_id] = code_tables[col_id].get(record[col_id], record[col_id])
    return record

def process_conga(fixed_file, schema_path, tables_dir, output_csv):
    schema = load_schema(schema_path)
    code_tables = load_code_tables(tables_dir)
    with open(fixed_file, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=[f["id"] for f in schema])
        writer.writeheader()
        for line in infile:
            record = parse_fixed_width_line(line, schema)
            record = decode_record(record, schema, code_tables)
            writer.writerow(record)

if __name__ == "__main__":
    process_conga(
        fixed_file="CONGA.6673FIX",
        schema_path="schema/schema.json",
        tables_dir="tables/",
        output_csv="conga_processed.csv"
    )
