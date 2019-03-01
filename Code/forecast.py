import matplotlib
import matplotlib.pyplot as plt
import numpy
import imaplib
import os
from datetime import datetime, timedelta, date, time
import time
from darksky import forecast
import pytz
import pandas
import math
import os, sys
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras import callbacks
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from os.path import exists
# import datetime
from selenium import webdriver
import schedule


# now = datetime.datetime.now()
hotspots = pandas.read_csv("../Excel & CSV Sheets/Jan28Feb28Hotspotsabove5.csv", sep=",")
# forecast = pandas.read_csv("../Excel & CSV Sheets/2019-02-25_08_forecast_accidents.csv", sep=",")
# monday = pandas.read_excel("../Excel & CSV Sheets/2019 Data/Final Form Reports/911_Reports_for_2019-02-25_FinalForm.xlsx")
# dataset = shuffle(dataset)
# dataset = shuffle(dataset)
#
# columns = ('Log_Mile','Hour','Temperature','Temp_Max','Temp_Min','Dewpoint','Humidity','Month',
# 'Weekday','Visibility','Cloud_Coverage','Precipitation_Intensity','Precip_Intensity_Max','Clear',
# 'Cloudy','Rain','Fog','Snow','RainBefore','Terrain','Land_Use','Access_Control','Operation',
# 'Thru_Lanes','Num_Lanes','Ad_Sys','Gov_Cont','Func_Class','Pavement_Width',	'Pavement_Type')
# X_test = dataset.ix[:,columns].values



def add_data(hotspots,day,month, year):
    # Caste the columns into the data types we need them to be
    hotspots.Event = hotspots.Event.astype(str)
    hotspots.Conditions = hotspots.Conditions.astype(str)
    hotspots.Precipitation_Type = hotspots.Precipitation_Type.astype(str)
    hotspots.Precipitation_Intensity = hotspots.Precipitation_Intensity.astype(float)
    hotspots.Precip_Intensity_Max = hotspots.Precip_Intensity_Max.astype(float)
    hotspots.Temp_Max = hotspots.Temp_Max.astype(float)
    hotspots.Temp_Min = hotspots.Temp_Min.astype(float)
    hotspots.Precip_Intensity_Time = hotspots.Precip_Intensity_Time.astype(str)
    # hotspots.Date = hotspots.Date.astype(str)
    # hotspots.Time = hotspots.Time.astype(str)
    hotspots.Latitude = hotspots.Latitude.astype(float)
    hotspots.Longitude = hotspots.Longitude.astype(float)
    hotspots.EventBefore = hotspots.EventBefore.astype(str)
    hotspots.ConditionBefore = hotspots.ConditionBefore.astype(str)

    print("Fixing Latitude and Longitude")
    # Format the latitude and longitude values into the appropriate formats, if they need to be formatted
    for k, info in enumerate(hotspots.values):
        if hotspots.Latitude.values[k] > 40:
            hotspots.Latitude.values[k] = (hotspots.Latitude.values[k] / 1000000)
            hotspots.Longitude.values[k] = (hotspots.Longitude.values[k] / -1000000)

    # The key for using DarkSky API
    key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'

    print("Adding in DarkSky Weather")
    # Iterate through hotspots and assign weather data for each incident
    for k, info in enumerate(hotspots.values):
        print(k)
        # All variables are blank-of-accident, thus year is yoa.
        # toa = hotspots.Time.values[k]
        # hoa = int(toa.split(':')[0])
        hoa = hotspots.Hour.values[k]
        mioa = 0
        soa = 0
        yoa = year
        moa = month
        dayoa = day
        lat = hotspots.Latitude.values[k]
        long = hotspots.Longitude.values[k]

        # The following line needs to have this format:
        # print(datetime(yoa, moa, dayoa, hoa, mioa, soa))
        # exit()
        t = datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
        call = key, lat, long

        # Retrieve the previous hour's weather event and conditions for each incident
        # A series of if statements to see what day of the year it is
        # If it is the first of the month, then we call the weather data for the last day of the previous month
        if hoa == 0 and dayoa == 1:  # If 1/1, get weather data from 12/31, reduce year by 1
            if moa == 1:
                new_hoa = 23
                new_dayoa = 31
                new_moa = 12
                new_yoa = yoa - 1
                # Get weather data
                # The following line needs to have this format:
                t = datetime(new_yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 2:  # If 2/1, get weather data from 1/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 1
                # Get weather data
                # The following line needs to have this format:
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 3:  # If 3/1, get weather data from 2/28, same year
                new_hoa = 23
                new_dayoa = 28
                new_moa = 2
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 4:  # If 4/1, get weather data from 3/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 3
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 5:  # If 5/1, get weather data from 4/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 4
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 6:  # If 6/1, get weather data from 5/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 5
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 7:  # If 7/1, get weather data from 6/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 6
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 8:  # If 8/1, get weather data from 7/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 7
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 9:  # If 9/1, get weather data from 8/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 8
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 10:  # If 10/1, get weather data from 9/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 9
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 11:  # If 11/1, get weather data from 10/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 10
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 12:  # If 12/1, get weather data from 11/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 11
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        hotspots.EventBefore.values[k] = value.icon
                        hotspots.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            else:
                print("Error in calculating previous day")
        elif hoa == 0 and dayoa != 1:
            new_dayoa = dayoa - 1
            new_hoa = 23
            # Get weather data
            t = datetime(yoa, moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    hotspots.EventBefore.values[k] = value.icon
                    hotspots.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif hoa > 0:
            new_hoa = hoa - 1
            # Get weather data
            t = datetime(yoa, moa, dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    hotspots.EventBefore.values[k] = value.icon
                    hotspots.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        else:
            print("One of the hours was 0 and didn't register")

        # Retrieve the main weather data
        try:
            forecastcall = forecast(*call, time=t)
            # Hourly data
            for i, value in enumerate(forecastcall.hourly):
                # Retrieving weather for previous weather
                if i == hoa:
                    hotspots.Temperature.values[k] = value.temperature
                    hotspots.Dewpoint.values[k] = value.dewPoint
                    hotspots.Event.values[k] = value.icon
                    hotspots.Humidity.values[k] = value.humidity
                    hotspots.Month.values[k] = moa
                    hotspots.Visibility.values[k] = value.visibility
                    hotspots.Conditions.values[k] = value.summary
        except:
            print("Hourly Lookup Failed")
        # try:
            # Daily data, which requires individual try/except statements, otherwise the code crashes for some reason
        for j, value2 in enumerate(forecastcall.daily):
            try:
                hotspots.Precipitation_Type.values[k] = value2.precipType
            except:
                hotspots.Precipitation_Type.values[k] = "NA"
            try:
                hotspots.Precipitation_Intensity.values[k] = value2.precipIntensity
            except:
                hotspots.Precipitation_Intensity.values[k] = -1000
            try:
                hotspots.Precip_Intensity_Max.values[k] = value2.precipIntensityMax
            except:
                hotspots.Precip_Intensity_Max.values[k] = -1000
            try:
                hotspots.Precip_Intensity_Time.values[k] = value2.precipIntensityMaxTime
            except:
                hotspots.Precip_Intensity_Time.values[k] = -1000
            try:
                hotspots.Temp_Max.values[k] = value2.temperatureMax
            except:
                hotspots.Temp_Max.values[k] = -1000
            try:
                hotspots.Temp_Min.values[k] = value2.temperatureMin
            except:
                hotspots.Temp_Min.values[k] = -1000
            try:
                hotspots.Cloud_Coverage.values[k] = value2.cloudCover
            except:
                hotspots.Cloud_Coverage.values[k] = -1000
        for i, value in enumerate(hotspots.values):
            if "clear" in hotspots.Event.values[i] or "clear" in hotspots.Conditions.values[
                i] \
                    or "Clear" in hotspots.Event.values[i] or "Clear" in \
                    hotspots.Conditions.values[i]:
                hotspots.Clear.values[i] = 1
            else:
                hotspots.Clear.values[i] = 0

            if "rain" in hotspots.Event.values[i] or "rain" in hotspots.Conditions.values[i] \
                    or "Rain" in hotspots.Event.values[i] or "Rain" in \
                    hotspots.Conditions.values[i] \
                    or "Drizzle" in hotspots.Event.values[i] or "Drizzle" in \
                    hotspots.Conditions.values[i] \
                    or "drizzle" in hotspots.Event.values[i] or "drizzle" in \
                    hotspots.Conditions.values[i]:
                hotspots.Rain.values[i] = 1
            else:
                hotspots.Rain.values[i] = 0

            if "snow" in hotspots.Event.values[i] or "snow" in hotspots.Conditions.values[i] \
                    or "Snow" in hotspots.Event.values[i] or "Snow" in \
                    hotspots.Conditions.values[i]:
                hotspots.Snow.values[i] = 1
            else:
                hotspots.Snow.values[i] = 0

            if "cloudy" in hotspots.Event.values[i] or "cloudy" in \
                    hotspots.Conditions.values[i] \
                    or "Cloudy" in hotspots.Event.values[i] or "Cloudy" in \
                    hotspots.Conditions.values[i] \
                    or "overcast" in hotspots.Event.values[i] or "overcast" in \
                    hotspots.Conditions.values[i] \
                    or "Overcast" in hotspots.Event.values[i] or "Overcast" in \
                    hotspots.Conditions.values[
                        i]:
                hotspots.Cloudy.values[i] = 1
            else:
                hotspots.Cloudy.values[i] = 0

            if "fog" in hotspots.Event.values[i] or "foggy" in hotspots.Conditions.values[i] \
                    or "Fog" in hotspots.Event.values[i] or "Foggy" in \
                    hotspots.Conditions.values[i]:
                hotspots.Fog.values[i] = 1
            else:
                hotspots.Fog.values[i] = 0
            if "rain" in hotspots.EventBefore.values[i] or "rain" in \
                    hotspots.ConditionBefore.values[i] \
                    or "Rain" in hotspots.EventBefore.values[i] or "Rain" in \
                    hotspots.ConditionBefore.values[i]:
                hotspots.RainBefore.values[i] = 1
            else:
                hotspots.RainBefore.values[i] = 0
        now = datetime.now()
        # numpy.savetxt("../Excel & CSV Sheets/2018 Data/" +str(datetime.today())+"hotspotsForecast.csv", hotspots)
        hotspots.to_csv("../Excel & CSV Sheets/2019 Data/" +str(now.strftime("%Y-%m-%d_%h"))+"_hotspotsForecast.csv",
                     sep=",")


def generate_results(y_test,predictions, hist, fpr, tpr, roc_auc, date):
    font = {'family': 'serif',
            'weight': 'regular',
            'size': 14}
    plt.rc('font', **font)
    fig = plt.figure()
    # plt.subplot(211)
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.yticks((0,.5,1), (0,.5,1))
    plt.xticks((0,.5,1), (0,.5,1))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic curve')
    title = '../Graphs & Images/ResultsFromForecast/roc.png'
    fig.savefig(title, bbox_inches='tight')
    # plt.subplot(212)
    fig = plt.figure()
    plt.xticks(range(0, 20), range(1, 21), rotation=90)
    plt.yticks(range(0, 2), ['No', 'Yes', ''])
    plt.ylabel('Accident')
    plt.xlabel('Record')
    plt.grid(which='major', axis='x')
    x= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    plt.axhline(y=0.5, color='gray', linestyle='-')
    plt.scatter(x=x, y=predictions[0:20], s=100, c='blue', marker='x', linewidth=2)
    plt.scatter(x=x, y=y_test[0:20], s=110,
                facecolors='none', edgecolors='r', linewidths=2)
    title = '../Graphs & Images/ResultsFromForecast/pred'+date+'.png'
    fig.savefig(title, bbox_inches='tight')

    font = {'family': 'serif',
            'weight': 'bold',
            'size': 14}
    plt.rc('font', **font)
    fig = plt.figure()
    a1 = fig.add_subplot(2,1,1)
    a1.plot(hist.history['acc'])
    a1.plot(hist.history['val_acc'])
    a1.set_ylabel('Accuracy')
    a1.set_xlabel('Epoch')
    a1.set_yticks((.5, .65, .8) )
    a1.set_xticks((0,(len(hist.history['val_acc'])/2),len(hist.history['val_acc'])))
    a1.legend(['Train Accuracy', 'Test Accuracy'], loc='lower right', fontsize='small')
    # plt.show()
    # fig.savefig('acc.png', bbox_inches='tight')
    # summarize history for loss
    # fig = plt.figure()
    a2 = fig.add_subplot(2,1,2)
    # fig = plt.figure()
    a2.plot(hist.history['loss'])
    a2.plot(hist.history['val_loss'])
    a2.set_ylabel('Loss')
    a2.set_xlabel('Epoch')
    a2.set_yticks((.15,.20,.25,))
    a2.set_xticks((0,(len(hist.history['val_loss'])/2),len(hist.history['val_loss'])))
    a2.legend(['Train Loss', 'Test Loss'], loc='upper right', fontsize='small')
    # plt.show()
    title = '../Graphs & Images/ResultsFromForecast/lossandacc'+date+'.png'
    fig.savefig(title, bbox_inches='tight')


# dataset.to_csv("../Excel & CSV Sheets/2019 Data/" +str(now.strftime("%Y-%m-%d"))+"_hotspotsForecast.csv",
#                      sep=",")


def get_etrims(dataset):
    print("Getting Accident Road Geometrics")
    driver = webdriver.Firefox(executable_path=r"/home/admin/PycharmProjects/911Project/geckodriver")
    driver.get("https://e-trims.tdot.tn.gov/Account/Logon")

    usr = driver.find_element_by_id("UserName")
    pw = driver.find_element_by_id("Password")

    usr.send_keys("JJVPG56")
    pw.send_keys("Saturn71")  # updated 2/26/2019
    driver.find_element_by_class_name("btn").click()

    dataset.Route = dataset.Route.astype(str)

    for i, info in enumerate(dataset.values):
        latitude = dataset.Latitude.values[i]
        longitude = dataset.Longitude.values[i]

        site = "https://e-trims.tdot.tn.gov/etrimsol/services/applicationservice/roadfinder/lrsforlatlong?latitude=" \
               + str(latitude) + "&longitude=" + str(longitude) + "&d=1538146112919"

        driver.get(site)
        raw = str(driver.page_source)
        milepoint = float(raw[raw.index("<MilePoint>") + len("<MilePoint>"): raw.index("</MilePoint>")])
        # routeid = raw[raw.index("<RouteId>") + len("<RouteId>"): raw.index("</RouteId>")]

        # dataset.Route.values[i] = routeid
        dataset.Log_Mile.values[i] = milepoint

    geometrics = pandas.read_csv(
        "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_New.csv",
        sep=",")
    segments = pandas.read_csv(
        "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/ETRIMS/Road_Segment_County_Raw.csv",
        sep=",")
    descriptions = pandas.read_csv(
        "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/ETRIMS/Roadway_Description_County_HAMILTON RAW.csv",
        sep=",")
    traffic = pandas.read_csv(
        "/home/admin/PycharmProjects/911Project/Excel & CSV Sheets/ETRIMS/Traffic_Count.csv",
        sep=",")
    for k, info in enumerate(dataset.values):
        for i, value in enumerate(geometrics.values):
            if dataset.Route.values[k] == geometrics.ID_NUMBER.values[i]:
                if geometrics.ELM.values[i] > dataset.Log_Mile.values[k] > geometrics.BLM.values[i]:
                    dataset.Num_Lanes.values[k] = geometrics.Num_Lns.values[i]
                    dataset.Thru_Lanes.values[k] = geometrics.Thru_Lanes.values[i]
        for l, value in enumerate(segments.values):
            if dataset.Route.values[k] == segments.ID_NUMBER.values[l]:
                if segments.ELM.values[l] > dataset.Log_Mile.values[k] > segments.BLM.values[l]:
                    dataset.Ad_Sys.values[k] = segments.Ad_Sys.values[l]
                    dataset.Gov_Cont.values[k] = segments.Gov_Cont.values[l]
                    dataset.Func_Class.values[k] = segments.Func_Class.values[l]
        for m, value in enumerate(traffic.values):
            if dataset.Route.values[k] == traffic.ID_NUMBER.values[m]:
                if traffic.ELM.values[m] > dataset.Log_Mile.values[k] > traffic.BLM.values[m]:
                    dataset.AADT.values[k] = traffic.AADT.values[m]
                    dataset.DHV.values[k] = traffic.DHV.values[m]
        for n, value in enumerate(descriptions.values):
            if dataset.Route.values[k] == descriptions.ID_NUMBER.values[n]:
                if descriptions.ELM.values[n] > dataset.Log_Mile.values[k] > descriptions.BLM.values[n]:
                    if descriptions.Feature_Type[n] == 19:
                        dataset.Pavement_Width.values[k] = descriptions.Feat_Width.values[n]
                        dataset.Pavement_Type.values[k] = descriptions.Feature_Composition.values[n]
        for i, value in enumerate(geometrics.values):
            if dataset.Route.values[k] == geometrics.ID_NUMBER.values[i]:
                if geometrics.ELM.values[i] > dataset.Log_Mile.values[k] > geometrics.BLM.values[i]:
                    dataset.Terrain.values[k] = geometrics.Terrain.values[i]
                    dataset.Land_Use.values[k] = geometrics.Land_Use.values[i]
                    dataset.Access_Control.values[k] = geometrics.Acc_Ctrl.values[i]
                    dataset.Illumination.values[k] = geometrics.Illum.values[i]
                    dataset.Speed_Limit.values[k] = geometrics.Spd_Limit.values[i]
                    dataset.Operation.values[k] = geometrics.Operation.values[i]
    print("Getting weather stuff")
    for i, value in enumerate(dataset.values):
        if "clear" in dataset.Event.values[i] or "clear" in dataset.Conditions.values[
            i] \
                or "Clear" in dataset.Event.values[i] or "Clear" in \
                dataset.Conditions.values[i]:
            dataset.Clear.values[i] = 1
        else:
            dataset.Clear.values[i] = 0

        if "rain" in dataset.Event.values[i] or "rain" in dataset.Conditions.values[i] \
                or "Rain" in dataset.Event.values[i] or "Rain" in \
                dataset.Conditions.values[i] \
                or "Drizzle" in dataset.Event.values[i] or "Drizzle" in \
                dataset.Conditions.values[i] \
                or "drizzle" in dataset.Event.values[i] or "drizzle" in \
                dataset.Conditions.values[i]:
            dataset.Rain.values[i] = 1
        else:
            dataset.Rain.values[i] = 0

        if "snow" in dataset.Event.values[i] or "snow" in dataset.Conditions.values[i] \
                or "Snow" in dataset.Event.values[i] or "Snow" in \
                dataset.Conditions.values[i]:
            dataset.Snow.values[i] = 1
        else:
            dataset.Snow.values[i] = 0

        if "cloudy" in dataset.Event.values[i] or "cloudy" in \
                dataset.Conditions.values[i] \
                or "Cloudy" in dataset.Event.values[i] or "Cloudy" in \
                dataset.Conditions.values[i] \
                or "overcast" in dataset.Event.values[i] or "overcast" in \
                dataset.Conditions.values[i] \
                or "Overcast" in dataset.Event.values[i] or "Overcast" in \
                dataset.Conditions.values[
                    i]:
            dataset.Cloudy.values[i] = 1
        else:
            dataset.Cloudy.values[i] = 0

        if "fog" in dataset.Event.values[i] or "foggy" in dataset.Conditions.values[i] \
                or "Fog" in dataset.Event.values[i] or "Foggy" in \
                dataset.Conditions.values[i]:
            dataset.Fog.values[i] = 1
        else:
            dataset.Fog.values[i] = 0
        if "rain" in dataset.EventBefore.values[i] or "rain" in \
                dataset.ConditionBefore.values[i] \
                or "Rain" in dataset.EventBefore.values[i] or "Rain" in \
                dataset.ConditionBefore.values[i]:
            dataset.RainBefore.values[i] = 1
        else:
            dataset.RainBefore.values[i] = 0
    return dataset


def job(t, hotspots, day,month, year):
    add_data(hotspots,day,month, year)
    print(t)
    return
schedule.every().day.at("18:00").do(job, "Fetching weather forecast for 6 PM on Thursday 2/28", hotspots, 1, 3, 2019)
schedule.every().day.at("00:00").do(job, "Fetching weather forecast for Midnight on Friday 3/1", hotspots, 1, 3, 2019)
schedule.every().day.at("08:17").do(job, "Fetching weather forecast for 6 AM on Friday 3/1", hotspots, 1, 3, 2019)
schedule.every().day.at("12:00").do(job, "Fetching weather forecast for Noon on Friday 3/1", hotspots, 1, 3, 2019)
while True:
    schedule.run_pending()
    time.sleep(0)

# print(hotspots.columns.values)



# model = Sequential()
# model.add(Dense(30, input_dim=30, activation='sigmoid'))
# model.add(Dense(28, activation='sigmoid'))
# model.add(Dropout(.1))
# model.add(Dense(20, activation='sigmoid'))
# model.add(Dense(18, activation='sigmoid'))
# model.add(Dense(10, activation='sigmoid'))
# model.add(Dropout(.1))
# model.add(Dense(1, activation='sigmoid'))
#
# #           3. Compiling a model.
# model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])
# model.load_weights("model.h5")
# # Okay, now let's calculate predictions.
# predictions = model.predict(X_test)
# dataset["Probability"] = predictions
# # Then, let's round to either 0 or 1, since we have only two options.
# predictions_round = [abs(round(x[0])) for x in predictions]
# dataset["Predictions"] = predictions_round
# # print(rounded)
# print("Head of predicitons: ", predictions[0:10])
# print("Head of predictions_round: ", predictions_round)
#
# dataset.to_csv("../Excel & CSV Sheets/2019-02-25_13_forecast_full2.csv", sep=",")
# matches = 0

# for i, info in enumerate(forecast.values):
#     for j, data in enumerate(monday.values):
#         forecastHour = forecast.Hour.values[i]
#         mondayHour = monday.Hour.values[j]
#         hourDiff = abs(forecastHour - mondayHour)
#         if hourDiff < 3:
#             lat1 = forecast.Latitude.values[i]
#             long1 = forecast.Longitude.values[i]
#
#             lat2 = monday.Latitude.values[j]
#             long2 = monday.Longitude.values[j]
#             latChange = math.fabs(lat1 - lat2)
#             longChange = math.fabs(long1 - long2)
#             if latChange < 0.01 and longChange < 0.01:
#                 matches +=1
#
# print(matches)