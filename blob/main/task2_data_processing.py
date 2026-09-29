# 2_clean.py
import json
import os

def clean_data():
    print("[2/4] Initializing data cleaning pipeline...")
    input_file = "raw_trends.json"
    output_file = "clean_trends.json"

    if not os.path.exists(input_file):
        print(f"[!] Error: '{input_file}' not found. Please run 1_fetch.py first.")
        return

    with open(input_file, "r") as f:
        raw_data = json.load(f)

    cleaned_data = []
    for record in raw_data:
        # 1. Validation Guardrail: Ensure fields aren't blank
        if not record.get("topic"):
            print("[-] Dropping record: Missing 'topic' name identifier.")
            continue

        # 2. Validation Guardrail: Volume metrics cannot logically be zero or negative
        if record.get("volume", 0) <= 0:
            print(f"[-] Dropping record for '{record['topic']}': Invalid negative volume data.")
            continue

        # 3. Standardization: Normalize data structures
        record["topic"] = record["topic"].strip().title()
        record["region"] = record["region"].upper()
        cleaned_data.append(record)

    with open(output_file, "w") as f:
        json.dump(cleaned_data, f, indent=4)
    print(f"[✓] Data cleansing complete. {len(cleaned_data)} valid records saved to '{output_file}'.")

if __name__ == "__main__":
    clean_data()
