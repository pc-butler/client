from wakeonlan import send_magic_packet
import requests

queue_endpoint = "http://dashboard.pcbutler.net/api/queue.json"


def get_queue():
    r = requests.get(url=queue_endpoint)
    print("text")
    return r.json()


def clear_queue(mac):
    url = f"http://dashboard.pcbutler.net/api/delete/queue/{mac}"
    r = requests.get(url=url)
    return r


def clear_all():
    url = f"http://dashboard.pcbutler.net/api/delete/queue/all"
    r = requests.get(url=url)
    return r


def wake_devices(mac_table):
    for device in mac_table:
        send_magic_packet(device["mac"])


if __name__ == "__main__":
    pass
