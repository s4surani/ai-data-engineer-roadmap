# pipeline_demo.py

import pandas as pd
from data_utils.validators import validate_record
from data_utils.calculators import calculate_metrics
from data_utils.formatters import format_output
from data_utils.transformers import clean_text, normalize_phone, parse_date, extract_domain

def main():
    df = pd.read_csv('data.csv')
    valid_records, invalid_records = [], []
    for idx, row in df.iterrows():
        record = row.to_dict()
        record['product'] = clean_text(record.get('product', ''))
        record['phone'] = normalize_phone(record.get('phone', ''))
        record['date'] = parse_date(record.get('date', ''))
        record['domain'] = extract_domain(record.get('email', ''))
        is_valid, errors, _ = validate_record(record, idx+1)
        if is_valid:
            valid_records.append(record)
        else:
            invalid_records.append({**record, "errors": errors})
    metrics = calculate_metrics(valid_records)
    html_report = format_output(valid_records, invalid_records, metrics)
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_report)

if __name__ == "__main__":
    main()
