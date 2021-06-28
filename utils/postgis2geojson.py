import os

os.chdir("C:/Users/COTTRILLAD/Documents/1work/ScrapBook/fsdviz_geojson")

pars = {
    "PG_HOST": "localhost",
    "PG_DBASE": "fsdviz",
    "PG_PASS": os.getenv("PG_PASS"),
    "PG_USER": os.getenv("PG_USER"),
}


cmd0 = 'C:/OSGeo4w/bin/ogr2ogr.exe -f GeoJSON {lake}.json  -t_srs EPSG:4326 "PG:host={PG_HOST} dbname={PG_DBASE} user={PG_USER} password={PG_PASS}" -sql "{sql}"'

lakes = ["HU", "SU", "ER", "ON", "MI", "SC"]

for lake in lakes:
    sql = "select shoreline as {lake} from common_lake where abbrev='{lake}'"
    pars["lake"] = lake
    pars["sql"] = sql.format(**pars)

    cmd = cmd0.format(**pars)
    fname = "{lake}.json".format(**pars)
    try:
        os.remove(fname)
    except OSError:
        pass
    os.system(cmd)

print("Done exporting lake geoms!")

slugs = ["hu_on", "su_on", "er_on", "on_on", "sc_on"]

for slug in slugs:
    sql = "select geom as geom_ontario from common_juristiction where slug='{}'"
    pars["sql"] = sql.format(slug)

    cmd = cmd0.format(**pars)
    fname = "{}.json".format(slug)
    try:
        os.remove(fname)
    except OSError:
        pass
    os.system(cmd)

print("Done exporting geom_ontario polygons!")


print("Done!")


# compbine out individual json files into a single topojson file with
# each lake as a layer:

# geo2topo -o  <output> <input...>
# geo2topo -o  basin.geo.json SU.json HU.json MI.json SC.json ER.json ON.json

# toposimplify -p 0.00001 -f < basin.geo.json > basin-simple.top.json


# now repeat for each lake - with the consitutent jurisdictions

# IMPORTING


pars = {
    "PG_HOST": "localhost",
    "PG_DBASE": "glbdjango",
    "PG_PASS": os.getenv("PG_PASS"),
    "PG_USER": os.getenv("PG_USER"),
}


cmd0 = 'C:/OSGeo4w/bin/ogr2ogr.exe -f "PostgreSQL" PG:"host={PG_HOST} dbname={PG_DBASE} user={PG_USER} password={PG_PASS}" "{src_file}" -nln tmpgeom '

pars[
    "src_file"
] = "c:/Users/COTTRILLAD/1work/Python/djcode/uglmu_common/utils/geojson/sc_on.json"
cmd = cmd0.format(**pars)
os.system(cmd)


# LAKE ST CLARE:


pars[
    "src_file"
] = "c:/Users/COTTRILLAD/1work/Python/djcode/uglmu_common/utils/geojson/SC.json"
cmd = cmd0.format(**pars)
os.system(cmd)

sql = "update common_lake set geom = (select wkb_geometry from tmpgeom) where common_lake.abbrev='SC';"
