import json
import zipfile
import os
import re
import pandas as pd

def extract_source_tables_from_vpax(vpax_path):
    results = []
    file_name = os.path.basename(vpax_path)

    extract_path = os.path.join("vpax_extracted_temp")
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(vpax_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    model_path = os.path.join(extract_path, "model.bim")
    if not os.path.exists(model_path):
        print(f"model.bim not found in {file_name}")
        return results

    with open(model_path, 'r', encoding='utf-8-sig') as f:
        model_data = json.load(f)

    tables = model_data.get("model", {}).get("tables", [])
    for table in tables:
        for partition in table.get('partitions', []):
            source = partition.get('source', {})
            if source.get('type') == 'm':
                expression = source.get('expression', '')

                sql_candidates = extract_sql_strings(expression)

                for sql in sql_candidates:
                    found = re.findall(r'(?:FROM|JOIN|INNER\s+JOIN|LEFT\s+JOIN|RIGHT\s+JOIN|FULL\s+JOIN)\s+((?:[A-Z0-9_]+\.){1,2}[A-Z0-9_]+)', sql, re.IGNORECASE)
                    unique_tables = sorted(set(found))

                    for src_table in unique_tables:
                        results.append({
                            "vpax_file_name": file_name,
                            "table_name": table['name'],
                            "partition_name": partition.get("name", "unknown"),
                            "source_table": src_table
                        })
    return results

def extract_sql_strings(expression):
    quoted_strings = re.findall(r'"((?:[^"]|"")*)"', expression)

    
    sql_candidates = []
    for s in quoted_strings:
        clean = s.replace('""', '').replace('#(lf)', '\n').replace('#(tab)', '\t')
        if re.match(r'^\s*(SELECT|WITH|--)', clean, re.IGNORECASE):
            sql_candidates.append(clean)

    return sql_candidates

def process_all_vpax_in_directory():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    all_results = []

    for file in os.listdir(script_dir):
        if file.lower().endswith(".vpax"):
            vpax_path = os.path.join(script_dir, file)
            print(f"Processing: {file}")
            file_results = extract_source_tables_from_vpax(vpax_path)
            all_results.extend(file_results)

    if all_results:
        df = pd.DataFrame(all_results)
        output_excel = os.path.join(script_dir, "vpax_source_tables_summary.xlsx")
        df.to_excel(output_excel, index=False)
        print(f"\nExtracted source tables saved to: {output_excel}")
    else:
        print("No data found.")

if __name__ == "__main__":
    process_all_vpax_in_directory()
