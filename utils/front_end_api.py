import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def send_request(method: str, url: str, cookies: Optional[Dict[str, str]] = None, json: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
    try:
        if method == "GET":
            response = requests.get(url, cookies=cookies)
        elif method == "POST":
            response = requests.post(url, json=json, cookies=cookies)
        elif method == "PATCH":
            response = requests.patch(url, json=json, cookies=cookies)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def fetch_session_id(host: str, email: str, password: str) -> Optional[str]:
    url = f'{host}/api/auth/signin'
    payload = {'email': email, 'password': password}
    logging.info(f"Sending POST request to {url}")
    
    try:
        response = requests.post(url, json=payload)
        logging.info(f"Response code: {response.status_code}")
        
        if response.status_code != 200:
            raise Exception(f"Failed to authenticate. Status code: {response.status_code}")
        
        session_cookie = response.cookies.get('session')
        if session_cookie:
            logging.info(f"Session ID found!")
            return session_cookie
        else:
            raise Exception("Session cookie not found in response.")
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise Exception(f"Request to {url} failed") from e

def fetch_controller(host: str, session: str, mac: str) -> Optional[Dict[str, Any]]:
    url = f'{host}/api/controller/{mac}'
    cookies = {'session': session}

    logging.info(f"Fetching controller information from {url}")
    
    try:
        response = requests.get(url, cookies=cookies)
        logging.info(f"Response code: {response.status_code}")
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch controller. Status code: {response.status_code}")
        
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise Exception(f"Request to {url} failed") from e

def update_controller(host: str, session: str, controller: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    controller_id = controller.get('id')
    if not controller_id:
        logging.error("Controller ID is missing.")
        raise ValueError("Controller ID is required for updating.")

    url = f'{host}/api/devices/{controller_id}'
    cookies = {'session': session}

    logging.info(f"Updating controller {controller_id} at {url}")
    
    try:
        response = requests.patch(url, json=controller, cookies=cookies)
        logging.info(f"Response code: {response.status_code}")
        
        if response.status_code != 200:
            raise Exception(f"Failed to update controller. Status code: {response.status_code}")
        
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise Exception(f"Request to {url} failed") from e