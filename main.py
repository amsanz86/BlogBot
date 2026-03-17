import time
import schedule
import argparse
from core.logger import logger
from core.database import init_db, save_article, mark_trend_processed
from agents.trend_hunter import TrendHunter
from agents.trend_analyzer import TrendAnalyzer
from agents.content_writer import ContentWriter
from agents.image_creator import ImageCreator
from agents.publisher import Publisher
from agents.social_distributor import SocialDistributor
from agents.growth_analyst import GrowthAnalyst
import re
import unicodedata

# Initialize agents
hunter = TrendHunter()
analyzer = TrendAnalyzer()
writer = ContentWriter()
imager = ImageCreator()
publisher = Publisher()
distributor = SocialDistributor()
growth = GrowthAnalyst()

def create_slug(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).lower().strip()
    return re.sub(r'[-\s]+', '-', text)

def run_engine():
    logger.info("=== AUTO VIRAL BLOG ENGINE STARTING ===")
    
    # 1. Hunt Trends
    trends = hunter.hunt()
    if not trends:
        logger.warning("No trends found. Sleeping.")
        return

    # 2. Analyze and Select
    best_trend = analyzer.analyze(trends)
    if not best_trend:
        logger.warning("Analyzer could not select a trend.")
        return

    # 3. Write Content
    article_data = writer.write_article(best_trend)
    if not article_data:
        logger.error("Content generation failed.")
        return

    # 4. Create Image
    image_path = imager.create_image(article_data['image_prompt'])
    if not image_path:
        logger.error("Image generation failed. Aborting publication to maintain quality.")
        return

    # 5. Publish to Local Web
    post_id = publisher.publish(article_data['title'], article_data['content'], image_path)

    # 6. Save to DB
    if post_id:
        save_article(best_trend, article_data['title'], article_data['content'], image_path, post_id)
        mark_trend_processed(best_trend)
        
        # 7. Social Distribution
        slug = create_slug(article_data['title'])
        post_url = f"https://amsanz86.github.io/BlogBot/web/#{slug}" 
        distributor.share_all(article_data['title'], post_url)

    # 8. Growth Analysis
    growth.analyze_performance()
    
    logger.info("=== JOB COMPLETED SUCCESSFULLY ===")

def main():
    parser = argparse.ArgumentParser(description="Auto Viral Blog Engine")
    parser.add_argument("--now", action="store_true", help="Ejecutar una publicación inmediatamente.")
    args = parser.parse_args()

    init_db()
    
    # Schedule: Every 8 hours at viral peaks
    def safe_run():
        try:
            run_engine()
        except Exception as e:
            logger.error(f"Scheduled run failed: {e}")

    if args.now:
        logger.info("Ejecutando publicación inmediata (--now)...")
        safe_run()

    schedule.every().day.at("11:00").do(safe_run)
    schedule.every().day.at("19:00").do(safe_run)
    schedule.every().day.at("01:00").do(safe_run)
    
    logger.info("Scheduler iniciado. Tareas programadas: 11:00, 19:00, 01:00.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
