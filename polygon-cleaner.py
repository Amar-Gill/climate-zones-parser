# this file removes any polygons that are less than 4 data points in length

import sys
import json

inFile = sys.argv[1]
outFile = 'cleaned.geojson'

with open(inFile, 'r') as inf:
    cz_dict = json.load(inf)

for feature in cz_dict['features']:
    cleaned_coordinates = [polygon for polygon in feature['geometry']['coordinates'] if len(polygon[0]) > 3]
    feature['geometry']['coordinates'] = cleaned_coordinates

with open(outFile, 'w') as outf:
    json.dump(cz_dict, outf)