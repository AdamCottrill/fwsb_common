"""=============================================================
~/geopy/get_grid_geoms_from_shapefiles.py
 Created: 10 Oct 2019 14:45:56

 DESCRIPTION:

  This script reads geometries from 10-minute grid shapefile for each
  of the 5 great lakes and updates the geometry of each grid on FSDViz database.

  Grids are trasformed to srid=4326 by postgis when they are saved. A
  small snippet at the bottom of the script reports the number of grid10
  objects in fsdviz that still do not have a geomtry object.

 A. Cottrill
=============================================================

"""


import json
import os
import psycopg2
import shapefile

# the location of our source shapefiles and associated output

SHP_SRC = (
    "c:/Users/COTTRILLAD/1work/LakeTrout/Stocking/GLFSD_Datavis/shapefiles/10min_grids"
)

# pg connections parameters
con_pars = {
    "HOST": "localhost",
    "NAME": "fsdviz",
    "USER": "cottrillad",
    "PASSWORD": os.getenv("PGPASS", "password"),
}

pg_constring = """host='{HOST}' dbname='{NAME}' user='{USER}'
                  password='{PASSWORD}'"""
pg_constring = pg_constring.format(**con_pars)


shapefiles = [
    # Lake Huron
    dict(
        shpfile="Huron/lh_10min_grids_shrln_IFR.shp",
        abbrev="hu",
        srid="4269",
        labelIndex=0,
    ),
    # Lake Erie
    dict(
        shpfile="Erie/le_10min_grid_cells_IFR.shp",
        abbrev="er",
        srid="4269",
        labelIndex=0,
    ),
    # Lake Michigan
    dict(shpfile="Michigan/statgrd_10min.shp", abbrev="mi", srid="26916", labelIndex=0),
    # Lake Ontario
    dict(
        shpfile="Ontario/lo_10min_grids_shrln_IFR.shp",
        abbrev="on",
        srid="4269",
        labelIndex=0,
    ),
    # Lake Superior
    dict(
        shpfile="Superior/ls_10min_grids_shrln_IFR.shp",
        abbrev="su",
        srid="4269",
        labelIndex=0,
    ),
    #    # Lake St Clair
    #    dict(shpfile="SC_MI.shp", srid='4269', labelIndex=8),
    #    dict(shpfile="SC_ON.shp", srid='4269', labelIndex=8)
]


sql1 = """Update common_grid10 set
         geom=ST_transform(ST_SETSRID(ST_MULTI(ST_GeomFromGeoJSON('{}')), {}), 4326)
         where slug='{}';"""

pg_conn = psycopg2.connect(pg_constring)
pg_cur = pg_conn.cursor()


for lake in shapefiles:

    shpfile = os.path.join(SHP_SRC, lake.get("shpfile"))
    labelIndex = lake.get("labelIndex")
    spatialRef = lake.get("srid")
    abbrev = lake.get("abbrev")
    print("adding Grids for {}".format(abbrev))

    sf = shapefile.Reader(shpfile)
    for i, record in enumerate(sf.records()):
        grid_no = record[labelIndex]
        slug = "{}_{}".format(abbrev, grid_no)
        print("\t", record, slug)
        geoj = sf.shape(i).__geo_interface__
        pg_cur.execute(sql1.format(json.dumps(geoj), spatialRef, slug))

    pg_conn.commit()

# check for any gri10 objects that still have an empty geom.
sql2 = "select slug from common_grid10 where geom is null;"
pg_cur.execute(sql2)
rs = pg_cur.fetchall()
if len(rs):
    print("Oh-oh - there are still {} grids without geometries!".format(len(rs)))
    print("for example:")
    for x in rs[:10]:
        print(x)

# pg_conn.close()
