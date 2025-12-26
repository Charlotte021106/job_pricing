from job_pricing.db.clickhouse import ch_fetch_features_1d
from job_pricing.db.csv_store import csv_fetch_features_1d

FEATURE_STORE_MODE = "auto"

def fetch_features_1d(job_id: int):
    feats, sql, err = ch_fetch_features_1d(job_id)
    if feats and not err:
        return feats

    return csv_fetch_features_1d(job_id)
