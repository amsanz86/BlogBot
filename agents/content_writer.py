from core.ai_handler import ai_handler
from core.logger import logger

class ContentWriter:
    def write_article(self, trend):
        logger.info(f"Generating article for trend: {trend}")
        prompt = f"""
        Write a viral, SEO-optimized blog article about the following trend: {trend}.
        
        The article must follow this structure:
        1. Clickbait but accurate Title
        2. Introduction (hook the reader)
        3. Detailed explanation of the trend
        4. Why it went viral
        5. Impact on the internet/world
        6. Conclusion
        
        Use HTML tags for formatting (h2, p, strong).
        Language: Spanish (or same as trend) - Default to Spanish for this blog.
        
        Return the response in this format:
        TITLE: [The Title]
        CONTENT: [The HTML Content]
        IMAGE_PROMPT: [A descriptive prompt to generate a 16:9 cinematic image for this article]
        """
        
        try:
            raw_text = ai_handler.generate_text(prompt, max_tokens=2000)
            if not raw_text:
                return None
            
            # Robust parsing
            title = "Tendencia Viral Hoy"
            content = "<p>No se pudo generar el contenido.</p>"
            image_prompt = trend
            
            if "TITLE:" in raw_text:
                parts = raw_text.split("TITLE:")[1].split("CONTENT:")
                title = parts[0].strip()
                if len(parts) > 1:
                    c_parts = parts[1].split("IMAGE_PROMPT:")
                    content = c_parts[0].strip()
                    
                    # Clean up markdown code blocks if present
                    if content.startswith("```"):
                        content = content.split("\n", 1)[-1] # Remove first line like ```html
                        if content.endswith("```"):
                            content = content.rsplit("```", 1)[0]
                    content = content.strip()
                    
                    if len(c_parts) > 1:
                        image_prompt = c_parts[1].strip()
            
            return {
                "title": title,
                "content": content,
                "image_prompt": image_prompt
            }
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return None
