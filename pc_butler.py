import host_discovery
import wake_device
import requests


def main():
    while True:
        devices = host_discovery.find_hosts()  # ARP Scan local network
        host_discovery.update_database(devices)  # Update web server

        queue = wake_device.get_queue()
