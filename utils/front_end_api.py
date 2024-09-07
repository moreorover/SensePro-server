import requests
import logging
from typing import Optional, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"

class FrontEndAPI:
    def __init__(self, host: str, session: Optional[str] = None):
        self.host = host
        self.session = session

    def _send_request(self, method: HTTPMethod, endpoint: str, cookies: Optional[Dict[str, str]] = None, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Sends an HTTP request and handles common errors."""
        url = f"{self.host}{endpoint}"
        try:
            logger.info(f"Sending {method.value} request to {url}")
            response = requests.request(method.value, url, cookies=cookies, json=json)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info(f"Received {response.status_code} response from {url}")
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def fetch_session_id(self, email: str, password: str) -> Optional[str]:
        """Fetches a session ID using the provided credentials."""
        endpoint = '/api/auth/signin'
        payload = {'email': email, 'password': password}

        response = self._send_request(HTTPMethod.POST, endpoint, json=payload)
        session_cookie = response.cookies.get('session')
        if not session_cookie:
            logger.error("Session cookie not found in response.")
            raise Exception("Session cookie not found in response.")
        
        logger.info("Session ID found!")
        self.session = session_cookie  # Store session cookie in the object
        return self.session

    def fetch_controller(self, mac: str) -> Optional[Dict[str, Any]]:
        """Fetches controller information based on the MAC address."""
        if not self.session:
            logger.error("Session ID is required to fetch the controller.")
            raise Exception("Session ID is required.")

        endpoint = f'/api/controller/{mac}'
        cookies = {'session': self.session}

        response = self._send_request(HTTPMethod.GET, endpoint, cookies=cookies)
        return response.json()

    def update_device(self, device: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Updates controller information based on the provided data."""
        if not self.session:
            logger.error("Session ID is required to update the controller.")
            raise Exception("Session ID is required.")

        device_id = device.get('id')
        if not device_id:
            logger.error("Device ID is missing.")
            raise ValueError("Device ID is required for updating.")

        endpoint = f'/api/devices/{device_id}'
        cookies = {'session': self.session}

        response = self._send_request(HTTPMethod.PATCH, endpoint, json=device, cookies=cookies)
        return response.json()
