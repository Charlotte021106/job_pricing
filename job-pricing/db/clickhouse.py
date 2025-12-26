import os
import json
from urllib.request import urlopen
from urllib.parse import quote

def get_features_from_clickhouse(job_id: int):
    sql = f"""
    SELECT
        impression_1d,
        view_1d,
        apply_1d,
        hire_1d
    FROM job_features_1d
    WHERE job_id = {job_id}
    ORDER BY dt DESC
    LIMIT 1
    FORMAT JSON
    """

    url = (
        f"http://{os.getenv('CLICKHOUSE_HOST','127.0.0.1')}:8123/"
        f"?database=pricing&query={quote(sql)}"
    )

    resp = urlopen(url).read().decode("utf-8")
    data = json.loads(resp)["data"]

    return data[0] if data else None
