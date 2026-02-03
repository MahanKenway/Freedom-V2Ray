import os
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config.settings import load_settings
from src.config.sources import SOURCES
from src.core.collector import ConfigCollector
from src.core.exporter import ConfigExporter
from src.core.notifier import TelegramNotifier
from src.core.tester import ConfigTester
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main() -> None:
    """Main entry point."""
    settings = load_settings()
    tester = ConfigTester(
        timeout=settings.ping_timeout,
        retries=settings.ping_retries,
        threshold_ms=settings.latency_threshold_ms,
    )
    collector = ConfigCollector(
        sources=SOURCES,
        tester=tester,
        max_workers=settings.max_workers,
        fetch_timeout=settings.fetch_timeout,
    )
    exporter = ConfigExporter()
    notifier = TelegramNotifier(
        token=os.environ.get("TELEGRAM_TOKEN"),
        chat_id=os.environ.get("TELEGRAM_CHAT_ID"),
    )

    categories = collector.collect()
    exporter.export(categories)
    notifier.send(categories)
    logger.info("Collection completed")


if __name__ == "__main__":
    main()
