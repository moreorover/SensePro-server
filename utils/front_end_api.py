import requests

def fetchSessionId(host, email, password):
    # The URL to which the POST request will be sent
    url = f'{host}/api/auth/signin'

    # The data you want to send in the POST request
    payload = {
        'email': email,
        'password': password
    }

    # Sending the POST request with a JSON body
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Access cookies from the response
        cookies = response.cookies

        # Print all cookies
        for cookie in cookies:
            print(f"Cookie Name: {cookie.name}, Cookie Value: {cookie.value}")

        # Access a specific cookie by name
        session_cookie = cookies.get('session')
        if session_cookie:
            print(f"Session ID: {session_cookie}")
        return session_cookie
    else:
        print(f"Failed to fetch response, status code: {response.status_code}")


def fetchController(host, session, mac):
    # The URL to which the POST request will be sent
    url = f'{host}/api/controller/{mac}'

    # Define the cookies you want to set
    cookies = {
        'session': session,
    }

    # Sending the POST request with a JSON body
    response = requests.get(url, cookies=cookies)

    print(response.status_code)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()


def updateController(host, session, controller):
    controllerId = controller['id']
    # The URL to which the POST request will be sent
    url = f'{host}/api/devices/{controllerId}'

    # Define the cookies you want to set
    cookies = {
        'session': session,
    }

    # Sending the POST request with a JSON body
    response = requests.patch(url, json=controller, cookies=cookies)

    print(response.status_code)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    
