import os
import pymysql

def create_mysql_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""), #输入密码
        database=os.getenv("MYSQL_DB", "job_pricing"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def get_baseline_price_from_mysql(job_id=None, company_id=None):
    if job_id is None and company_id is None:
        return None

    sql = "SELECT price_label FROM train_samples WHERE job_id=%s LIMIT 1"

    conn = create_mysql_connection()
    with conn.cursor() as cur:
        cur.execute(sql, (job_id,))
        row = cur.fetchone()

    return float(row["price_label"]) if row else None
