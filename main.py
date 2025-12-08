#!/usr/bin/env python3
"""
MBT Newsletter Generator
Generates and sends a curated tech newsletter every 5 days.
"""

import logging
from scraper import scrape_all_sources
from openai_client import generate_newsletter
from email_sender import send_email
from config import NEWS_SOURCES
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
        scraped_items = scrape_all_sources(NEWS_SOURCES)
        
        # Filter successful scrapes
        successful_items = [item for item in scraped_items if item.get('success')]
        logger.info(f"Successfully scraped {len(successful_items)}/{len(NEWS_SOURCES)} sources")
        
        if not successful_items:
            raise Exception("Failed to scrape any news sources")
        
        # Step 2: Generate newsletter content
        logger.info("Step 2: Generating newsletter content with OpenAI...")
        days_since_last_run = get_days_since_last_run()
        newsletter_content = generate_newsletter(successful_items, days_since_last_run)
        
        if test_mode:
            logger.info("TEST MODE: Newsletter generated but not sent.")
            logger.info("=" * 80)
            logger.info(newsletter_content)
            logger.info("=" * 80)
            return newsletter_content
        
        # Step 3: Send email
        logger.info("Step 3: Sending newsletter via email...")
        subject = f"MBT Newsletter - {datetime.now().strftime('%B %d, %Y')}"
        send_email(newsletter_content, subject)
        
        logger.info("Newsletter generation and sending completed successfully!")
        return newsletter_content
        
    except Exception as e:
        logger.error(f"Error in newsletter generation: {str(e)}")
        raise

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

