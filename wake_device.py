import time

import requests
from wakeonlan import send_magic_packet

from host_discovery import base_url, send_wake_status, get_current_computers


def get_queue():
    r = requests.get(url=f"{base_url}/queue.json")
    if r.json() is None:
        return []
    else:
        queued_devices = [mac["mac"] for mac in r.json()]
    return queued_devices


def clear_queue(mac):
    url = f"{base_url}/delete/queue/{mac}"
    r = requests.get(url=url)
    return r


def clear_all():
    current_comps = get_current_computers()
    for mac in current_comps:
        url = f"{base_url}/delete/{mac}"
        r = requests.get(url=url)


def wake_devices(queued_devices):
    for mac in queued_devices:
        i = 0
        print(f"Sending magic packet to {mac}")
        while i <= 3:
            send_magic_packet(mac)
            i += 1
        clear_queue(mac)
        time.sleep(5)
        send_wake_status(mac, flag="online")


def start():
    devices = get_queue()
    print(f"{len(devices)} : {devices}")
    if len(devices) == 0:
        pass
    else:
        wake_devices(devices)


if __name__ == "__main__":
    clear_all()
    print("Cleared all from database.")
