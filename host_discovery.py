from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from wakeonlan import send_magic_packet
from datetime import datetime
import wake_device
import requests
import random
import sys
import time

base_url = "https://dashboard.pcbutler.net/api"


def find_hosts():
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24"), timeout=2, verbose=0)
    return ans


def get_current_computers():
    url = f"{base_url}/all.json"
    active_comps = requests.get(url=url).json()
    if active_comps is None:
        active_macs = []
    else:
        active_macs = [comp["mac"] for comp in active_comps]
    return active_macs


hostnames = ["DESKTOP-BOB", "DESKTOP-ALICE", "DESKTOP-STEVE", "DESKTOP-RECEPTION", "DESKTOP-OFFICE"]


def send_wake_status(mac, flag=None):
    url = None
    if flag == "online":
        url = f"{base_url}/api/update/online/{mac}"
    if flag == "offline":
        url = f"{base_url}/api/update/offline/{mac}"
    r = requests.get(url=url)


def send_computer(mode, mac=None, hostname=None, address=None):
    target_url = None
    if mode == "new":
        target_url = f"{base_url}/new/{mac}/{hostname}/{address}"
    elif mode == "update":
        target_url = f"{base_url}/update/{mac}/{address}"
    r = requests.get(url=target_url)


def update_database(ans):
    discovery_table = {}
    for query_ans in ans:  # Discover new devices
        for packet in query_ans:
            device_mac = packet[Ether].src
            device_ip = packet[ARP].psrc
            discovery_table[device_mac] = device_ip
    print(discovery_table)

    database_macs = get_current_computers()
    if len(database_macs) != 0:
        for mac in database_macs:  # Check if device is already in database
            if mac in discovery_table.keys():  # Send online status if in db
                send_wake_status(mac, "online")
                discovery_table.pop(mac)
            else:  # Send offline status if in db but not discovered
                send_wake_status(mac, "offline")
                discovery_table.pop(mac)

        for mac, ip in discovery_table.items():
            send_computer("new", mac=mac, address=ip, hostname=random.choice(hostnames))
    else:
        for mac, ip in discovery_table.items():
            send_computer("new", mac=mac, address=ip, hostname=random.choice(hostnames))
            send_wake_status(mac, "online")



if __name__ == "__main__":
    while True:
        try:
            update_database(find_hosts())
            time.sleep(5)
            wake_device.start()
        except KeyboardInterrupt:
            sys.exit(0)
