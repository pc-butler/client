import requests


def main():
    url = f"https://dashboard.pcbutler.net/api/all.json"
    r = requests.get(url=url).json()
    print(r)


if __name__ == "__main__":
    main()
