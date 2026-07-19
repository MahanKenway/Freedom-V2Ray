import ipaddress
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.models.config import Config
from src.models.normalized import NormalizedConfig, ValidationStatus


class ValidationErrorCode(str, Enum):
    EMPTY_HOST = "empty_host"
    INVALID_PORT = "invalid_port"
    PRIVATE_HOST = "private_host"


@dataclass(frozen=True)
class StaticValidationResult:
    """Result of validation that never performs network I/O."""

    status: ValidationStatus
    error_code: Optional[ValidationErrorCode] = None
    error_message: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.status == ValidationStatus.VALID


def _is_blocked_ip(host: str) -> bool:
    try:
        address = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        return False
    return (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    )


def validate_static(config: Config | NormalizedConfig) -> StaticValidationResult:
    """Validate basic fields without DNS, sockets, HTTP, or subprocess calls."""
    host = getattr(config, "host", None) or getattr(config, "server", None)
    port = getattr(config, "port", None)

    if not host or not str(host).strip():
        return StaticValidationResult(
            status=ValidationStatus.INVALID,
            error_code=ValidationErrorCode.EMPTY_HOST,
            error_message="Host/server is empty.",
        )

    if not isinstance(port, int) or not 1 <= port <= 65535:
        return StaticValidationResult(
            status=ValidationStatus.INVALID,
            error_code=ValidationErrorCode.INVALID_PORT,
            error_message="Port must be an integer between 1 and 65535.",
        )

    if _is_blocked_ip(str(host)):
        return StaticValidationResult(
            status=ValidationStatus.INVALID,
            error_code=ValidationErrorCode.PRIVATE_HOST,
            error_message="Private, loopback, link-local, or reserved IPs are blocked.",
        )

    return StaticValidationResult(status=ValidationStatus.VALID)
