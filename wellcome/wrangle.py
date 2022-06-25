#!/usr/bin/python3

import csv
import json

# Data from: https://developers.wellcomecollection.org/docs/datasets
# https://developers.wellcomecollection.org/api/catalogue#operation/getWork

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

def extract_maker_names(contributors):
    maker_names = []

    for contributor in contributors:
        maker_names.append(contributor.get("agent", dict()).get("label"))

    return maker_names

def extract_maker_roles(contributors):
    maker_roles = []

    for contributor in contributors:
        roles = contributor.get("roles", [])

        if len(roles) > 0:
            maker_roles.append(roles[0].get("label"))
        else:
            maker_roles.append("")

    return maker_roles

def main():
    out_f = open("objects.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    in_f = open("works.json", "r")
    for json_line in in_f:
        json_dict = json.loads(json_line)

        out_row = {
            "object_number": json_dict.get("id"),
            "institution_name": "Wellcome Collection",
            "institution_city": "London",
            "institution_country": "United Kingdom",
            "institution_latitude": 51.5259,
            "institution_longitude": 0.1339,
            "title": json_dict.get("title"),
            "description": json_dict.get("description"),
            "dimensions": json_dict.get("physicalDescription"),
            "category": json_dict.get("workType"),
            "inscription": json_dict.get("lettering"),
            "date_description": json_dict.get("createdDate", dict()).get("label"),
            "maker_full_name": "|".join(extract_maker_names(json_dict.get("contributors", []))),
            "maker_role": "|".join(extract_maker_roles(json_dict.get("contributors", []))),
            "image_url": json_dict.get("thumbnail", dict()).get("url"),
            "source_1": "https://data.wellcomecollection.org/catalogue/v2/works.json.gz",
            "source_2": "https://api.wellcomecollection.org/catalogue/v2/works/" + json_dict.get("id")
        }

    in_f.close()
    out_f.close()

if __name__ == "__main__":
    main()

