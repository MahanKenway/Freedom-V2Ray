from src.core.source_health import SourceHealthManager


def test_source_prioritization(tmp_path):
    manager = SourceHealthManager(state_file=str(tmp_path / "state.json"))
    sources = ["a", "b"]

    manager.record_result("a", had_configs=False)
    manager.record_result("a", had_configs=False)
    manager.record_result("a", had_configs=False)
    manager.record_result("b", had_configs=True)

    prioritized = manager.prioritize(sources)
    assert prioritized[0] == "b"


def test_source_quarantine_fallback(tmp_path):
    manager = SourceHealthManager(
        state_file=str(tmp_path / "state.json"),
        quarantine_failures=1,
        quarantine_seconds=3600,
    )
    sources = ["a"]
    manager.record_result("a", had_configs=False)

    prioritized = manager.prioritize(sources)
    assert prioritized == ["a"]
