import base64
from pathlib import Path
from typing import Dict, List

from src.models.config import Config
from src.models.protocol import Protocol
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ConfigExporter:
    """Exports configs to files."""

    def __init__(self, output_dir: str = "configs") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export(self, categories: Dict[Protocol, List[Config]]) -> None:
        """Export configs to raw and base64 files."""
        for protocol, configs in categories.items():
            raw_file = self.output_dir / f"{protocol.value}.txt"
            raw_content = "\n".join([config.raw for config in configs])
            raw_file.write_text(raw_content, encoding="utf-8")

            sub_file = self.output_dir / f"{protocol.value}_sub.txt"
            encoded = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")
            sub_file.write_text(encoded, encoding="utf-8")

            logger.info("Exported %s configs for %s", len(configs), protocol.value)
