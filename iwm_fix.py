#!/usr/bin/python3

import doltcli as dolt


def main():
    db = dolt.Dolt("/root/data/museum-collections/")

    sql1 = 'SELECT * FROM `objects` WHERE `institution_name` = "Imperial War Museum" AND `accession_number` IS NOT NULL;'
    print(sql1)

    res = db.sql(sql1, result_format="csv")

    for row in res:
        a_n = row["accession_number"]
        o_n = row["object_number"]

        sql2 = 'SELECT COUNT(*) FROM `objects` WHERE `object_number` = "{}" AND `institution_name` = "Imperial War Museum"'.format(
            a_n
        )
        res2 = db.sql(sql2, result_format="csv")

        count = res2[0]["COUNT(*)"]

        if count != 0:
            sql3 = 'DELETE FROM `objects` WHERE `institution_name` = "Imperial War Museum" AND `accession_number` = "{}"'.format(
                a_n
            )
            db.sql(sql3, result_format="csv")
        else:
            sql3 = 'UPDATE `objects` SET `object_number` = `accession_number`, `accession_number` = NULL WHERE `institution_name` = "Imperial War Museum" AND `object_number` = "{}"'.format(
                o_n
            )
            db.sql(sql3, result_format="csv")


if __name__ == "__main__":
    main()
