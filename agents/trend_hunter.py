from pytrends.request import TrendReq
from core.config import Config
from core.logger import logger
from core.database import save_trend

class TrendHunter:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def fetch_google_trends(self):
        logger.info("Fetching Google Trends...")
        trends = []
        
        # Method 1: PyTrends (Fragile)
        try:
            geo_code = Config.GEO.upper() if Config.GEO else "US"
            df = self.pytrends.today_searches(pn=geo_code)
            trends = df.tolist()
            if trends:
                logger.info("Fetched trends via PyTrends.")
        except Exception as e:
            logger.warning(f"PyTrends failed: {e}. Trying RSS fallback...")

        # Method 2: RSS Feed (More stable)
        if not trends:
            try:
                import requests
                import xml.etree.ElementTree as ET
                
                # Try Google RSS first
                geo = Config.GEO.upper() if Config.GEO else "US"
                rss_urls = [
                    f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}",
                    "https://www.reddit.com/r/all/hot/.rss", # Global Reddit RSS
                    "http://feeds.bbci.co.uk/news/rss.xml" # Global News
                ]
                
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                
                for url in rss_urls:
                    logger.info(f"Trying RSS source: {url}")
                    try:
                        response = requests.get(url, headers=headers, timeout=10)
                        if response.status_code == 200:
                            root = ET.fromstring(response.content)
                            # Handle both standard RSS and Atom (Reddit uses Atom)
                            items = root.findall('.//{http://www.w3.org/2005/Atom}entry') or root.findall('.//item')
                            for item in items:
                                title_elem = item.find('{http://www.w3.org/2005/Atom}title') or item.find('title')
                                if title_elem is not None and title_elem.text:
                                    trends.append(title_elem.text)
                            
                            if len(trends) > 5:
                                logger.info(f"Successfully fetched {len(trends)} trends from {url}")
                                break
                    except Exception as e:
                        logger.warning(f"Failed to fetch RSS from {url}: {e}")

                if not trends:
                    logger.warning("All RSS sources failed.")
            except Exception as e:
                logger.error(f"RSS Discovery failed: {e}")

        for t in trends:
            save_trend(t, "Google Trends", 0.8)
        return trends

    def fetch_reddit_trends(self):
        logger.info("Fetching Reddit trends via JSON (No API Key Required)...")
        trends = []
        try:
            import requests
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) auto_viral_blog_v1"}
            url = "https://www.reddit.com/r/all/hot.json?limit=25"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for post in data.get("data", {}).get("children", []):
                    post_data = post.get("data", {})
                    title = post_data.get("title")
                    score = post_data.get("score", 0)
                    
                    if title and score > 5000:
                        save_trend(title, "Reddit (JSON)", 0.7)
                        trends.append(title)
                return trends
            else:
                logger.error(f"Failed to fetch Reddit JSON. Status: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error fetching Reddit via JSON: {e}")
            return []

    def hunt(self):
        g_trends = self.fetch_google_trends()
        r_trends = self.fetch_reddit_trends()
        
        total_found = g_trends + r_trends
        
        # Fallback Evergreen Trends if APIs fail
        if not total_found:
            logger.warning("APIs failed. Using evergreen viral fallback trends.")
            total_found = [
                "10 Life Hacks That Will Change Your Daily Routine Forever",
                "New AI Tools That Are Secretly Replacing High-Paying Jobs in 2026",
                "How to Earn Passive Income in 2026: The Ultimate Guide",
                "The Productivity Secrets of Successful CEOs Revealed",
                "Why 8 Hours of Sleep is the Ultimate Performance Enhancer (Scientific Facts)"
            ]
            for t in total_found:
                save_trend(t, "Fallback", 0.5)

        logger.info(f"Trend Hunter found {len(total_found)} potential trends.")
        return total_found
