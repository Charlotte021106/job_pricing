from datetime import datetime

def safe_float(value):
    try:
        if value is None:
            return 0.0
        return float(value)
    except Exception:
        return 0.0

def parse_datetime_string(text):
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except Exception:
            pass
    return None
