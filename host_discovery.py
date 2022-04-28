from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import requests
import random
import json


def find_hosts():
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.2.0/24"), timeout=2, verbose=0)
    return ans


def get_current_computers():
    url = "http://dashboard.pcbutler.net/api/all.json"
    active_comps = requests.get(url=url).json()
    active_macs = [comp["mac"] for comp in active_comps]
    return active_macs


hostnames = ["DESKTOP-BOB", "DESKTOP-ALICE", "DESKTOP-STEVE", "DESKTOP-RECEPTION", "DESKTOP-OFFICE"]


def send_computer(mac, hostname, address):
    url = f"http://dashboard.pcbutler.net/api/new/{mac}/{hostname}/{address}"
    r = requests.get(url=url)
    print(r.text)


def sending_computer(ans):
    for query_ans in ans:
        for packet in query_ans:
            device_mac = packet[Ether].src
            device_ip = packet[ARP].psrc
            send_computer(device_mac, random.choice(hostnames), device_ip)


if __name__ == "__main__":
    pass
