import google.generativeai as genai
from openai import OpenAI
from core.config import Config
from core.logger import logger

class AIHandler:
    def __init__(self):
        self.openai_client = None
        if Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        self.gemini_enabled = False
        if Config.GEMINI_API_KEY and "your_gemini" not in Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_enabled = True
                
                # Dynamically find an available model for the future
                available_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
                
                if available_models:
                    self.gemini_models = available_models
                    logger.info(f"Gemini auto-detected {len(self.gemini_models)} available models.")
                else:
                    self.gemini_models = []
                    logger.warning("No Gemini models found supporting generateContent.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.gemini_enabled = False

    def generate_text(self, prompt, model="gpt-4o-mini", max_tokens=1000):
        # 1. Try OpenAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            except Exception as e:
                err = str(e).lower()
                if "unsupported_country" in err or "403" in err:
                    logger.warning("OpenAI Restricted in your region.")
                else:
                    logger.error(f"OpenAI Error: {e}")

        # 2. Try Gemini with auto-detected models
        if self.gemini_enabled and hasattr(self, 'gemini_models') and self.gemini_models:
            for m_name in self.gemini_models[:5]: # Try up to first 5 valid models
                try:
                    logger.info(f"Trying Gemini model: {m_name}...")
                    m = genai.GenerativeModel(m_name)
                    response = m.generate_content(prompt)
                    if response and hasattr(response, 'text'):
                        logger.info(f"Success with {m_name}")
                        return response.text
                except Exception as e:
                    logger.warning(f"Gemini {m_name} failed: {e}")
                    if "403" in str(e) or "unsupported_country" in str(e).lower():
                        logger.error("Gemini is also restricted in your region. Check VPN.")
                        break
            
        return None

ai_handler = AIHandler()
