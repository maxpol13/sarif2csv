import sys
import json
import csv
from collections import Counter

def count_rule_violations(sarif_path, output_csv="rule_violations_count.csv"):
    with open(sarif_path, "r", encoding="utf-8") as f:
        sarif = json.load(f)
    # SARIF files may have multiple runs
    all_results = []
    for run in sarif.get("runs", []):
        all_results.extend(run.get("results", []))
    # Count ruleId occurrences
    rule_counter = Counter()
    for result in all_results:
        rule_id = result.get("ruleId")
        if rule_id:
            rule_counter[rule_id] += 1

    # If possible, resolve rule name from the run's tool.driver.rules section
    rule_names = {}
    for run in sarif.get("runs", []):
        driver = run.get("tool", {}).get("driver", {})
        for rule in driver.get("rules", []):
            rule_id = rule.get("id")
            rule_name = rule.get("name") or rule_id
            if rule_id:
                rule_names[rule_id] = rule_name

    # Write to CSV: columns are Rule Name, Violations
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Rule", "Violations"])
        for rule_id, count in rule_counter.items():
            rule_name = rule_names.get(rule_id, rule_id)
            writer.writerow([rule_name, count])

    print(f"Exported rule violations to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_sarif_rule_violations.py <sarif_report.json>")
        sys.exit(1)
    count_rule_violations(sys.argv[1])

