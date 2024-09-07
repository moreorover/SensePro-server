import logging
import os
import schedule
from dotenv import load_dotenv
import time

from utils.network import find_ip_for_mac, find_network_devices, get_mac_address
from utils.redis_client import RedisClient
from utils.retry import retry
from utils.front_end_api import FrontEndAPI

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

# Create an instance of FrontEndAPI with the host URL
api = FrontEndAPI(host=api_host)

mac = get_mac_address()

@retry(retries=3, delay=15)
def fetch_session():
    """Fetch a new session ID with retries on failure."""
    session = api.fetch_session_id(email, password)
    if session:
        r.save_object("session", session)
        logging.info("Successfully wrote key session to KeyDB.")
    else:
        logging.error("Failed to update Session ID.")

def fetch_devices():
    """Fetch controller details."""

    logging.info("job starting")

    session = r.get_object("session")

    if session is None:
        logging.error("Session is None!")
        raise Exception("Session is None!")
    
    # Create an instance of FrontEndAPI with the host URL
    api = FrontEndAPI(host=api_host, session=session)

    controller = api.fetch_controller(mac)

    network_devices = find_network_devices()

    if controller:
        cctv_devices = controller.get("cctv")
        if cctv_devices:
            r.save_object("cctv", cctv_devices)
            for cctv_device in cctv_devices:
                device_mac = cctv_device.get("mac")
                device_ip = find_ip_for_mac(network_devices, device_mac)

                if device_ip is None:
                    logging.error(f"Could not find IP address for mac: {device_mac}")
                    continue
                
                if cctv_device.get("ip") != device_ip:
                    logging.info("Device IP address is not the same.")
                    cctv_device['ip'] = device_ip
                    api.update_device(cctv_device)
                    r.save_object("cctv", cctv_devices)

                logging.info(f"IP {device_ip} for MAC {device_mac}")

    else:
        logging.error("Failed to fetch controller.")

def run_scheduler():
    """Run the scheduled tasks in an infinite loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule tasks
    schedule.every(5).seconds.do(fetch_session)  # Schedule session update
    schedule.every(10).seconds.do(fetch_devices) # Schedule device update

    # Get the initial session ID
    fetch_session()

    fetch_devices()

    # Start the scheduler loop
    run_scheduler()
