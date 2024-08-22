import logging
import os
import schedule
from dotenv import load_dotenv
import time
import json

from utils.redis_client import RedisClient
from utils.front_end_api import fetch_controller

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logging.info("Controller service is starting...")

# Load environment variables from the .env file
load_dotenv()

keydb_host = os.getenv('KEYDB_HOST')
keydb_port = os.getenv('KEYDB_PORT')
keydb_database = os.getenv('KEYDB_DATABASE')
api_host = os.getenv('API_HOST')
mac = os.getenv('MAC')

r: RedisClient = RedisClient(host=keydb_host, port=keydb_port, db=keydb_database)

session = r.get_object("session")

logging.info(f"MAC Address: {mac}")

# @retry(retries=3, delay=15)
def job():
    """Fetch controller details."""

    logging.info("job starting")

    if session is None:
        logging.error("Session is None!")
        raise Exception("Session is None!")
    
    controller = fetch_controller(api_host, session, mac)
    # logging.info(controller)
    if controller:
        cctv = controller.get("cctv")
        logging.info(cctv)
        if cctv:
            # Serialize the list of dictionaries to a JSON string
            my_data_json = json.dumps(cctv)
            r.save_object("cctv", my_data_json)
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
