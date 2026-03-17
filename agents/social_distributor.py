import requests
from core.config import Config
from core.logger import logger

class SocialDistributor:
    def __init__(self):
        self.telegram_token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID

    def share_on_telegram(self, message):
        if not self.telegram_token:
            return
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            requests.post(url, json=payload)
            logger.info("Shared on Telegram.")
        except Exception as e:
            logger.error(f"Error sharing on Telegram: {e}")

    def share_all(self, title, url):
        message = f"🚀 <b>NUEVO ARTÍCULO VIRAL</b>\n\n{title}\n\nLee más aquí: {url}"
        self.share_on_telegram(message)
        logger.info("Social distribution completed.")
        # Templates for others
        # self.share_on_twitter(title, url)
        # self.share_on_pinterest(title, url)
