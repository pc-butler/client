from wakeonlan import send_magic_packet
import requests

queue_endpoint = "http://dashboard.pcbutler.net/api/queue.json"


def get_table():
    r = requests.get(url=queue_endpoint)
    return r.json()


def clear_queue(mac_address):
    payload = {"mac": mac_address}
    r = requests.delete(url=queue_endpoint, data=payload)
    print(r.status_code)


def wake_devices(mac_table):
    for device in mac_table:
        send_magic_packet(device["mac"])
        clear_queue(device["mac"])


if __name__ == "__main__":
    mac_table = get_table()
    wake_devices(mac_table)