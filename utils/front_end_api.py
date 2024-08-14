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

    response = send_request("POST", url, json=payload)

    if response:
        session_cookie = response.cookies.get('session')
        if session_cookie:
            logging.info(f"Session ID: {session_cookie}")
            return session_cookie
        else:
            logging.warning("Session cookie not found in response.")
    return None

def fetch_controller(host: str, session: str, mac: str) -> Optional[Dict[str, Any]]:
    url = f'{host}/api/controller/{mac}'
    cookies = {'session': session}

    response = send_request("GET", url, cookies=cookies)

    if response:
        return response.json()
    return None

def update_controller(host: str, session: str, controller: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    controller_id = controller.get('id')
    if not controller_id:
        logging.error("Controller ID is missing.")
        return None

    url = f'{host}/api/devices/{controller_id}'
    cookies = {'session': session}

    response = send_request("PATCH", url, json=controller, cookies=cookies)

    if response:
        return response.json()
    return None
