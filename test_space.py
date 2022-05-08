import requests
from wakeonlan import send_magic_packet


def main():
    url = f"https://dashboard.pcbutler.net/api/all.json"
    r = requests.get(url=url).json()
    print(r)


if __name__ == "__main__":
    send_magic_packet("20.47.47.EF.6F.C2")
