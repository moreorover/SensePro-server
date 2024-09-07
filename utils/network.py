
import logging
from typing import Dict, List
import netifaces
import re
import socket
import uuid

from scapy.all import ARP, Ether, srp

logger = logging.getLogger(__name__)

class DefaultGatewayNotFoundException(Exception):
    pass

def is_valid_ipv4(ip):
    # Regular expression to validate an IPv4 address
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None

def get_default_gateway():
    # Get the default gateway information
    gateways = netifaces.gateways()
    
    # Extract the default gateway for IPv4
    default_gateway = gateways.get('default', {}).get(netifaces.AF_INET)
    
    if not default_gateway:
        raise DefaultGatewayNotFoundException("Default gateway not found.")
    
    gateway_ip = default_gateway[0]  # IP of the default gateway
    
    if not is_valid_ipv4(gateway_ip):
        raise DefaultGatewayNotFoundException(f"Invalid default gateway: {gateway_ip}")
    
    return gateway_ip


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
    # Get all network interfaces
    interfaces = netifaces.interfaces()
    
    for interface in interfaces:
        # Fetch address info for the interface
        addresses = netifaces.ifaddresses(interface)
        
        # Check if the interface has a MAC address (AF_LINK is for link layer addresses, including MAC)
        if netifaces.AF_LINK in addresses:
            mac_address = addresses[netifaces.AF_LINK][0].get('addr')
            
            if mac_address:
                return mac_address
    
    raise Exception("MAC address not found")

def get_ip_range_for_gateway(default_gateway):
    # Assuming a /24 subnet mask for simplicity
    # We replace the last octet with '0/24' to define the range
    ip_parts = default_gateway.split('.')
    ip_parts[-1] = '0/24'
    return '.'.join(ip_parts)

def scan_network(ip_range) -> List[Dict[str, str]]:
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
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

def find_network_devices() -> List[Dict[str, str]]:
    logging.info(f"Finding network devices...")
    gateway_ip = get_default_gateway()
    logging.info(f"Default Gateway IP Address: {gateway_ip}")

    local_ip = get_local_ip()
    logging.info(f"Local IP Address: {local_ip}")
    
    mac_address = get_mac_address()
    logging.info(f"MAC Address: {mac_address}")

    mac_address_eth0 = get_mac_address()
    logging.info(f"MAC Address eth0: {mac_address_eth0}")

    ip_range = get_ip_range_for_gateway(gateway_ip)
    logging.info(ip_range)

    network_devices = scan_network(ip_range)

    logging.info(f"Found a total of {len(network_devices)} network devices.")
    return network_devices

def find_ip_for_mac(network_devices: List[Dict[str, str]], mac: str) -> str:
    for device in network_devices:
        if device.get("mac") == mac:
            return device.get("ip")
    
    raise Exception(f"There is no such device on the network for MAC: {mac}")

if __name__ == "__main__":
    gateway_ip = get_default_gateway()
    logging.info(f"Default Gateway IP Address: {gateway_ip}")

    local_ip = get_local_ip()
    logging.info(f"Local IP Address: {local_ip}")
    
    mac_address = get_mac_address()
    logging.info(f"MAC Address: {mac_address}")

    ip_range = get_ip_range_for_gateway(gateway_ip)
    logging.info(ip_range)

    network_devices = scan_network(ip_range)

    logging.info("Available devices in the network:")
    logging.info("IP" + " "*18+"MAC")

    for device in network_devices:
        logging.info("{:16}    {}".format(device.get("ip"), device.get("mac")))