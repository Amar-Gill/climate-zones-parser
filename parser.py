# parser for koppen-geiger map coordinates files
# input is name of file
# output is geojson file with separate feature for each cz implemented using Geometry type: MultiPolygon

import sys
import json

inFile = sys.argv[1]
outFile = f'{sys.argv[1][0:-4]}.geojson'
outFile2 = f'{sys.argv[1][0:-4]}-metadata.csv'

climate_zones = ["Af", "Am", "As", "Aw", "BWk", "BWh", "BSk", "BSh", "Cfa", "Cfb", "Cfc", "Csa", "Csb", "Csc",
                 "Cwa", "Cwb", "Cwc", "Dfa", "Dfb", "Dfc", "Dfd", "Dsa", "Dsb", "Dsc", "Dsd", "Dwa", "Dwb", "Dwc", "Dwd", "EF", "ET"]

main_climates = {
    "A": "equatorial",
    "B": "arid",
    "C": "warm temperate",
    "D": "snow",
    "E": "polar"
}

precipitation = {
    "W": "desert",
    "S": "steppe",
    "f": "fully humid",
    "s": "summer dry",
    "w": "winter dry",
    "m": "monsoonal"
}

temperature = {
    "h": "hot arid",
    "k": "cold arid",
    "a": "hot summer",
    "b": "warm summer",
    "c": "cool summer",
    "d": "extremely continental",
    "F": "polar frost",
    "T": "polar tundra"
}

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

# load dict
def load_features(cz):

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
    # first pass - return sequence for polygon of a cz
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


# analyze_features
# pass 2 - output length of multi-polygon nodes comrpising each cz
# accept geojson feature dataformat
def analyze_features(features):
    for feature in features:
        climate_zone = feature['properties']['climate_zone']
        
        polygon_count = len(feature['geometry']['coordinates'])

        for polygon in feature['geometry']['coordinates']:
            polygon_length = len(polygon[0])
            print('climate_zone: ' + climate_zone + ' - polygon_nodes: ' + f'{polygon_length}' )

        feature['properties']['polygon_count'] = polygon_count
        feature['properties']['main_climate'] = main_climates[climate_zone[0]]

        # if not climate_zone[0] == "E":
        #     feature['properties']['precipitation'] = precipitation[climate_zone[1]]

        # if not climate_zone[0] == "A":
        #     feature['properties']['temperature'] = temperature[climate_zone[2]]

# write geojson
with open(inFile, 'r') as inf, open(outFile, 'w') as outf:

    for zone in climate_zones:
        load_features(zone)

    analyze_features(output_dict['features'])

    json.dump(output_dict, outf)
