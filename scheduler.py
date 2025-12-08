import schedule
import time
import logging
from datetime import datetime, timedelta
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LAST_RUN_FILE = 'last_run.json'

def get_days_since_last_run() -> int:
    """Get number of days since last newsletter run."""
    if os.path.exists(LAST_RUN_FILE):
        try:
            with open(LAST_RUN_FILE, 'r') as f:
                data = json.load(f)
                last_run = datetime.fromisoformat(data['last_run'])
                days = (datetime.now() - last_run).days
                return max(days, 5)  # Minimum 5 days
        except Exception as e:
            logger.warning(f"Error reading last run file: {e}")
            return 5
    return 5

def update_last_run():
    """Update the last run timestamp."""
    data = {
        'last_run': datetime.now().isoformat()
    }
    with open(LAST_RUN_FILE, 'w') as f:
        json.dump(data, f)
    logger.info(f"Last run updated to {datetime.now().isoformat()}")

def run_newsletter():
    """Main function to run the newsletter generation and sending."""
    from main import generate_and_send_newsletter
    
    try:
        logger.info("Starting newsletter generation...")
        generate_and_send_newsletter()
        update_last_run()
        logger.info("Newsletter process completed successfully")
    except Exception as e:
        logger.error(f"Error in newsletter generation: {str(e)}")
        raise

def start_scheduler():
    """Start the scheduler to run newsletter every 5 days."""
    # Schedule to run every 5 days
    schedule.every(5).days.do(run_newsletter)
    
    logger.info("Scheduler started. Newsletter will run every 5 days.")
    logger.info("First run will be in 5 days, or run manually with: python main.py")
    
    # Run continuously
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour



