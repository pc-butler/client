from scapy.layers.l2 import ARP, Ether, srp, Loopback

import nmap


def main():
    scanner = nmap.PortScanner()
    scan_range = scanner.scan(hosts="192.168.2.101")

if __name__ == "__main__":
    main()