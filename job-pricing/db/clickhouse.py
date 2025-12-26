import json
import os
from urllib.parse import quote as urlquote
from urllib.request import Request, urlopen

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "127.0.0.1")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8123"))
CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB", "pricing")
CH_FEATURE_TABLE = os.getenv("CH_FEATURE_TABLE", "job_features_1d")
CLICKHOUSE_TIMEOUT = int(os.getenv("CLICKHOUSE_TIMEOUT", "5"))


def ch_query(sql: str) -> str:
    url = (
        f"http://{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/"
        f"?database={urlquote(CLICKHOUSE_DB)}&query={urlquote(sql)}"
    )
    req = Request(url, method="GET")
    with urlopen(req, timeout=CLICKHOUSE_TIMEOUT) as resp:
        return resp.read().decode("utf-8")


def ch_build_sql(job_id: int) -> str:
    return f"""
    SELECT
        toString(dt) AS dt,
        job_id,
        impression_1d,
        view_1d,
        apply_1d,
        hire_1d
    FROM {CH_FEATURE_TABLE}
    WHERE job_id = {int(job_id)}
    ORDER BY dt DESC
    LIMIT 1
    FORMAT JSON
    """.strip()


def ch_fetch_features_1d(job_id: int):
    sql = ch_build_sql(job_id)
    try:
        raw = ch_query(sql)
        data = json.loads(raw)
        rows = data.get("data", [])
        return rows[0] if rows else None, sql, None
    except Exception as e:
        return None, sql, repr(e)
