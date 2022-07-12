#!/usr/bin/python3

import doltcli as dolt

def main():
    db = dolt.Dolt("/root/data/museum-collections/")

    sql1 = 'SELECT `institution_name`, COUNT(*) FROM `objects` WHERE `source_1` LIKE "%ehive%" GROUP BY `institution_name`;'
    print(sql1)

    res = db.sql(sql1, result_format="csv")

    for row in res:
        institution_name = row["institution_name"]
        count = int(row["COUNT(*)"])

        if "Archive" in institution_name or count < 25:
            sql2 = 'DELETE FROM `objects` WHERE `institution_name` = "{}"'.format(institution_name)
            print(sql2)
            db.sql(sql2, result_format="csv")

if __name__ == "__main__":
    main()

