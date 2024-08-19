import logging
import os
import schedule
from dotenv import load_dotenv
import time
import json

from utils.network import get_mac_address_eth0
from utils.retry import retry
from utils.common import connect_to_keydb
from utils.front_end_api import fetch_controller

from logging.handlers import TimedRotatingFileHandler

# Set up a timed rotating log handler
timed_handler = TimedRotatingFileHandler(
    "/app/logs/controller_service.log",  # Log file path
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

logging.info("Controller service is starting...")

# Load environment variables from the .env file
load_dotenv()

keydb_url = os.getenv('KEYDB_URL')
api_host = os.getenv('API_HOST')
mac = os.getenv('MAC')

r = connect_to_keydb(keydb_url)

session = r.get("session")

logging.info(f"MAC Address: {mac}")

# @retry(retries=3, delay=15)
def job():
    """Fetch controller details."""

    logging.info("job starting")

    if session is None:
        logging.error("Session is None!")
        raise Exception("Session is None!")
    
    controller = fetch_controller(api_host, session.decode('utf-8'), mac)
    # logging.info(controller)
    if controller:
        cctv = controller.get("cctv")
        logging.info(cctv)
        if cctv:
            # Serialize the list of dictionaries to a JSON string
            my_data_json = json.dumps(cctv)
            r.set("cctv", my_data_json)
        # logging.info("Successfully wrote key session to KeyDB.")
    else:
        logging.error("Failed to fetch controller.")


def run_scheduler():
    """Run the scheduled tasks in an infinite loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule tasks
    schedule.every(10).seconds.do(job)  # Schedule session update

    # Get the initial session ID
    job()

    # Start the scheduler loop
    run_scheduler()
