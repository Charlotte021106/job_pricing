import os
import pymysql

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "") #输入密码
MYSQL_DB = os.getenv("MYSQL_DB", "job_pricing")
MYSQL_CHARSET = os.getenv("MYSQL_CHARSET", "utf8mb4")

PRICING_TABLE = os.getenv("PRICING_TABLE", "train_samples")
PRICE_COL = os.getenv("PRICE_COL", "price_label")


def get_conn():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset=MYSQL_CHARSET,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def mysql_get_baseline(job_id=None, company_id=None):
    if job_id is None and company_id is None:
        return None, None, None, None

    where = []
    params = []
    if job_id is not None:
        where.append("job_id=%s")
        params.append(job_id)
    if company_id is not None:
        where.append("company_id=%s")
        params.append(company_id)

    sql = (
        f"SELECT job_id, company_id, {PRICE_COL} AS price "
        f"FROM {PRICING_TABLE} WHERE {' AND '.join(where)} LIMIT 1"
    )

    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
        price = float(row["price"]) if row and row.get("price") is not None else None
        return row, price, sql, None
    except Exception as e:
        return None, None, sql, repr(e)
    finally:
        try:
            conn.close()
        except Exception:
            pass
