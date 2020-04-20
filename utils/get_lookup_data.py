"""
=============================================================
~/uglmu_common/utils/get_lookup_data.py
Created: 02 Jul 2019 14:46:33

DESCRIPTION:

Get data from lookup tables and populate the models in common app.

A. Cottrill
=============================================================
"""

from collections import namedtuple
import pyodbc

import django_settings

from common.models import Lake, Species, Grid5, ManagementUnit

MDB = "C:\\1work\\Data_Warehouse\\LookupTables.accdb"


# ====================================
#             LAKES

lakes = [
    ("Lake Huron", "HU"),
    ("Lake Superior", "SU"),
    ("Lake Erie", "ER"),
    ("Lake Ontario", "ON"),
    ("Lake St. Clare", "SC"),
]

items = []
for lake in lakes:
    items.append(Lake(lake_name=lake[0], abbrev=lake[1]))
Lake.objects.bulk_create(items)


print("Done adding lakes.")

# ====================================
#             SPECIES

conString = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}"
# connect using pyodbc
conn = pyodbc.connect(conString.format(MDB))
cursor = conn.cursor()

sql = """select SPC, SPC_LAB, SPC_NM, SPC_NMCO, SPC_NMSC, SPC_NMFAM,
COMMENT from [SPC] where [SPC_LAB] is not null order by [SPC]"""

cursor.execute(sql)

colnames = [x[0].lower() for x in cursor.description]

rs = cursor.fetchall()

items = []
for row in rs:
    item = {k: v for k, v in zip(colnames, row)}
    items.append(Species(**item))

Species.objects.bulk_create(items)

print("Done adding Species.")


# ====================================
#     5-MINUTE GRIDS

# NOTE: Someday, these should be read in from a shapefile so that we
# can capture their geometries.

huron = Lake.objects.get(abbrev="HU")
# HURON GRIDS

sql = """select GRID from [Grid_Lookup]"""

cursor.execute(sql)

colnames = [x[0].lower() for x in cursor.description]

rs = cursor.fetchall()

items = []
for row in rs:
    item = dict()
    item["grid"] = int(row[0])
    item["lake"] = huron
    item["slug"] = "{}-{:04d}".format(huron.abbrev, int(row[0]))
    items.append(Grid5(**item))

Grid5.objects.bulk_create(items)

print("Done adding Huron Grids.")

##====================================

# MANAGEMENT UNITS:

# In the grid lookup table, there is a column for each management unit
# type.  we will create list of tuples containing the column name and
# manaagement unit type, Then for each MU, get the list of distinct
# values, create each one, and associate it with the appropriate list
# of 5-minute grids.

mu_attr = namedtuple("mu_attr", "fieldname, mu_type")

mus = [
    mu_attr("LTRZ", "ltrz"),
    mu_attr("LTRZ_buffer", "bltrz"),
    mu_attr("QUOTA_ZONE", "qma"),
    mu_attr("ASSESS_ARE", "aa"),
    mu_attr("AREA", "area"),
    mu_attr("SUB_AREA", "subarea"),
    mu_attr("STAT_DIST", "stat_dist"),
    mu_attr("MOE", "moe"),
    mu_attr("BASIN", "basin"),
    mu_attr("NAZ", "naz"),
    mu_attr("US_GRID_NO", "grid10")
    # ("", "region")  #these don't exist anywhere at the moment.
]

for mu in mus:

    sql1 = """select distinct [{0.fieldname}] from [Grid_lookup]
              where [{0.fieldname}] is not null order by [{0.fieldname}] ;"""

    cursor.execute(sql1.format(mu))
    rs = cursor.fetchall()

    for manUnit in rs:

        print("creating {} - {} ...".format(mu.fieldname, manUnit[0]))
        # get the grids associated with each of our mus:

        sql2 = (
            "select [{0.fieldname}], [GRID] from [Grid_lookup]"
            + "where [{0.fieldname}] is not null;"
        )
        cursor.execute(sql2.format(mu))
        rs2 = cursor.fetchall()
        # create a dictionary that has a list grids of each qma:
        grid_lookup = dict()
        for rec in rs2:
            if grid_lookup.get(rec[0]):
                tmp = grid_lookup.get(rec[0])
                tmp.append(rec[1])
                grid_lookup[rec[0]] = tmp
            else:
                grid_lookup[rec[0]] = [rec[1]]

        grid5s = Grid5.objects.filter(grid__in=grid_lookup[manUnit[0]]).values_list(
            "pk"
        )

        # create our managment unit:
        new_mu, created = ManagementUnit.objects.get_or_create(
            lake=huron, label=manUnit[0], mu_type=mu.mu_type
        )
        new_mu.save()
        new_mu.grids.add(*[x[0] for x in grid5s])
        new_mu.save()
