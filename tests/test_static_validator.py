from src.core.static_validator import ValidationErrorCode, validate_static
from src.models.config import Config
from src.models.normalized import ValidationStatus
from src.models.protocol import Protocol


def test_static_validator_accepts_public_host():
    config = Config(
        raw="vless://uuid@example.com:443",
        protocol=Protocol.VLESS,
        host="example.com",
        port=443,
    )

    result = validate_static(config)

    assert result.ok
    assert result.status == ValidationStatus.VALID


def test_static_validator_rejects_invalid_port():
    config = Config(
        raw="vless://uuid@example.com:99999",
        protocol=Protocol.VLESS,
        host="example.com",
        port=99999,
    )

    result = validate_static(config)

    assert not result.ok
    assert result.error_code == ValidationErrorCode.INVALID_PORT


def test_static_validator_rejects_private_ip():
    config = Config(
        raw="vless://uuid@127.0.0.1:443",
        protocol=Protocol.VLESS,
        host="127.0.0.1",
        port=443,
    )

    result = validate_static(config)

    assert not result.ok
    assert result.error_code == ValidationErrorCode.PRIVATE_HOST
