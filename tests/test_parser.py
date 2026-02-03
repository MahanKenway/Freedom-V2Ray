import base64
import json

from src.core.parser import ConfigParser
from src.models.protocol import Protocol


def test_parse_vless():
    config_str = "vless://uuid@example.com:443?security=tls#name"
    result = ConfigParser.parse(config_str)
    assert result is not None
    assert result.protocol == Protocol.VLESS
    assert result.host == "example.com"
    assert result.port == 443


def test_parse_vmess():
    vmess_data = {"add": "example.com", "port": "443", "id": "uuid"}
    encoded = base64.b64encode(json.dumps(vmess_data).encode()).decode()
    config_str = f"vmess://{encoded}"

    result = ConfigParser.parse(config_str)
    assert result is not None
    assert result.protocol == Protocol.VMESS
    assert result.host == "example.com"


def test_parse_shadowsocks():
    config_str = "ss://cipher:password@example.com:443#name"
    result = ConfigParser.parse(config_str)
    assert result is not None
    assert result.protocol == Protocol.SHADOWSOCKS
    assert result.host == "example.com"
    assert result.port == 443
