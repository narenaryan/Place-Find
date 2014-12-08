from __future__ import division
from settings import show_first

from osgeo import ogr
import shapely.geometry
import shapely.wkt



shapefile = ogr.Open("tl_2014_us_cbsa.shp")
layer = shapefile.GetLayer(0)
#code for displaying and as

city = raw_input('\nEnter ISO2 code of city: ')

print '\nSelect category of place to search in and around the city\n'
for index,place in show_first.items():
	print '||%s|||||||%s'%(index,place)

place_choice = int(raw_input('\nEnter code of place from above listing: '))
place = show_first[place_choice]

distance = int(raw_input('\nEnter with in range distance(KM) to find %s: '%place))

#converting distance range to angular distance $$$$ 100 KM = 1 Degree $$$
MAX_DISTANCE = distance/100 # Angular distance; approx 10 km.
print "Loading urban areas..."

# Maps area name to Shapely polygon.
urbanAreas = {} 

for i in range(layer.GetFeatureCount()):
	feature = layer.GetFeature(i)
	name = feature.GetField("NAME")
	geometry = feature.GetGeometryRef()
	shape = shapely.wkt.loads(geometry.ExportToWkt())
	dilatedShape = shape.buffer(MAX_DISTANCE)
	urbanAreas[name] = dilatedShape

print "Checking %ss..."%place


f = open("NationalFile_20141005.txt", "r")
result = {}

for line in f.readlines():
	chunks = line.rstrip().split("|")
	if chunks[2] == place and chunks[3] == city:
		parkName = chunks[1]
		latitude = float(chunks[9])
		longitude = float(chunks[10])
		pt = shapely.geometry.Point(longitude, latitude)
		for urbanName,urbanArea in urbanAreas.items():
			if urbanArea.contains(pt):
				if not result.has_key(parkName):
					result[parkName]=[urbanName]
				else:
					result[parkName].append(urbanName)


print '\n---------------------%s--------------------\n'%place
for k,v in result.items():
	print k,'\n','=========================='
	for item in v:
		print item
	print '\n\n'
f.close()


