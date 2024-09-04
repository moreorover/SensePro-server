import logging
import os
import schedule
from dotenv import load_dotenv
import time

from utils.redis_client import RedisClient
from utils.front_end_api import FrontEndAPI

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

logging.info(f"MAC Address: {mac}")

# @retry(retries=3, delay=15)
def job():
    """Fetch controller details."""

    logging.info("job starting")

    session = r.get_object("session")

    if session is None:
        logging.error("Session is None!")
        raise Exception("Session is None!")
    
    # Create an instance of FrontEndAPI with the host URL
    api = FrontEndAPI(host=api_host, session=session)

    controller = api.fetch_controller(mac)

    if controller:
        cctv = controller.get("cctv")
        # logging.info(cctv)
        if cctv:
            r.save_object("cctv", cctv)
            for c in cctv:
                logging.info(c)
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
