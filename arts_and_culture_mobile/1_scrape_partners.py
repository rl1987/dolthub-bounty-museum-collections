#!/usr/bin/python3

import csv
import json
from pprint import pprint

import requests

FIELDNAMES = ["name", "slug", "city", "state", "country", "latitude", "longitude"]
PROXIES = {
    "http": "http://lum-customer-c_cecd546c-zone-zone_dc_artsandculture:kd9ni4qgyyuv@zproxy.lum-superproxy.io:22225",
    "https": "http://lum-customer-c_cecd546c-zone-zone_dc_artsandculture:kd9ni4qgyyuv@zproxy.lum-superproxy.io:22225",
}


def main():
    out_f = open("partners.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) IOSWebView/9.0.47 ARCapable",
        "x-same-domain": "1",
        "accept-language": "en-GB,en;q=0.9",
    }

    pt = ""

    while True:
        params = {
            "s": "30",
            "pt": pt,
            "hl": "en_LT",
            "rt": "j",
        }

        resp = requests.get(
            "https://artsandculture.google.com/api/objects/partner",
            params=params,
            headers=headers,
            proxies=PROXIES,
        )
        print(resp.url)

        if resp.status_code != 200:
            print(resp.text)
            break

        json_str = resp.text
        json_str = json_str[4:]

        json_arr = json.loads(json_str)

        try:
            pt = json_arr[0][0][-1]
        except:
            pt = None

        json_arr = json_arr[0][0][2]

        for partner_arr in json_arr:
            row = dict()

            row["name"] = partner_arr[1]
            row["slug"] = partner_arr[4].replace("/partner/", "")

            try:
                location = partner_arr[14][7]
                loc_components = location.split(", ")
                row["city"] = loc_components[1]
                row["country"] = partner_arr[2]
                if row["country"] == "United States":
                    row["state"] = loc_components[-2]
            except:
                print(location)

            try:
                row["latitude"] = partner_arr[14][5]
                row["longitude"] = partner_arr[14][6]
            except:
                continue

            if row.get("latitude") is not None and row.get("longitude") is not None:
                pprint(row)
                csv_writer.writerow(row)

        if type(pt) != str:
            break

        params["pt"] = pt

    out_f.close()


if __name__ == "__main__":
    main()
