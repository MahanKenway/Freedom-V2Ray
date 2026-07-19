from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from src.models.protocol import Protocol


class ValidationStatus(str, Enum):
    """Validation states that separate syntax, reachability, and runtime errors."""

    VALID = "valid"
    INVALID = "invalid"
    TIMEOUT = "timeout"
    UNREACHABLE = "unreachable"
    RATE_LIMITED = "rate_limited"
    NOT_TESTED = "not_tested"


@dataclass(frozen=True)
class ConfigMetadata:
    """Non-sensitive metadata for a normalized configuration."""

    source_id: str
    raw_hash: str
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    checked_at: Optional[datetime] = None
    latency_ms: Optional[int] = None
    validation_status: ValidationStatus = ValidationStatus.NOT_TESTED


@dataclass(frozen=True)
class NormalizedConfig:
    """Normalized, side-effect-free representation of a proxy config."""

    protocol: Protocol
    server: str
    port: int
    metadata: ConfigMetadata
    uuid: Optional[str] = None
    password: Optional[str] = None
    method: Optional[str] = None
    network: Optional[str] = None
    security: Optional[str] = None
    name: Optional[str] = None
