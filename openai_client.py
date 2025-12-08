from openai import OpenAI
from config import OPENAI_API_KEY, SYSTEM_PROMPT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_newsletter(scraped_items: list, days_since_last_run: int = 5) -> str:
    """Generate newsletter content using OpenAI."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set in environment variables")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Format scraped items for the prompt
    items_text = []
    for item in scraped_items:
        if item.get('success'):
            items_text.append({
                'source': item['url'],
                'content': item['text'][:2000],  # Limit content per source
                'articles': item.get('articles', [])[:5]  # Top 5 articles
            })
    
    user_prompt = f"""Analyze these tech news sources from the past {days_since_last_run} days. Find the 3-4 stories with the deepest strategic implications for someone building a career in business + AI.

SOURCES:

{str(items_text)}

Focus on:

- What's genuinely NEW or SURPRISING (not just incremental updates)

- Stories that reveal competitive dynamics or market shifts

- Developments that create opportunities for students/professionals

- Insights that challenge conventional thinking

Be ruthless: Skip stories that are surface-level or already widely understood."""
    
    try:
        logger.info("Calling OpenAI API to generate newsletter...")
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        newsletter_content = response.choices[0].message.content
        logger.info("Newsletter generated successfully")
        return newsletter_content
    except Exception as e:
        logger.error(f"Error generating newsletter: {str(e)}")
        raise



