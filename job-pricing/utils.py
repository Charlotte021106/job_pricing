from datetime import datetime

def to_float(x) -> float:
    if x is None:
        return 0.0
    try:
        s = str(x).strip()
        if s == "" or s.lower() == "nan":
            return 0.0
        return float(s)
    except Exception:
        return 0.0


def parse_dt(dt_str: str):
    dt_str = (dt_str or "").strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(dt_str, fmt)
        except Exception:
            pass
    return None
