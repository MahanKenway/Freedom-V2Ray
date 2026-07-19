import json
import re
from typing import Optional
from urllib.parse import urlparse

from src.models.config import Config
from src.models.protocol import Protocol
from src.utils.encoding import decode_base64
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ConfigParser:
    """Parses V2Ray configuration strings."""

    @staticmethod
    def parse(config_str: str) -> Optional[Config]:
        """Parse a config string and return Config object."""
        try:
            if config_str.startswith("vmess://"):
                return ConfigParser._parse_vmess(config_str)
            if config_str.startswith("vless://"):
                return ConfigParser._parse_standard(config_str, Protocol.VLESS)
            if config_str.startswith("trojan://"):
                return ConfigParser._parse_standard(config_str, Protocol.TROJAN)
            if config_str.startswith("ss://"):
                return ConfigParser._parse_shadowsocks(config_str)
        except (ValueError, json.JSONDecodeError) as exc:
            logger.warning("Failed to parse config: %s", exc)
        return None

    @staticmethod
    def _parse_vmess(config: str) -> Optional[Config]:
        payload = decode_base64(config[8:])
        if not payload:
            return None
        data = json.loads(payload)
        host = data.get("add")
        port = data.get("port")
        if not host or not port:
            return None
        return Config(
            raw=config,
            protocol=Protocol.VMESS,
            host=str(host),
            port=int(port),
        )

    @staticmethod
    def _parse_standard(config: str, protocol: Protocol) -> Optional[Config]:
        parsed = urlparse(config)
        if not parsed.hostname or not parsed.port:
            return None
        return Config(
            raw=config,
            protocol=protocol,
            host=parsed.hostname,
            port=parsed.port,
        )

    @staticmethod
    def _parse_shadowsocks(config: str) -> Optional[Config]:
        data = config[5:]
        data = data.split("#", 1)[0]
        if "@" not in data:
            decoded = decode_base64(data)
            if not decoded:
                return None
            data = decoded
        data = data.split("?", 1)[0]
        match = re.search(r"@([^:/]+):(\d+)$", data)
        if not match:
            return None
        return Config(
            raw=config,
            protocol=Protocol.SHADOWSOCKS,
            host=match.group(1),
            port=int(match.group(2)),
        )
