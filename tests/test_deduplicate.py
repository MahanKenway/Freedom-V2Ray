from src.core.deduplicate import canonical_key, deduplicate_configs, stable_hash
from src.models.config import Config
from src.models.protocol import Protocol


def test_canonical_key_normalizes_host_case():
    first = Config(raw="a", protocol=Protocol.VLESS, host="Example.COM", port=443)
    second = Config(raw="b", protocol=Protocol.VLESS, host="example.com", port=443)

    assert canonical_key(first) == canonical_key(second)


def test_deduplicate_configs_preserves_first_occurrence():
    first = Config(raw="first", protocol=Protocol.VLESS, host="Example.COM", port=443)
    second = Config(raw="second", protocol=Protocol.VLESS, host="example.com", port=443)

    result = deduplicate_configs([first, second])

    assert result == [first]


def test_stable_hash_is_deterministic():
    assert stable_hash("vless|example.com|443") == stable_hash("vless|example.com|443")
