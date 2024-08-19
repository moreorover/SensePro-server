import requests
import logging
from typing import Optional, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"

def send_request(method: HTTPMethod, url: str, cookies: Optional[Dict[str, str]] = None, json: Optional[Dict[str, Any]] = None) -> requests.Response:
    """Sends an HTTP request and handles common errors."""
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


def fetch_session_id(host: str, email: str, password: str) -> Optional[str]:
    """Fetches a session ID using the provided credentials."""
    url = f'{host}/api/auth/signin'
    payload = {'email': email, 'password': password}

    response = send_request(HTTPMethod.POST, url, json=payload)
    session_cookie = response.cookies.get('session')
    if not session_cookie:
        logger.error("Session cookie not found in response.")
        raise Exception("Session cookie not found in response.")
    
    logger.info("Session ID found!")
    return session_cookie


def fetch_controller(host: str, session: str, mac: str) -> Optional[Dict[str, Any]]:
    """Fetches controller information based on the MAC address."""
    url = f'{host}/api/controller/{mac}'
    cookies = {'session': session}

    response = send_request(HTTPMethod.GET, url, cookies=cookies)
    return response.json()


def update_controller(host: str, session: str, controller: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Updates controller information based on the provided data."""
    controller_id = controller.get('id')
    if not controller_id:
        logger.error("Controller ID is missing.")
        raise ValueError("Controller ID is required for updating.")

    url = f'{host}/api/devices/{controller_id}'
    cookies = {'session': session}

    response = send_request(HTTPMethod.PATCH, url, json=controller, cookies=cookies)
    return response.json()
