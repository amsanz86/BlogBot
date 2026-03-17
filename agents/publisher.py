import json
import os
import shutil
import time
from core.logger import logger
from core.github_pusher import GitHubPusher

class Publisher:
    def __init__(self):
        self.web_data_dir = os.path.join("web", "data")
        self.data_path = os.path.join(self.web_data_dir, "posts.json")
        self.web_img_path = os.path.join(self.web_data_dir, "images")
        
        if not os.path.exists(self.web_data_dir):
            os.makedirs(self.web_data_dir)
        if not os.path.exists(self.web_img_path):
            os.makedirs(self.web_img_path)

    def publish(self, title, content, image_path=None):
        logger.info(f"Publishing to Local Web: {title}")
        
        # 1. Prepare image for web
        web_image_url = ""
        if image_path and os.path.exists(image_path):
            new_name = os.path.basename(image_path)
            dest = os.path.join(self.web_img_path, new_name)
            shutil.copy(image_path, dest)
            web_image_url = f"data/images/{new_name}"
        
        # CRITICAL: If no image after all attempts, do not publish
        if not web_image_url:
            logger.error("No image available for this post. Skipping publication.")
            return None

        # 2. Read existing posts
        posts = []
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    posts = json.load(f)
                # Cleanup: remove anything corrupted or without image
                posts = [p for p in posts if p.get('image') and p.get('title')]
            except Exception as e:
                logger.error(f"Error reading posts.json: {e}")
                posts = []

        # 3. Add new post (at the BEGINNING for reverse chronological order)
        new_post = {
            "title": title,
            "content": content,
            "image": web_image_url,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tag": "Viral"
        }
        posts.insert(0, new_post)

        # 4. Save back to JSON
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            logger.info(f"Article saved to {self.data_path}")
            
            # Auto-Push to GitHub for live deployment
            GitHubPusher.push_changes(f"Viral Post: {title}")
            
            return len(posts)
        except Exception as e:
            logger.error(f"Error saving posts.json: {e}")
            return None
