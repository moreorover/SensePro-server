import netifaces
import socket
import uuid

def get_default_gateway():
    gateways = netifaces.gateways()
    default_gateway = gateways.get('default')
    
    if default_gateway:
        # Get the default gateway for IPv4
        gateway_ip = default_gateway.get(netifaces.AF_INET)
        if gateway_ip:
            return gateway_ip[0]
        else:
            return "No IPv4 gateway found"
    else:
        return "No default gateway found"


def get_local_ip():
    try:
        # Connect to an external server to find the local IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to a remote host on a non-open port (no data is sent)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        return f"An error occurred: {e}"


def get_mac_address():
    # Get the MAC address using uuid.getnode()
    mac = uuid.getnode()
    # Format the MAC address in human-readable form
    mac_address = ':'.join(f'{(mac >> 8*i) & 0xff:02x}' for i in reversed(range(6)))
    return mac_address


if __name__ == "__main__":
    gateway_ip = get_default_gateway()
    print(f"Default Gateway IP Address: {gateway_ip}")

    local_ip = get_local_ip()
    print(f"Local IP Address: {local_ip}")
    
    mac_address = get_mac_address()
    print(f"MAC Address: {mac_address}")