#!/usr/bin/python3

import doltcli as dolt

# Based on:
# https://github.com/elouajib/sqlescapy/blob/master/sqlescapy/sqlescape.py
def escape(str):
    return str.translate(
        str.maketrans({
            "\0": "\\0",
            "\r": "\\r",
            "\x08": "\\b",
            "\x09": "\\t",
            "\x1a": "\\z",
            "\n": "\\n",
            "\r": "\\r",
            "\"": "\\\"",
            "'": "\\'",
            "\\": "\\\\",
            "%": "\\%"
        }))

def main():
    db = dolt.Dolt("/root/data/museum-collections/")

    sql1 = 'SELECT * FROM `objects` WHERE `institution_name` = "The National Museum of World Cultures";'
    print(sql1)

    res = db.sql(sql1, result_format="csv")

    for row in res:
        description = row['description']
        object_number = row['object_number']

        from_idx = 0

        if row['dimensions'] is not None and row['dimensions'] != '':
            from_idx = description.index(row['dimensions']) + len(row['dimensions'])
        elif row['provenance'] is not None and row['provenance'] != '':
            from_idx = description.index(row['provenance']) + len(row['provenance'])
        elif row['culture'] is not None and row['culture'] != '':
            from_idx = description.index(row['culture']) + len(row['culture'])

        try:
            to_idx = description.index('Inventarisnummer')
        except:
            try:
                to_idx = description.index('Object number')
            except:
                continue

        new_description = description[from_idx:to_idx]
        new_description = new_description.strip()
        if new_description.startswith('/'):
            new_description = ''
        
        print("'{}' -> '{}'".format(description, new_description))

        db.sql('UPDATE `objects` SET `description` = "{}" WHERE `institution_name` = "The National Museum of World Cultures" AND `object_number` = "{}";'.format(escape(new_description), object_number), result_format="csv")

if __name__ == "__main__":
    main()
