import fiona
from collections import OrderedDict
from fiona.crs import from_epsg
from shapely.geometry import Polygon


with fiona.open("../data/ne_10m_urban_areas/ne_10m_urban_areas.shp") as src:

    print(src.meta)
    print(src.meta['driver'])
    print(src.meta['schema']['properties']['scalerank'])
    print(src.meta['schema']['properties']['featurecla'])
    print(src.meta['schema']['properties']['area_sqkm'])
    print(src.meta['schema']['properties']['min_zoom'])
    print(src.meta['schema']['geometry'])
    # ...etc
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
p = Polygon([(0,0),(0,11),(11,11),(11,0)])
print(p.__dict__)
poly = {
    'type': 'Polygon',
    'coordinates': [[
        (1179091.1646903288, 712782.8838459781),
        (1161053.0218226474, 667456.2684348812),
        (1214704.933941905, 641092.8288590391),
        (1228580.428455506, 682719.3123998424),
        (1218405.0658121984, 721108.1805541387),
        (1179091.1646903288, 712782.8838459781) ]]}
sch = {
    'geometry': 'Polygon',
    'type':'str',
    'coordinates':'list',
    'properties': OrderedDict([
                ('id', 4),
                ('objectid', 5)])
}

crs = from_epsg(25831)



with fiona.open('test.geojson','w',driver="GeoJSON",schema=sch,crs=crs) as dst:
    dst.write(poly)
    dst.write(p)
