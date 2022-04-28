import host_discovery
import wake_device
import requests

def main():
    while True:
        devices = host_discovery.find_hosts()
        host_discovery.sending_computer(devices)
        wake_table = wake_device.get_table()


def get_current_devices():
    url = "https://dashboard.pcbutler.net/api/all.json"
