#!/usr/bin/python3

import csv
import json
from pprint import pprint
from urllib.parse import urljoin

from lxml import html
import requests

HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) IOSWebView/9.0.47 ARCapable',
    'x-same-domain': '1',
    'accept-language': 'en-GB,en;q=0.9',
}

FIELDNAMES = ["object_number", "institution_name", "institution_city", "institution_country",
        "institution_latitude", "institution_longitude", "department", "category",
        "title", "description", "current_location", "dimensions", "inscription",
        "provenance", "materials", "technique", "from_location", "culture", "date_description",
        "year_start", "year_end", "maker_full_name", "maker_first_name", "maker_last_name",
        "maker_birth_year", "maker_death_year", "maker_role", "maker_gender", "acquired_year",
        "acquired_from", "accession_year", "accession_number", "credit_line", "image_url",
        "source_1", "source_2"]

PROXIES = {
    'http': 'http://lum-customer-c_cecd546c-zone-zone_dc_artsandculture:kd9ni4qgyyuv@zproxy.lum-superproxy.io:22225',
    'https': 'http://lum-customer-c_cecd546c-zone-zone_dc_artsandculture:kd9ni4qgyyuv@zproxy.lum-superproxy.io:22225'
}

def scrape_artwork_details(link, in_row):
    asset_id = link.split("/")[-1]

    params = {
        'assetId': asset_id,
        'hl': 'en_LT',
        'rt': 'j',
    }

    resp = requests.get("https://artsandculture.google.com/api/asset", params=params, 
            headers=HEADERS, proxies=PROXIES)
    print(resp.url)

    if resp.status_code != 200:
        return None

    out_row = dict()

    json_str = resp.text
    json_str = json_str[4:]
    json_arr = json.loads(json_str)
    json_arr = json_arr[0][0][2]

    out_row['object_number'] = asset_id
    out_row['institution_name'] = in_row.get('name')
    #out_row['institution_city'] = in_row.get('city')
    #out_row['institution_state'] = in_row.get('state')
    #out_row['institution_country'] = in_row.get('country')
    out_row['institution_latitude'] = in_row.get('latitude')
    out_row['institution_longitude'] = in_row.get('longitude')
    # XXX: department
    out_row['title'] = json_arr[2]

    if json_arr[5] is not None:
        html_str = json_arr[5][-1]
        tree = html.fromstring(html_str)
        out_row['description'] = " ".join(tree.xpath("//text()"))

    out_row['date_description'] = json_arr[3]
    out_row['maker_full_name'] = json_arr[6][0]
    out_row['image_url'] = 'https:' + json_arr[4]

    properties_arr = json_arr[12]

    for prop_arr in properties_arr:
        key = prop_arr[0]
        value = prop_arr[1][0][0]

        if key == "Physical Dimensions":
            out_row['dimensions'] = value
        elif key == "Type":
            out_row['category'] = value
        elif key == "Medium": 
            out_row['materials'] = value
        elif key == "Culture":
            out_row['culture'] = value
        elif key == "Provenance":
            out_row['provenance'] = value
        elif key == "Repository":
            out_row['current_location'] = value
        elif key == "Credit Line":
            out_row['credit_line'] = value

    out_row['source_1'] = urljoin(resp.url, link)
    out_row['source_2'] = resp.url

    return out_row

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

            try:
                out_row = scrape_artwork_details(link, in_row)
            except Exception as e:
                print(e)
                continue

            if out_row is not None:
                yield out_row

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

