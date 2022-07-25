#!/usr/bin/python3

import csv
import json

import requests
from pprint import pprint

HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) IOSWebView/9.0.47 ARCapable',
    'x-same-domain': '1',
    'accept-language': 'en-GB,en;q=0.9',
}

FIELDNAMES = ["object_number", "institution_name"]

PROXIES = {
    'http': 'http://lum-customer-c_cecd546c-zone-zone_dc_artsandculture:kd9ni4qgyyuv@zproxy.lum-superproxy.io:22225',
    'https': 'http://lum-customer-c_cecd546c-zone-zone_dc_artsandculture:kd9ni4qgyyuv@zproxy.lum-superproxy.io:22225'
}

def scrape_artwork_data(in_row):
    slug = in_row.get("slug")

    pt = ''

    while True:
        params = {
            'p': slug, 
            's': '18',
            'pm': '1',
            'pt': pt,
            'hl': 'en_LT',
            'rt': 'j',
        }

        resp = requests.get("https://artsandculture.google.com/api/assets/images", params=params,
                headers=HEADERS, proxies=PROXIES)
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

        for artwork_arr in json_arr:
            link = artwork_arr[4]
            print(link)

        if type(pt) != str:
            break

def main():
    in_f = open("filtered_partners.csv", "r")

    out_f = open("artworks.csv", "w", encoding="utf-8")
    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    csv_reader = csv.DictReader(in_f)

    for in_row in csv_reader:
        for out_row in scrape_artwork_data(in_row):
            if out_row is None:
                continue

            pprint(out_row)
            csv_writer.writerow(out_row)

    in_f.close()

if __name__ == "__main__":
    main()

