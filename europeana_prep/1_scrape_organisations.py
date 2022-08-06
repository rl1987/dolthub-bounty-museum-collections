#!/usr/bin/python3

import csv

import requests

FIELDNAMES = ["name", "slug"]


def main():
    out_f = open("orgs.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    headers = {
        "authority": "www.europeana.eu",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-69cc552154f142a22b00de90de241055-06ceac04be17836a-01",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    }

    resp = requests.get(
        "https://www.europeana.eu/_api/cache/collections/organisations", headers=headers
    )
    print(resp.url)

    json_arr = resp.json()

    for json_dict in json_arr:
        name = json_dict.get("prefLabel", dict()).get("en")
        if name is None:
            continue

        slug = json_dict.get("slug")

        row = {"name": name, "slug": slug}

        print(row)
        csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()
