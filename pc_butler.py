import host_discovery
import wake_device
import sys
from datetime import datetime


def perform_host_discovery():
    devices = host_discovery.find_hosts()  # ARP Scan local network
    host_discovery.update_database(devices)  # Update web server


def wake_devices():
    queue = wake_device.get_queue()
    wake_device.wake_devices(queue)


def main():
    discover = host_discovery.find_hosts()
    host_discovery.update_database(discover)

if __name__ == "__main__":
    print("Starting PC Butler...")
    main()
