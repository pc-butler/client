from wakeonlan import send_magic_packet
import requests

queue_endpoint = "http://dashboard.pcbutler.net/api/queue.json"


def get_table():
    r = requests.get(url=queue_endpoint)
    print("text")
    return r.json()


def clear_queue():
    pass
### Waiting on endpoint for clear queue

def wake_devices(mac_table):
    for device in mac_table:
        send_magic_packet(device["mac"])


if __name__ == "__main__":
    mac_table = get_table()
    print(mac_table)
    wake_devices(mac_table)
