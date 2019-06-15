import numpy
import pandas


# gridblocks = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/GridInfoCutandUpdated.csv")
# terrain = pandas.read_csv("/Users/pete/Downloads/TerrainRoadData.csv", dtype={'OBJECTID':int, 'Highway_1':int, 'Land_Use_Mode':int, 'Segment_Count':int,
#  'Road_Count': int, 'Terrain':int, 'Short_Terrain':int})
# print(terrain.dtypes)


road_info = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Info.csv")
grid_data = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid Oriented Small Data 2017+2018_AllTemp.csv")
for j, info in enumerate(grid_data.values):
    print(j)
    for i, stuff in enumerate(road_info.values):
        if grid_data.Grid_Block.values[j] == road_info.ORIG_FID.values[i]:
            grid_data.Road_Count.values[j] = int(road_info.Road_Count.values[i])
            grid_data.Highway.values[j] = int(road_info.Highway.values[i])
            grid_data.Land_Use_Mode.values[j] = int(road_info.Land_Use_Mode.values[i])
            grid_data.Grid_Col.values[j] = road_info.Col_Num.values[i]
            grid_data.Grid_Row.values[j] = road_info.Row_Num.values[i]
    if j % 20000 == 0:
        print("Saving at:", j)
        grid_data.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid Oriented Small Data 2017+2018.csv")
grid_data.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid Oriented Small Data 2017+2018.csv")
exit()

# for i, info in enumerate(gridblocks.values): 
#     stuff = terrain.values[i]
#     stuffcut = stuff[0:5]
#     # print(stuffcut, info[0])
# #     if info != stuffcut:
# #         print("Numbers don't match at :", info[0], stuffcut[0])
# #     else: 
# #         pass
# # exit()
#     if (info != stuffcut).all(): 
#         print("Found Error", info[0], info, " ", stuffcut)
#     else:
#         pass
# exit()


#### Setting Grid Blocks for the original grid block setup. 
a = list(range(1100))
a = numpy.reshape(a, (25, 44))
a = list(a+1)

gridblocks = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Forecast Forum Original.csv")
for i, info in enumerate(gridblocks.values):
    for j,k in enumerate(a):
        k = list(k)
        for l in enumerate(k):
            if gridblocks.Grid_Block.values[i] == l[1]:
                col = l[0]
                row = int(l[1]/44)
                print(i, col, row)
                gridblocks.Grid_Col.values[i] = col
                gridblocks.Grid_Row.values[i] = row
gridblocks.to_csv('../Excel & CSV Sheets/Grid Layout Test Files/Forecast Forum Original.csv')
exit()

# roadfile = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/GridCountRoads.csv")
# highwayfile = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Highway.csv")
# blockstodrop = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/BlocksToDrop.csv")
# gridinfo = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/GridInfo.csv")
# gridblocks = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")


# print(roadfile.head())
# print(highwayfile.head())
# print(blockstodrop.head())

def droppingGridblocks(blockstodrop, gridblocks):
    gridblockscopy = gridblocks.copy()
    for i, info in enumerate(gridblocks.values):
        for k, thing in enumerate(blockstodrop.values):
            if blockstodrop.Grid_Block.values[k] == gridblocks.Grid_Block.values[i]:
                # print("Dropping : ", blockstodrop.Grid_Block.values[k], gridblocks.Grid_Block.values[i])
                gridblockscopy = gridblockscopy.drop([i],axis=0)
    return gridblockscopy

def updateTimeframe(gridblocks):
    for i, info in enumerate(gridblocks.values):
        if (gridblocks.Hour.values[i] < 7 or gridblocks.Hour.values[i] > 19):  
            gridblocks.DayFrame.values[i] = 1
        elif (gridblocks.Hour.values[i] < 10 and gridblocks.Hour.values[i] > 7):
            gridblocks.DayFrame.values[i] = 2
        elif (gridblocks.Hour.values[i] < 13 and gridblocks.Hour.values[i] > 10):
            gridblocks.DayFrame.values[i] = 3
        elif (gridblocks.Hour.values[i] < 19 and gridblocks.Hour.values[i] > 13):
            gridblocks.DayFrame.values[i] = 4   
        if i % 1000 == 0:
            print(i)
    return gridblocks

# print(len(highwayfile))
# cuthighway = droppingGridblocks(blockstodrop, highwayfile)
# print(len(cuthighway))

# print(len(roadfile))
# cutroad = droppingGridblocks(blockstodrop, roadfile)
# print(len(cutroad))

# print(len(gridinfo))
# gridinfocut = droppingGridblocks(blockstodrop, gridinfo)
# print(len(gridinfocut))


# for j, info in enumerate(gridinfo.values): 
#     print(j)
#     for i, stuff in enumerate(roadfile.values):
#         if gridinfo.Grid_Block.values[j] == roadfile.Grid_Block.values[i]:
#             gridinfo.Road_Count.values[j] = int(roadfile.Road_Count.values[i])

# print(gridinfo.head())
# gridinfocut = droppingGridblocks(blockstodrop, gridinfo)
# gridinfocut.to_csv('../Excel & CSV Sheets/Grid Layout Test Files/GridInfoCutandUpdated.csv')


# gridblocks = updateTimeframe(gridblocks)
# gridblockscopy = gridblocks.copy()
# print(len(gridblocks))
# for i, info in enumerate(gridblocks.values):
#     # print(i)
#     if gridblocks.TravelDay.values[i] == 1:
#         gridblockscopy = gridblockscopy.drop([i],axis=0)
#     if i % 1000 == 0:
#         print(i)
# print(len(gridblockscopy))
# gridblockscopy.to_csv('../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018 Test.csv')

gridblocks = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018 Test.csv")
gridblocks = gridblockscopy = gridblockscopy.drop(['Month'],axis=1)
gridblocks.to_csv('../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018 Test.csv')