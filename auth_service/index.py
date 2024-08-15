import logging
import os
import schedule
from dotenv import load_dotenv
import time

from utils.common import connect_to_keydb
from utils.front_end_api import fetch_session_id

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/app/logs/auth_service.log"),  # Log to a file named 'service1.log'
        logging.StreamHandler()          # Also log to the console
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

logging.info(f"api_host -> {api_host}")
logging.info(f"email -> {email}")
logging.info(f"password -> {password}")

def update_session_id():
    """Fetch a new session ID every hour."""
    global session
    session = fetch_session_id(api_host, email, password)
    if session:
        logging.info("Session ID updated successfully.")
    else:
        logging.error("Failed to update Session ID.")

def run_scheduler():
    """Run the scheduled tasks in an infinite loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule tasks
    schedule.every(5).seconds.do(update_session_id)  # Update session ID every hour
    # schedule.every(2).seconds.do(fetch_controller_id)  # Fetch controller ID every minute

    # Get the initial session ID
    update_session_id()

    # Start the scheduler loop
    run_scheduler()
