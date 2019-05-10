import gmplot
import pandas
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import radians, cos, sin, asin, sqrt
from descartes.patch import PolygonPatch
import numpy
import math
import os, sys

path = os.path.dirname(sys.argv[0])


# Haversine Formula #
def haversine(long1, lat1, long2, lat2):
    # convert decimal degrees to radians
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    # haversine formula
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # the radius of the earth in miles
    return c * r


# Place map
gmap = gmplot.GoogleMapPlotter(35.14, -85.17, 11)

gridCoords = pandas.read_csv("../Excel & CSV Sheets/VerticesPoints.csv")
# print(gridCoords.head())

# This will hold the polygon versions of our grid blocks
# The final length of this should be 1100, since we have 1100 blocks
gridLayout_Coords = []


# Places the first 5 coordinates in the file as pins, represents the first grid block seen in Connor's diagram
# for i, value in enumerate(gridCoords.values[0:5]):
#     lat = gridCoords.Y.values[i]
#     long = gridCoords.X.values[i]
#     gmap.marker(lat, long, '#FF0000', title=i)

# Drawing the grid blocks on a gmap
for i, value in enumerate(gridCoords.values):
    if i % 5 == 0:
        # Drawing the block grid
        # We only draw on each 5th iteration, since each grid block's coordinates are grouped by 5
        # grid_lats, grid_longs = zip(*[(gridCoords.Y.values[i], gridCoords.X.values[i]),
        #                                     (gridCoords.Y.values[i+1], gridCoords.X.values[i+1]),
        #                                     (gridCoords.Y.values[i+2], gridCoords.X.values[i+2]),
        #                                     (gridCoords.Y.values[i+3], gridCoords.X.values[i+3]),
        #                                     (gridCoords.Y.values[i+4], gridCoords.X.values[i+4])])
        # gmap.plot(grid_lats, grid_longs, 'cornflowerblue', edge_width=5)

        # Making the actual polygon using the coordinates above
        poly_coords = ((gridCoords.Y.values[i], gridCoords.X.values[i]),
                                                (gridCoords.Y.values[i+1], gridCoords.X.values[i+1]),
                                                (gridCoords.Y.values[i+2], gridCoords.X.values[i+2]),
                                                (gridCoords.Y.values[i+3], gridCoords.X.values[i+3]),
                                                (gridCoords.Y.values[i+4], gridCoords.X.values[i+4]))
        gridLayout_Coords.append(poly_coords)
        # print(len(gridLayout_Coords))

calldata = pandas.read_csv("../Excel & CSV Sheets/Full Data Grid.csv", sep=",")
for j in range(0, len(gridLayout_Coords)):
    poly = Polygon(gridLayout_Coords[j])
    print(j)
    # take in the 911 incident lat and long one at a time
    for o, value2 in enumerate(calldata.values):
        call_lat = calldata.Latitude.values[o]
        call_long = calldata.Longitude.values[o]
        call_incident = Point(call_lat, call_long)
        # See if the 911 incident is in the current polygon (representing a weather station)
        if poly.contains(call_incident):
            calldata.Grid_Block.values[o] = j
        else:
            pass
calldata.to_csv("../Excel & CSV Sheets/Full Data Grid.csv")
# gmap.draw("Chattanooga Polygons.html")
