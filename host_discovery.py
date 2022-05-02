from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from datetime import datetime
import requests
import random

base_url = "http://dashboard.pcbutler/api"


def find_hosts():
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.2.0/24"), timeout=2, verbose=0)
    return ans


def get_current_computers():
    url = f"{base_url}/all.json"
    active_comps = requests.get(url=url).json()
    active_macs = [comp["mac"] for comp in active_comps]
    return active_macs


hostnames = ["DESKTOP-BOB", "DESKTOP-ALICE", "DESKTOP-STEVE", "DESKTOP-RECEPTION", "DESKTOP-OFFICE"]


def send_computer(mode, mac=None, hostname=None, address=None, time=None):
    target_url = None
    if mode == "new":
        target_url = f"{base_url}/{mac}/{hostname}/{address}"
    elif mode == "update":
        target_url = f"{base_url}/update/{mac}"
    r = requests.get(url=target_url)
    print(r.text)


def update_database(ans):
    active_macs = get_current_computers()
    for query_ans in ans:
        for packet in query_ans:
            device_mac = packet[Ether].src
            device_ip = packet[ARP].psrc
            if device_mac in active_macs:
                send_computer("update", time=datetime.now().timestamp())
            else:
                send_computer("new", mac=device_mac, hostname=random.choice(hostnames), address=device_ip)


if __name__ == "__main__":
    update_database(find_hosts())