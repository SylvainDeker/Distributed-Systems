import fiona
from collections import OrderedDict
from fiona.crs import from_epsg
from shapely.geometry import Polygon
import pprint

crs = from_epsg(25831)

schema = {  'geometry':'Polygon',
            'properties': OrderedDict([
                ('name', 'str'),
                ('height', 'float'),
                ('view', 'str'),
                ('year', 'int')
            ])
        }

test1 = {
        'geometry': {
            'type':'Polygon',
            'coordinates': [[(0,0),(11,11)]]
        },
        'properties': OrderedDict([
            ('name', 'Eiffel Tower'),
            ('height', 300.01),
            ('view', 'divedown'),
            ('year', 1889)
        ])
}

with fiona.open("res.shp",mode="w",driver="ESRI Shapefile",schema=schema,crs=crs) as dst:
    dst.write(test1)


with fiona.open("res.shp") as src:
    pprint.pprint(src[0])
