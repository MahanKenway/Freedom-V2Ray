from src.core import tester as tester_module
from src.core.tester import ConfigTester
from src.models.config import Config
from src.models.protocol import Protocol


def test_tester_marks_valid(monkeypatch):
    def fake_connect_latency(host, port, timeout, retries):
        return 120

    monkeypatch.setattr(tester_module, "connect_latency", fake_connect_latency)

    tester = ConfigTester(timeout=1.0, retries=1, threshold_ms=500)
    config = Config(
        raw="vless://uuid@example.com:443",
        protocol=Protocol.VLESS,
        host="example.com",
        port=443,
    )
    result = tester.test(config)
    assert result.latency_ms == 120


def test_tester_marks_invalid(monkeypatch):
    def fake_connect_latency(host, port, timeout, retries):
        return 800

    monkeypatch.setattr(tester_module, "connect_latency", fake_connect_latency)

    tester = ConfigTester(timeout=1.0, retries=1, threshold_ms=500)
    config = Config(
        raw="vless://uuid@example.com:443",
        protocol=Protocol.VLESS,
        host="example.com",
        port=443,
    )
    result = tester.test(config)
    assert result.latency_ms is None
