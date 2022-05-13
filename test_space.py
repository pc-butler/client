import requests


def main():
    url = f"https://dashboard.pcbutler.net/api/delete/queue_all"
    r = requests.get(url=url)


if __name__ == "__main__":
    main()
