from wakeonlan import send_magic_packet
from host_discovery import base_url, send_wake_status
import sys
from tqdm.contrib.concurrent import thread_map
import requests
import time


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
    url = f"{base_url}/delete/queue/all"
    r = requests.get(url=url)
    return r


def wake_devices(mac_table):
    thread_map(send_magic_packet, get_queue)
    thread_map(clear_queue, get_queue)
    time.sleep(5)
    thread_map(send_wake_status, get_queue)


def start():
    devices = get_queue()
    if len(devices) == 0:
        pass
    else:
        wake_devices(devices)
