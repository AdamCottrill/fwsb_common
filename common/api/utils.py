"""
=============================================================
~/uglmu_common/common/api/utils.py
 Created: 19 Apr 2020 08:52:11

 Description:

  Some utility functions that are used in the uglmu common application.

 A. Cottrill
=============================================================
"""

from django.contrib.gis.geos import Point, GEOSGeometry


def parse_point(data):
    """A helper function used by the spatial lookup api views to convert
    the reqest data to a GEOSGeometry Point object.  If it cannot be
    coerced to a Point object return None.

    TODOs:

    + consider including a meaningful error message if it cannot be
    converted to geometry object, or is not a Point.


    """

    if data is None:
        return None

    try:
        pt = GEOSGeometry(data, srid=4326)
    except:
        # the data could not be converted to a valid geometry object
        return None

    if isinstance(pt, Point):
        return pt
    else:
        # the data was not a valid Point in either geojson or wkt
        return None
