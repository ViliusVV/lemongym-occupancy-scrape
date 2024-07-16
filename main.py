import datetime
import time

import requests
from bs4 import BeautifulSoup

SCRAPE_INTERVAL = 60 * 3  # minutes
TGT_URL = "https://www.lemongym.lt/wp-json/api/async-render-block?pid=MTI2NQ==&bid=YWNmL2NsdWJzLW9jY3VwYW5jeQ==&rest_language=lt"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Cookie": "pll_language=lt; consents_essentials=1; consents_required=1; consents_functional=1; consents_analytics=1; PHPSESSID=2m0ats33guhl61rppp137b6f62",
    "Referer": "https://www.lemongym.lt/klubu-uzimtumas/",
}


def fetch_page() -> str:
    print("Sending request...")
    r = requests.get(TGT_URL, headers=HEADERS)
    print("Response received.")
    if r.status_code != 200:
        print(f"Error: {r.status_code}, {r.text}")

    json_response = r.json()
    if not json_response["success"]:
        print(f"Success not true")
    elif not json_response["data"]["success"]:
        print(f"Data success not true")

    return json_response["data"]["content"]


def parse_club(div) -> tuple[str, int]:
    # find club name clubs-occupancy__club -> first h6
    club_name = div.find("div", class_="clubs-occupancy__club").find("h6").text.strip()

    # find occupancy clubs-occupancy__percentage
    club_occupancy = div.find(class_="clubs-occupancy__percentage").text.strip().removesuffix("%")
    club_occupancy = int(club_occupancy)
    return club_name, club_occupancy


def parse_page(html: str) -> dict[str, int]:
    print("Parsing response...")
    res_dict = {}

    soup = BeautifulSoup(html, "html.parser")
    # find all divs with class "clubs-occupancy"
    clubs_divs = soup.find_all("div", class_="clubs-occupancy")
    for club_div in clubs_divs:
        try:
            club_name, club_occupancy = parse_club(club_div)
            res_dict[club_name] = club_occupancy
        except Exception as e:
            print(f"Error parsing club: {e}")

    print("Response parsed.")
    return res_dict


def write_to_csv(os: dict[str, int]):
    iso_time = datetime.datetime.now(datetime.UTC).isoformat()
    # append to file
    with open("occupancies.csv", "a+", encoding="utf-8") as file:
        for c, o in os.items():
            file.write(f"{iso_time};{c};{o}\n")


if __name__ == "__main__":
    last_time = datetime.datetime.now() - datetime.timedelta(minutes=SCRAPE_INTERVAL)
    while True:
        current_time = datetime.datetime.now()
        if (current_time - last_time).seconds > SCRAPE_INTERVAL:
            print(f"\n\n========== Scraping at {current_time} ==============")
            last_time = current_time
            response = fetch_page()
            occupancies = parse_page(response)
            write_to_csv(occupancies)
            for club, occupancy in occupancies.items():
                print(f"{club}: {occupancy}")

            print("Sleeping.", end="")
        else:
            print(".", end="")

        time.sleep(1)
