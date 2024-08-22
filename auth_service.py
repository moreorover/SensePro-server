import logging
import os
import schedule
from dotenv import load_dotenv
import time

from utils.redis_client import RedisClient
from utils.retry import retry
from utils.front_end_api import fetch_session_id

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logging.info("Authentication service is starting...")

# Load environment variables from the .env file
load_dotenv()

keydb_host = os.getenv('KEYDB_HOST')
keydb_port = os.getenv('KEYDB_PORT')
keydb_database = os.getenv('KEYDB_DATABASE')
api_host = os.getenv('API_HOST')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

r: RedisClient = RedisClient(host=keydb_host, port=keydb_port, db=keydb_database)

@retry(retries=3, delay=15)
def fetch_session():
    """Fetch a new session ID with retries on failure."""
    session = fetch_session_id(api_host, email, password)
    if session:
        r.save_object("session", session)
        logging.info("Successfully wrote key session to KeyDB.")
    else:
        logging.error("Failed to update Session ID.")

def run_scheduler():
    """Run the scheduled tasks in an infinite loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule tasks
    schedule.every(5).seconds.do(fetch_session)  # Schedule session update

    # Get the initial session ID
    fetch_session()

    # Start the scheduler loop
    run_scheduler()
