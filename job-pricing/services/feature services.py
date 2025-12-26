from job_pricing.db.clickhouse import get_features_from_clickhouse
from job_pricing.db.csv_store import get_features_from_csv

def get_job_features(job_id: int):
    features = get_features_from_clickhouse(job_id)
    if features:
        return features

    return get_features_from_csv(job_id)
