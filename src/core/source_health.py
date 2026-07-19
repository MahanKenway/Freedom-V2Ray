import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class SourceHealthManager:
    """Tracks source reliability and provides prioritized source lists."""

    state_file: str = "logs/source_health.json"
    quarantine_failures: int = 3
    quarantine_seconds: int = 12 * 3600

    def _load_state(self) -> Dict[str, Dict[str, float]]:
        path = Path(self.state_file)
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to read source health state: %s", exc)
            return {}

    def _save_state(self, state: Dict[str, Dict[str, float]]) -> None:
        path = Path(self.state_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def prioritize(self, sources: Iterable[str]) -> List[str]:
        """Return sources sorted by health score while skipping quarantined entries."""
        state = self._load_state()
        now = int(time.time())

        ranked: List[tuple[float, str]] = []
        quarantined: List[str] = []

        for source in sources:
            entry = state.get(source, {})
            quarantined_until = int(entry.get("quarantined_until", 0))
            if quarantined_until > now:
                quarantined.append(source)
                continue

            successes = float(entry.get("successes", 0))
            failures = float(entry.get("failures", 0))
            total = successes + failures
            score = (successes / total) if total else 0.5
            ranked.append((score, source))

        ranked.sort(key=lambda item: item[0], reverse=True)
        prioritized = [source for _, source in ranked]

        if not prioritized and quarantined:
            logger.warning("All sources quarantined; using them anyway as fallback")
            return list(sources)

        return prioritized

    def record_result(self, source: str, had_configs: bool) -> None:
        """Persist per-source success/failure outcomes."""
        now = int(time.time())
        state = self._load_state()
        entry = state.get(
            source,
            {
                "successes": 0,
                "failures": 0,
                "consecutive_failures": 0,
                "last_success": 0,
                "last_failure": 0,
                "quarantined_until": 0,
            },
        )

        if had_configs:
            entry["successes"] = int(entry.get("successes", 0)) + 1
            entry["consecutive_failures"] = 0
            entry["last_success"] = now
            entry["quarantined_until"] = 0
        else:
            entry["failures"] = int(entry.get("failures", 0)) + 1
            entry["consecutive_failures"] = int(entry.get("consecutive_failures", 0)) + 1
            entry["last_failure"] = now
            if entry["consecutive_failures"] >= self.quarantine_failures:
                entry["quarantined_until"] = now + self.quarantine_seconds

        state[source] = entry
        self._save_state(state)
