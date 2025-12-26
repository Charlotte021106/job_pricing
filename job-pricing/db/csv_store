import csv
from job_pricing.utils import safe_float

def get_features_from_csv(job_id: int, path="job_features_1d.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["job_id"]) == job_id:
                return {
                    "impression_1d": safe_float(row["impression_1d"]),
                    "view_1d": safe_float(row["view_1d"]),
                    "apply_1d": safe_float(row["apply_1d"]),
                    "hire_1d": safe_float(row["hire_1d"]),
                }
    return None
