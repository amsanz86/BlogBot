from openai import OpenAI
from core.config import Config
from core.logger import logger
import requests
import os

class ImageCreator:
    def __init__(self):
        # Pollinations image generation API
        self.base_url = "https://image.pollinations.ai/prompt/"

    def create_image(self, prompt):
        logger.info(f"Generating FREE image with Pollinations.ai...")
        try:
            # Clean prompt for URL
            encoded_prompt = requests.utils.quote(prompt)
            image_url = f"{self.base_url}{encoded_prompt}?width=1024&height=1024&seed={os.urandom(4).hex()}&model=flux"
            
            # Download image locally
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                img_data = response.content
                filename = f"image_{os.urandom(4).hex()}.png"
                path = os.path.join("data", filename)
                with open(path, 'wb') as handler:
                    handler.write(img_data)
                    
                logger.info(f"Free image saved to {path}")
                return path
            else:
                logger.warning(f"Pollinations failed ({response.status_code}). Trying Unsplash Fallback...")
                fallback_url = f"https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1024&q=80"
                return self._download_fallback(fallback_url)
        except Exception as e:
            logger.error(f"Error creating free image: {e}. Trying Unsplash Fallback...")
            # Unsplash fallback for reliability
            fallback_url = f"https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1024&q=80"
            return self._download_fallback(fallback_url)

    def _download_fallback(self, url):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                filename = f"image_fallback_{os.urandom(4).hex()}.png"
                path = os.path.join("data", filename)
                with open(path, 'wb') as handler:
                    handler.write(response.content)
                logger.info(f"Fallback image saved to {path}")
                return path
        except:
            return None
