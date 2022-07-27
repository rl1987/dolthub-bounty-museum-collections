#!/usr/bin/python3

import csv
import json
from pprint import pprint

# wget http://www.penn.museum/collections/assets/data/all-csv-latest.zip
# unzip all-csv-latest.zip

FIELDNAMES = [
    "object_number",
    "institution_name",
    "institution_city",
    "institution_state",
    "institution_country",
    "institution_latitude",
    "institution_longitude",
    "department",
    "category",
    "title",
    "description",
    "current_location",
    "dimensions",
    "inscription",
    "provenance",
    "materials",
    "technique",
    "from_location",
    "culture",
    "date_description",
    "year_start",
    "year_end",
    "maker_full_name",
    "maker_first_name",
    "maker_last_name",
    "maker_birth_year",
    "maker_death_year",
    "maker_role",
    "maker_gender",
    "acquired_year",
    "acquired_from",
    "accession_year",
    "accession_number",
    "credit_line",
    "image_url",
    "source_1",
    "source_2",
]


def wrangle_dimension_data(in_row):
    dimension_dict = {
        "measurement_height": in_row.get("measurement_height"),
        "measurement_length": in_row.get("measurement_length"),
        "measurement_width": in_row.get("measurement_width"),
        "measurement_outside_diameter": in_row.get("measurement_outside_diameter"),
        "measurement_tickness": in_row.get("measurement_tickness"),
        "measurement_unit": in_row.get("measurement_unit"),
    }

    return json.dumps(dimension_dict)


def main():
    in_f = open("all-20181028.csv", "r")
    csv_reader = csv.DictReader(in_f)

    out_f = open("objects.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for in_row in csv_reader:
        out_row = {
            "object_number": in_row.get("object_number"),
            "institution_name": "Penn Museum",
            "institution_city": "Philadelphia",
            "institution_state": "PA",
            "institution_country": "USA",
            "institution_latitude": 39.952305,
            "institution_longitude": -75.193703,
            "department": in_row.get("curatorial_section"),
            "category": "",
            "title": in_row.get("object_name"),
            "description": in_row.get("description"),
            "current_location": "",
            "dimensions": wrangle_dimension_data(in_row),
            "inscription": "",
            "provenance": in_row.get("provenience"),
            "materials": in_row.get("material"),
            "technique": in_row.get("technique"),
            "from_location": in_row.get("manufacture_locationlocus"),
            "culture": in_row.get("culture"),
            "date_description": in_row.get("date_made"),
            "year_start": in_row.get("date_made_early").split(" ")[-1],
            "year_end": in_row.get("date_made_late").split(" ")[-1],
            "maker_full_name": in_row.get("creator"),
            "acquired_year": "",
            "acquired_from": "",
            "credit_line": in_row.get("accession_credit_line"),
            "image_url": "",
            "source_1": in_row.get("url"),
            "source_2": "http://www.penn.museum/collections/assets/data/all-csv-latest.zip",
        }

        pprint(out_row)
        csv_writer.writerow(out_row)

    in_f.close()
    out_f.close()


if __name__ == "__main__":
    main()
