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
                logger.error(f"Pollinations error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error creating free image: {e}")
            return None
