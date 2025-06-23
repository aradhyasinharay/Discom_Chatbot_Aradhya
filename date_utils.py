import re
from datetime import datetime
from logger import logger
from email.utils import parsedate_to_datetime


def extract_date(text):
    try:
        m = re.search(r'\b(202\d-\d{2}-\d{2})\b', text)
        return m.group(1) if m else datetime.now().strftime('%Y-%m-%d')
    except Exception as e:
        logger.error(f"Date extraction error: {e}")
        return datetime.now().strftime('%Y-%m-%d')


def extract_time(text):
    try:
        m = re.search(r'\b(\d{1,2}:\d{2})\b', text)
        return datetime.strptime(m.group(1), '%H:%M').time() if m else None
    except Exception as e:
        logger.error(f"Time extraction error: {e}")
        return None


def build_timestamp(date_str, time_obj):
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    return datetime.combine(d, time_obj)

