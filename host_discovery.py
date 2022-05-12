import sys
import time

import requests
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp

import wake_device

base_url = "https://dashboard.pcbutler.net/api"


def find_hostname(mac):
    hostnames = {
        "20-47-47-EF-6F-C2": "SAI-PC",
        "20-47-47-BA-62-92": "JOHN-PC",
        "98-28-A6-24-8A-58": "ROYCE-PC",
        "30-5A-3A-C4-47-68": "GATEWAY",
        "DC-A6-32-0C-0F-B0": "PCBUTLER",
        "5C-26-0A-2A-64-97": "LUCIA-PC"
    }
    if mac in hostnames.keys():
        return hostnames[mac]
    return "UNKNOWN"


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


def send_wake_status(mac, flag=None):
    url = None
    if flag == "online":
        url = f"{base_url}/update/online/{mac}"
    if flag == "offline":
        url = f"{base_url}/update/offline/{mac}"
    r = requests.get(url=url)


def send_computer(mode, mac=None, hostname=None, address=None):
    target_url = None
    if mode == "new":
        target_url = f"{base_url}/new/{mac}/{hostname}/{address}"
    elif mode == "update":
        target_url = f"{base_url}/update/{mac}/{address}"
    r = requests.get(url=target_url)


def format_mac(mac):
    sep = mac[2]
    return mac.replace(sep, "-").upper()


def update_database(ans):
    discovery_table = {}
    for query_ans in ans:  # Discover new devices
        for packet in query_ans:
            device_mac = format_mac(packet[Ether].src)
            device_ip = packet[ARP].psrc
            discovery_table[device_mac] = device_ip
    print(discovery_table)

    database_macs = get_current_computers()
    if len(database_macs) != 0:
        for mac in database_macs:  # Check if device is already in database
            if mac in discovery_table.keys():  # Send online status if in db
                send_wake_status(mac, flag="online")
                discovery_table.pop(mac)
            else:  # Send offline status if in db but not discovered
                send_wake_status(mac, flag="offline")

    for mac, ip in discovery_table.items():
        send_computer("new", mac=mac, address=ip, hostname=find_hostname(mac))
        send_wake_status(mac, flag="online")


if __name__ == "__main__":
    while True:
        try:
            update_database(find_hosts())
            time.sleep(8)
            wake_device.start()
        except KeyboardInterrupt:
            sys.exit(0)
