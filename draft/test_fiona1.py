import fiona
from collections import OrderedDict
from fiona.crs import from_epsg
from shapely.geometry import Polygon
import pprint

with fiona.open("../data/ne_10m_urban_areas/ne_10m_urban_areas.shp") as src:
    pprint.pprint(src[1]) # It's a 'record', A record has an id key.
    pprint.pprint(src[1]['id']) # A record has an id key.
    pprint.pprint(src[1]['properties']) #  The keys of the properties mapping are the same as the keys of the properties mapping in the schema
    # TODO 1.5.3

    print(src.driver) # OGR format driver used to open file
    print(src.crs)
    print(src.bounds) # The minimum bounding rectangle (MBR) or bounds of the collection’s records
    print(src.schema) # A vector file has a single type of record,It has ‘geometry’ and ‘properties’ items. The former is a string and the latter is an ordered dict with items having the same order as the fields in the data file.

# The default width is 80 chars, which means ‘str’ and ‘str:80’ are more or less equivalent.

# Schema’s geometry item will be one of the following:
#    Point
#    LineString
#    Polygon
#    MultiPoint
#    MultiLineString
#    MultiPolygon
#    GeometryCollection
#    3D Point
#    3D LineString
#    3D Polygon
#    3D MultiPoint
#    3D MultiLineString
#    3D MultiPolygon
#    3D GeometryCollection


# /!\ Esri’s Shapefile, has no ‘MultiLineString’ or ‘MultiPolygon’ schema geometries. However, a Shapefile that indicates ‘Polygon’ in its schema may yield either ‘Polygon’ or ‘MultiPolygon’ features.


# A record you get from a collection is a Python dict, the values in the fields are typed properly for the type of record.
