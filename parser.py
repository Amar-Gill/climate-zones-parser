# parser for koppen-geiger map coordinates files
# input is name of file
# output is one file per cz in the form of array of objects

import sys

inFile = sys.argv[1]

climate_zones = ["Af", "Am", "As", "Aw", "BWk", "BWh", "BSk", "BSh", "Cfa", "Cfb", "Cfc", "Csa", "Csb", "Csc", "Cwa", "Cwb", "Cwc", "Dfa", "Dfb", "Dfc", "Dfd", "Dsa", "Dsb", "Dsc", "Dsd", "Dwa", "Dwb", "Dwc", "Dwd", "EF", "ET"]

def parse(cz):
    outFile = f'{sys.argv[1][0:-4]}_{cz}.js'

    with open(inFile, 'r') as inf, open(outFile, 'w') as outf:

        outf.write("export default [")
        outf.write('\n')
        active_zone = False

        for line in inf:
            line = line.split()

            if cz == line[2]:
                if not active_zone:
                    outf.write("[\n")
                active_zone = True
            else:
                if active_zone:
                    outf.write("],\n")
                active_zone = False
            if active_zone:
                output_line = "{" + f'lat: {line[0]}, lng: {line[1]}' + "},"
                outf.write(output_line)
                outf.write('\n')
        
        outf.write("]")

for zone in climate_zones:
    parse(zone)
    