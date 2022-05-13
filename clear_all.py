import requests


def main():
    url = f"https://dashboard.pcbutler.net/api/delete_all"
    r = requests.get(url=url)
    print("Database cleared.")


if __name__ == "__main__":
    main()
