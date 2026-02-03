from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Iterable, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.core.parser import ConfigParser
from src.core.tester import ConfigTester
from src.models.config import Config
from src.models.protocol import Protocol
from src.utils.encoding import decode_base64
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ConfigCollector:
    """Main collector class."""

    def __init__(
        self,
        sources: Iterable[str],
        tester: ConfigTester,
        max_workers: int,
        fetch_timeout: float,
    ) -> None:
        self.sources = list(sources)
        self.tester = tester
        self.max_workers = max_workers
        self.fetch_timeout = fetch_timeout
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def fetch_source(self, url: str) -> List[str]:
        """Fetch configs from a single source."""
        configs: List[str] = []
        try:
            response = self.session.get(url, timeout=self.fetch_timeout)
            response.raise_for_status()
            content = response.text
            if "://" not in content[:100]:
                decoded = decode_base64(content)
                if decoded:
                    content = decoded
            for line in content.splitlines():
                line = line.strip()
                if "://" in line:
                    configs.append(line)
        except requests.RequestException as exc:
            logger.warning("Failed to fetch %s: %s", url, exc)
        return configs

    def collect(self) -> Dict[Protocol, List[Config]]:
        """Collect, parse, and test all configs."""
        all_configs: List[str] = []
        for source in self.sources:
            configs = self.fetch_source(source)
            logger.info("Fetched %s configs from %s", len(configs), source)
            all_configs.extend(configs)

        unique_configs = sorted(
            {config for config in all_configs if config.strip()}
        )
        parsed_configs: List[Config] = []
        for raw in unique_configs:
            config = ConfigParser.parse(raw)
            if config:
                parsed_configs.append(config)

        valid_configs: List[Config] = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for config in executor.map(self.tester.test, parsed_configs):
                if config.is_valid:
                    valid_configs.append(config)

        categories: Dict[Protocol, List[Config]] = {
            Protocol.VLESS: [],
            Protocol.VMESS: [],
            Protocol.TROJAN: [],
            Protocol.SHADOWSOCKS: [],
            Protocol.MIX: list(valid_configs),
        }
        for config in valid_configs:
            categories[config.protocol].append(config)

        logger.info("Valid configs: %s", len(valid_configs))
        return categories
