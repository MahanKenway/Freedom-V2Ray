import base64
from typing import Optional


def decode_base64(data: str) -> Optional[str]:
    """Decode base64 data, supporting urlsafe and missing padding."""
    cleaned = data.strip()
    if not cleaned:
        return None
    cleaned += "=" * (-len(cleaned) % 4)
    for decoder in (base64.urlsafe_b64decode, base64.b64decode):
        try:
            return decoder(cleaned).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            continue
    return None
