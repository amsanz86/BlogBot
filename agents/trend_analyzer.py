from core.ai_handler import ai_handler
from core.logger import logger

class TrendAnalyzer:
    def analyze(self, trends):
        logger.info(f"Analyzing {len(trends)} trends for viral potential...")
        prompt = f"""
        Analyze the following trends and pick the ONE with the highest viral potential and SEO traffic capability for a general interest blog.
        Return ONLY the name of the trend.
        
        Trends:
        {chr(10).join(trends)}
        """
        
        try:
            choice = ai_handler.generate_text(prompt, max_tokens=50)
            if choice:
                choice = choice.strip()
                logger.info(f"Analyzer selected: {choice}")
                return choice
            return trends[0] if trends else None
        except Exception as e:
            logger.error(f"Error in Trend Analysis: {e}")
            return trends[0] if trends else None
