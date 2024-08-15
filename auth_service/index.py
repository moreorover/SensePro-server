import logging
import os
import schedule
from dotenv import load_dotenv
import time

from utils.common import connect_to_keydb
from utils.front_end_api import fetch_session_id

from logging.handlers import TimedRotatingFileHandler

# Set up a timed rotating log handler
timed_handler = TimedRotatingFileHandler(
    "/app/logs/auth_service.log",  # Log file path
    when="midnight",  # Rotate at midnight
    interval=1,  # Rotate every day
    backupCount=7  # Keep up to 7 days of logs
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        timed_handler,  # Timed rotating file handler
        logging.StreamHandler()  # Also log to the console
    ]
)

logging.info("Authentication service is starting...")

keydb_url = os.getenv('KEYDB_URL', 'redis://keydb:6379/0')
r = connect_to_keydb(keydb_url)

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
api_host = os.getenv('API_HOST')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

def fetch_session():
    """Fetch a new session ID every hour."""
    session = fetch_session_id(api_host, email, password)
    if session:
        r.set("session", session)
        logging.info(f"Successfully wrote key session with to KeyDB.")
    else:
        logging.error("Failed to update Session ID.")

def run_scheduler():
    """Run the scheduled tasks in an infinite loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule tasks
    schedule.every(5).seconds.do(fetch_session)  # Update session ID every hour

    # Get the initial session ID
    fetch_session()

    # Start the scheduler loop
    run_scheduler()
