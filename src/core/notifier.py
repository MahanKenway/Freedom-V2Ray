from typing import Dict, List, Optional

import requests

from src.models.config import Config
from src.models.protocol import Protocol
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramNotifier:
    """Sends notifications to Telegram."""

    def __init__(self, token: Optional[str], chat_id: Optional[str]) -> None:
        self.token = token
        self.chat_id = chat_id
        self.enabled = bool(token and chat_id)

    def send(self, categories: Dict[Protocol, List[Config]]) -> None:
        """Send notification to Telegram."""
        if not self.enabled:
            logger.info("Telegram notification disabled")
            return

        message = self._format_message(categories)
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Telegram notification sent")
        except requests.RequestException as exc:
            logger.warning("Failed to send Telegram notification: %s", exc)

    @staticmethod
    def _format_message(categories: Dict[Protocol, List[Config]]) -> str:
        mix_count = len(categories[Protocol.MIX])
        return (
            "🚀 *Freedom V2Ray Updated!*\n\n"
            f"✅ High-Speed Configs: `{mix_count}`\n"
            f"🔹 VLESS: `{len(categories[Protocol.VLESS])}`\n"
            f"🔹 VMESS: `{len(categories[Protocol.VMESS])}`\n"
            f"🔹 Trojan: `{len(categories[Protocol.TROJAN])}`\n"
            f"🔹 Shadowsocks: `{len(categories[Protocol.SHADOWSOCKS])}`\n\n"
            "⏱ Update Interval: `2 Hours`\n"
            "🌐 [View on GitHub](https://github.com/MahanKenway/Freedom-V2Ray)"
        )
