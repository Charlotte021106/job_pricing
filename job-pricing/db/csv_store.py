import csv
import os
from datetime import datetime
from job_pricing.utils import to_float, parse_dt

JOB_FEATURES_CSV = os.getenv(
    "JOB_FEATURES_CSV",
    os.path.join(os.getcwd(), "backend", "data", "job_features_1d.csv"),
)


def csv_fetch_features_1d(job_id: int):
    best = None
    best_dt = None

    with open(JOB_FEATURES_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                if int(r.get("job_id", -1)) != int(job_id):
                    continue
            except Exception:
                continue

            dt_val = parse_dt(r.get("dt")) or datetime.min
            if best is None or dt_val > best_dt:
                best_dt = dt_val
                best = {
                    "job_id": job_id,
                    "impression_1d": to_float(r.get("impression_1d")),
                    "view_1d": to_float(r.get("view_1d")),
                    "apply_1d": to_float(r.get("apply_1d")),
                    "hire_1d": to_float(r.get("hire_1d")),
                }

    return best
