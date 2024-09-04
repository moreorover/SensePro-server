import netifaces
import socket
import uuid

from scapy.all import ARP, Ether, srp

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

def get_mac_address_eth0(interface='eth0'):
    # Get the MAC address of the specified interface
    mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    return mac_address

def get_ip_range(default_gateway):
    # Assuming a /24 subnet mask for simplicity
    # We replace the last octet with '0/24' to define the range
    ip_parts = default_gateway.split('.')
    ip_parts[-1] = '0/24'
    return '.'.join(ip_parts)

def scan_network(ip_range):
    # Create ARP request packet
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Send packet and get the response
    result = srp(packet, timeout=3, verbose=0)[0]

    # Store the results in a list
    devices = []

    for sent, received in result:
        # Append the IP and MAC address of each device to the list
        devices.append({'IP': received.psrc, 'MAC': received.hwsrc})
    
    return devices

if __name__ == "__main__":
    gateway_ip = get_default_gateway()
    print(f"Default Gateway IP Address: {gateway_ip}")

    local_ip = get_local_ip()
    print(f"Local IP Address: {local_ip}")
    
    mac_address = get_mac_address()
    print(f"MAC Address: {mac_address}")

    mac_address_eth0 = get_mac_address()
    print(f"MAC Address eth0: {mac_address_eth0}")

    ip_range = get_ip_range(gateway_ip)
    print(ip_range)

    network_devices = scan_network(ip_range)

    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")

    for device in network_devices:
        print("{:16}    {}".format(device['IP'], device['MAC']))