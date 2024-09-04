from utils.dahua_client import DahuaClient
from utils.network import get_mac_address
from utils.front_end_api import fetch_session_id, fetch_controller
from dotenv import load_dotenv
import os
import schedule
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named 'app.log'
        logging.StreamHandler()          # Also log to the console
    ]
)

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
api_host = os.getenv('API_HOST')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

session = None
mac_address = get_mac_address()
logging.info(f"MAC Address set: {mac_address}")

def update_session_id():
    """Fetch a new session ID every hour."""
    global session
    session = fetch_session_id(api_host, email, password)
    if session:
        logging.info("Session ID updated successfully.")
    else:
        logging.error("Failed to update Session ID.")

def fetch_controller_id():
    """Fetch the controller ID every minute."""
    if session is not None and mac_address is not None:
        controller = fetch_controller(api_host, session, mac_address)
        if controller:
            cid = controller.get('id')
            logging.info(f'Fetched Controller ID: {cid}')
        else:
            logging.error("Failed to fetch Controller ID.")
    else:
        logging.warning("Session or MAC address not set. Skipping controller fetch.")

def fetch_dahua_id():
    # Example usage:
    camera = DahuaClient(ip_address='192.168.88.51', username='admin', password='kc158741')

    # Get system info
    camera.get_system_info()

    # Get serial number
    x = camera.get_serial_number()
    logging.info(x)

def run_scheduler():
    """Run the scheduled tasks in an infinite loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule tasks
    schedule.every(5).seconds.do(update_session_id)  # Update session ID every hour
    schedule.every(2).seconds.do(fetch_controller_id)  # Fetch controller ID every minute

    # Get the initial session ID
    update_session_id()

    # Start the scheduler loop
    run_scheduler()
