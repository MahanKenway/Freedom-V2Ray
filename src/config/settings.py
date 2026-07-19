import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Configuration settings for the collector."""
    max_workers: int
    fetch_timeout: float
    ping_timeout: float
    ping_retries: int
    latency_threshold_ms: int
    source_health_file: str
    source_quarantine_failures: int
    source_quarantine_seconds: int


def load_settings() -> Settings:
    """Load settings from environment variables with defaults."""
    return Settings(
        max_workers=int(os.getenv("MAX_WORKERS", "50")),
        fetch_timeout=float(os.getenv("FETCH_TIMEOUT", "15")),
        ping_timeout=float(os.getenv("PING_TIMEOUT", "1.5")),
        ping_retries=int(os.getenv("PING_RETRIES", "2")),
        latency_threshold_ms=int(os.getenv("LATENCY_THRESHOLD_MS", "1000")),
        source_health_file=os.getenv("SOURCE_HEALTH_FILE", "logs/source_health.json"),
        source_quarantine_failures=int(os.getenv("SOURCE_QUARANTINE_FAILURES", "3")),
        source_quarantine_seconds=int(os.getenv("SOURCE_QUARANTINE_SECONDS", str(12 * 3600))),
    )
