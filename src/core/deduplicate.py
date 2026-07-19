import hashlib
from typing import Iterable, List, Set

from src.models.config import Config
from src.models.normalized import NormalizedConfig


def canonical_key(config: Config | NormalizedConfig) -> str:
    """Build a stable deduplication key without using display fragments."""
    protocol = getattr(config.protocol, "value", str(config.protocol))
    server = getattr(config, "host", None) or getattr(config, "server", "")
    values = [
        protocol.lower(),
        str(server).lower(),
        str(config.port),
        getattr(config, "uuid", None) or "",
        getattr(config, "password", None) or "",
        getattr(config, "method", None) or "",
        getattr(config, "network", None) or "",
        getattr(config, "security", None) or "",
    ]
    return "|".join(values)


def stable_hash(value: str) -> str:
    """Return a deterministic SHA-256 identifier for a canonical value."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def deduplicate_configs(configs: Iterable[Config]) -> List[Config]:
    """Deduplicate parsed configs while preserving the first occurrence order."""
    seen: Set[str] = set()
    unique: List[Config] = []
    for config in configs:
        key_hash = stable_hash(canonical_key(config))
        if key_hash in seen:
            continue
        seen.add(key_hash)
        unique.append(config)
    return unique
