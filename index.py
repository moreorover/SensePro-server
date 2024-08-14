from utils.network import get_default_gateway, get_local_ip, get_mac_address
from utils.front_end_api import fetch_session_id, fetch_controller, update_controller
from dotenv import load_dotenv
import os
import schedule
import time
import urllib.parse
import logging

# Load environment variables from the .env file
load_dotenv()

# Now you can access the environment variables
api_host = os.getenv('API_HOST')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named 'app.log'
        logging.StreamHandler()          # Also log to the console
    ]
)

def run_continuously():
    """Run the schedule in an infinite loop with a small delay between each iteration."""
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second before checking the schedule again

if __name__ == "__main__":
    gateway_ip = get_default_gateway()
    print(f"Default Gateway IP Address: {gateway_ip}")

    local_ip = get_local_ip()
    print(f"Local IP Address: {local_ip}")
    
    mac_address = get_mac_address()
    print(f"MAC Address: {mac_address}")
    # URL encode the MAC address
    encoded_mac_address = urllib.parse.quote(mac_address)
    print(encoded_mac_address)

    # print(f"API Host: {api_host}")

    session = fetch_session_id(api_host, email, password)

    controller = fetch_controller(api_host, session, mac_address)

    controller['ip'] = local_ip

    update_controller(api_host, session, controller)
