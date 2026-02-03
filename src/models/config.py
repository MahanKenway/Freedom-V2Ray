from dataclasses import dataclass
from typing import Optional

from src.models.protocol import Protocol


@dataclass
class Config:
    """Represents a V2Ray configuration."""
    raw: str
    protocol: Protocol
    host: str
    port: int
    latency_ms: Optional[int] = None

    @property
    def is_valid(self) -> bool:
        return self.latency_ms is not None
