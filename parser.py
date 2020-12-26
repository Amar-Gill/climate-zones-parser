# parser for koppen-geiger map coordinates files
# input is name of file
# output is geojson file with separate feature for each cz implemented using Geometry type: MultiPolygon

import sys
import json

inFile = sys.argv[1]
outFile = 'test_output.geojson'

climate_zones = ["Af", "Am", "As", "Aw", "BWk", "BWh", "BSk", "BSh", "Cfa", "Cfb", "Cfc", "Csa", "Csb", "Csc",
                 "Cwa", "Cwb", "Cwc", "Dfa", "Dfb", "Dfc", "Dfd", "Dsa", "Dsb", "Dsc", "Dsd", "Dwa", "Dwb", "Dwc", "Dwd", "EF", "ET"]

output_dict = {
    "type": "FeatureCollection",
    "name": "Koeppen Geiger Climate Classifications",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": []
}


def parse(cz):

    feature = {
        "type": "Feature",
        "properties": {
            "climate_zone": cz
        },
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": []
        }
    }

    # begin parsing
    inf.seek(0)

    is_polygon = False
    polygon_index = 0 

    for line in inf:
        line = line.split()

        if cz == line[2]:
            if not is_polygon:
                feature["geometry"]["coordinates"].append([[]])
            is_polygon = True

        else:
            if is_polygon:
                polygon_index += 1
            is_polygon = False

        if is_polygon:
            feature["geometry"]["coordinates"][polygon_index][0].append([
                                                                             line[1], line[0]])

    # end of parsing

    output_dict["features"].append(feature)


with open(inFile, 'r') as inf, open(outFile, 'w') as outf:

    for zone in climate_zones:
        parse(zone)

    json.dump(output_dict, outf)
