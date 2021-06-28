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

# pg connections parameters
con_pars = {
    "HOST": "localhost",
    "NAME": "gldjango",
    "USER": os.getenv("PGUSER"),
    "PASSWORD": os.getenv("PGPASS"),
}

pg_constring = """host='{HOST}' dbname='{NAME}' user='{USER}'
                  password='{PASSWORD}'"""
pg_constring = pg_constring.format(**con_pars)


shapefiles = [
    #   Lake Huron
    dict(
        shpfile="C:/Users/COTTRILLAD/1work/Databases/GIS_ShapeFiles/LH_5min_grid.shp",
        abbrev="hu",
        srid="4269",
        labelIndex=1,
    ),
    #    Lake Superior
    #    dict(
    #        shpfile="C:/Users/COTTRILLAD/1work/Superior/Grids_Management_Units/New folder/LS_5min_grid.shp",
    #        abbrev="su",
    #        srid="93161",  #
    #        labelIndex=3,
    #    )
]


sql1 = """Update common_grid5 set
         geom=st_simplify(ST_transform(ST_SETSRID(ST_MULTI(ST_GeomFromGeoJSON('{}')), {}), 4326),
0.00001)
         where slug='{}';"""

pg_conn = psycopg2.connect(pg_constring)
pg_cur = pg_conn.cursor()


for lake in shapefiles:

    shpfile = lake.get("shpfile")
    labelIndex = lake.get("labelIndex")
    spatialRef = lake.get("srid")
    abbrev = lake.get("abbrev")
    print("adding Grids for {}".format(abbrev))

    sf = shapefile.Reader(shpfile)
    for i, record in enumerate(sf.records()):
        grid_no = record[labelIndex]
        slug = "{}_{}".format(abbrev.lower(), f"{grid_no:0004}")  # left padded
        print("\t", record, slug)
        geoj = sf.shape(i).__geo_interface__
        pg_cur.execute(sql1.format(json.dumps(geoj), spatialRef, slug))

    pg_conn.commit()

# check for any gri10 objects that still have an empty geom.
sql2 = "select slug from common_grid5 where geom is null;"
pg_cur.execute(sql2)
rs = pg_cur.fetchall()
if len(rs):
    print("Oh-oh - there are still {} grids without geometries!".format(len(rs)))
    print("for example:")
    for x in rs[:10]:
        print(x)

pg_conn.close()
