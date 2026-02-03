import socket
import time
from typing import Iterable, Optional

from src.models.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def resolve_host(host: str, port: int) -> Iterable[tuple[int, tuple]]:
    """Resolve host to addresses for TCP connection attempts."""
    try:
        return [
            (family, sockaddr)
            for family, _, _, _, sockaddr in socket.getaddrinfo(
                host, port, type=socket.SOCK_STREAM
            )
        ]
    except socket.gaierror:
        return []


def connect_latency(
    host: str, port: int, timeout: float, retries: int
) -> Optional[int]:
    """Return TCP connection latency in ms or None if unreachable."""
    addresses = resolve_host(host, port)
    if not addresses:
        return None
    for _ in range(retries + 1):
        for family, sockaddr in addresses:
            start_time = time.perf_counter()
            try:
                with socket.socket(family, socket.SOCK_STREAM) as sock:
                    sock.settimeout(timeout)
                    sock.connect(sockaddr)
                end_time = time.perf_counter()
                return int((end_time - start_time) * 1000)
            except (socket.timeout, OSError) as exc:
                logger.debug("Connection attempt failed: %s", exc)
                continue
    return None


class ConfigTester:
    """Tests V2Ray configurations for connectivity."""

    def __init__(self, timeout: float, retries: int, threshold_ms: int) -> None:
        self.timeout = timeout
        self.retries = retries
        self.threshold_ms = threshold_ms

    def test(self, config: Config) -> Config:
        """Test a single config and return with latency if valid."""
        latency = connect_latency(
            config.host, config.port, self.timeout, self.retries
        )
        if latency is not None and latency < self.threshold_ms:
            config.latency_ms = latency
        return config
