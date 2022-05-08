from wakeonlan import send_magic_packet
from host_discovery import base_url
import requests


def get_queue():
    r = requests.get(url=f"{base_url}/queue.json")
    queued_devices = [mac["mac"] for mac in r.json()]
    return queued_devices


def clear_queue(mac):
    url = f"{base_url}/delete/queue/{mac}"
    r = requests.get(url=url)
    return r


def clear_all():
    url = f"{base_url}/delete/queue/all"
    r = requests.get(url=url)
    return r


def wake_devices(mac_table):
    for device in mac_table:
        send_magic_packet(device["mac"])
        clear_queue(device["mac"])


if __name__ == "__main__":
    pass
