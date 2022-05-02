import host_discovery
import wake_device
import logging
import requests
from datetime import datetime


def main():

    now = datetime.now().strftime("%H-%M-%S")
    logging.basicConfig(filename="log_file.log", level=logging.DEBUG)
    logging.info(f"Starting at {now}")

    print("Starting PC Butler...")

    while True:
        devices = host_discovery.find_hosts()  # ARP Scan local network
        logging.info(f"Devices found: {devices}")
        host_discovery.update_database(devices)  # Update web server

        queue = wake_device.get_queue()
