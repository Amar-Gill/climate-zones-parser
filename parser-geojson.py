# parser for koppen-geiger map coordinates files
# input is name of file
# output is one file per cz in the form of array of objects

import sys

inFile = sys.argv[1]
outFile = 'test_output.geojson'

climate_zones = ["Af", "Am", "As", "Aw", "BWk", "BWh", "BSk", "BSh", "Cfa", "Cfb", "Cfc", "Csa", "Csb", "Csc",
                 "Cwa", "Cwb", "Cwc", "Dfa", "Dfb", "Dfc", "Dfd", "Dsa", "Dsb", "Dsc", "Dsd", "Dwa", "Dwb", "Dwc", "Dwd", "EF", "ET"]

# needs to write array of mult


def parse(cz):
    inf.seek(0)

    message = '{' \
                '"type": "Feature",' \
                '"properties": {' \
                    '"dank_level": 420,' \
                    f'"climate_zone": "{cz}"' \
                '},' \
                '"geometry": {' \
                    '"type": "MultiPolygon",' \
                    '"coordinates": ['
    
    outf.write(message)

    active_zone = False

    for line in inf:
        line = line.split()

        if cz == line[2]:
            if not active_zone:
                outf.write("[[\n")
            active_zone = True
        else:
            if active_zone:
                outf.write("]],\n")
            active_zone = False
        if active_zone:
            output_line = "[" + f'{line[1]}, {line[0]}' + "],"
            outf.write(output_line)
            outf.write('\n')

    outf.write("] } },")


with open(inFile, 'r') as inf, open(outFile, 'w') as outf:

    initial = '{"type": "FeatureCollection","name": "Building_Climate_Zones","crs": {"type": "name","properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"} },"features": ['
    outf.write(initial)

    for zone in climate_zones:
        parse(zone)

    outf.write("]}")
