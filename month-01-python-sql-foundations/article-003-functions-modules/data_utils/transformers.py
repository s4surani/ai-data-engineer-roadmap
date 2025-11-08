# data_utils/transformers.py

import re
from datetime import datetime
from typing import Optional

def clean_text(text: str) -> str:
    """Remove special characters, lowercase."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower()

def normalize_phone(phone: str) -> Optional[str]:
    """Standardize phone format to +91-XXXXXXXXXX (India example)."""
    digits = re.sub(r'\D', '', str(phone))
    if len(digits) == 10:
        return f'+91-{digits}'
    elif len(digits) == 12 and digits.startswith('91'):
        return f'+91-{digits[2:]}'
    return None

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse various date formats to datetime object."""
    if not isinstance(date_str, str):
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%b %d, %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except Exception:
            continue
    return None

def extract_domain(email: str) -> Optional[str]:
    """Extract domain portion from an email address."""
    match = re.search(r'@([\w\.-]+)', str(email))
    return match.group(1) if match else None
