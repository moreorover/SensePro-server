import requests
from requests.auth import HTTPDigestAuth
import logging

logger = logging.getLogger(__name__)

class DahuaClient:
    def __init__(self, ip_address, username, password):
        self.ip_address = ip_address
        self.username = username
        self.password = password

    def get_system_info(self):
        """
        Retrieve system information from the Dahua camera.
        """
        url = f'http://{self.ip_address}/cgi-bin/magicBox.cgi?action=getSystemInfo'

        try:
            # Perform the GET request with HTTP Digest Authentication
            response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password))
            
            # Log request and response headers for inspection
            # logger.info("Request Headers: %s", response.request.headers)
            # logger.info("Response Headers: %s", response.headers)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.text
                logger.info("Device Info: %s", data)
                return data  # Returning the data for further use
            else:
                logger.error("Failed to retrieve device info. HTTP Status Code: %d", response.status_code)
                logger.error("Response Text: %s", response.text)
                return None

        except requests.exceptions.RequestException as e:
            logger.error("An error occurred: %s", e)
            return None

    def get_serial_number(self):
        """
        Extract and return the serial number from the system information.
        """
        system_info = self.get_system_info()
        if system_info:
            for line in system_info.splitlines():
                if "serialNumber" in line:
                    _, serial_number = line.split('=')
                    serial_number = serial_number.strip()
                    logger.info("Serial Number: %s", serial_number)
                    return serial_number
        return None

    # Add more methods as needed to interact with the camera's API
