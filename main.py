#!/usr/bin/env python3
"""
MBT Newsletter Generator
Generates and sends a curated tech newsletter every 5 days.
"""

import logging
from scraper import scrape_all_sources
from config import NEWS_SOURCES, GEMINI_API_KEY, OPENAI_API_KEY

# Prefer Gemini if key set; fall back to OpenAI when all Gemini models 404 (if OPENAI_API_KEY set)
if GEMINI_API_KEY:
    from gemini_client import generate_newsletter as _gemini_generate
else:
    from openai_client import generate_newsletter as _gemini_generate  # only OpenAI path

from email_sender import send_email
from scheduler import get_days_since_last_run
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_and_send_newsletter(test_mode: bool = False):
    """Main function to generate and send newsletter.
    
    Args:
        test_mode: If True, generates newsletter but doesn't send email
    """
    try:
        # Step 1: Scrape all news sources
        logger.info("Step 1: Scraping news sources...")
        try:
            scraped_items = scrape_all_sources(NEWS_SOURCES)
        except Exception as e:
            logger.error("Scraping failed: %s", e)
            raise RuntimeError(f"Scraping failed: {e}") from e
        
        successful_items = [item for item in scraped_items if item.get('success')]
        logger.info("Successfully scraped %d/%d sources", len(successful_items), len(NEWS_SOURCES))
        
        if not successful_items:
            raise RuntimeError(
                "Failed to scrape any news sources. Check network and that source URLs are reachable."
            )
        
        # Step 2: Generate newsletter content
        logger.info("Step 2: Generating newsletter content with AI...")
        days_since_last_run = get_days_since_last_run()
        try:
            newsletter_content = _gemini_generate(successful_items, days_since_last_run)
        except (RuntimeError, ValueError, Exception) as e:
            if GEMINI_API_KEY and OPENAI_API_KEY:
                logger.warning("Gemini failed (%s), falling back to OpenAI...", type(e).__name__)
                from openai_client import generate_newsletter as openai_generate
                newsletter_content = openai_generate(successful_items, days_since_last_run)
            else:
                logger.error("AI generation failed: %s", e)
                raise RuntimeError(f"AI generation failed: {e}") from e
        
        if not newsletter_content or not newsletter_content.strip():
            raise RuntimeError("AI returned empty newsletter content.")
        
        if test_mode:
            logger.info("TEST MODE: Newsletter generated but not sent.")
            logger.info("=" * 80)
            logger.info(newsletter_content)
            logger.info("=" * 80)
            return newsletter_content
        
        # Step 3: Send email
        logger.info("Step 3: Sending newsletter via email...")
        subject = f"MBT Newsletter - {datetime.now().strftime('%B %d, %Y')}"
        try:
            send_email(newsletter_content, subject)
        except Exception as e:
            logger.error("Email send failed: %s", e)
            raise RuntimeError(f"Email send failed: {e}") from e
        
        logger.info("Newsletter generation and sending completed successfully!")
        return newsletter_content
        
    except (ValueError, RuntimeError):
        raise
    except Exception as e:
        logger.exception("Unexpected error in newsletter pipeline: %s", e)
        raise RuntimeError(f"Newsletter failed: {e}") from e

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--schedule':
            # Run as scheduled service
            from scheduler import start_scheduler
            start_scheduler()
        elif sys.argv[1] == '--test':
            # Test mode: generate but don't send
            generate_and_send_newsletter(test_mode=True)
        else:
            print("Usage:")
            print("  python main.py          - Run once and send email")
            print("  python main.py --test   - Generate newsletter without sending")
            print("  python main.py --schedule - Run as scheduled service (every 5 days)")
    else:
        # Run once immediately
        generate_and_send_newsletter()

