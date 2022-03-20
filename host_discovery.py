from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import json

ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.2.0/24"), timeout=2, verbose=0)

mac_table = {}

for query_ans in ans:
    for packet in query_ans:
        device_mac = packet[Ether].src
        device_ip = packet[ARP].psrc
        mac_table[device_ip] = device_mac


if __name__ == "__main__":
    print(json.dumps(mac_table, sort_keys=True, indent=4, separators=(",", ": ")))
    test_change = True