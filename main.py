from ReadDatabase import ReadDatabase
df = ReadDatabase('ais_data_william2.db')
df.reset_index(inplace=True, drop=True)

from MetoceanDownloader import MetoceanDownloader
downloader = MetoceanDownloader("wviken", "Audi3.0tdi")
import cftime
import pprint
import pandas as pd
from datetime import datetime as dt
import numpy as np
import folium


# Writing to an excel sheet using Python
from xlwt import Workbook

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

#defining labels to excel sheet
sheet1.write(0, 0, 'Time')
sheet1.write(0, 1, 'Latitude')
sheet1.write(0, 2, 'Longitude')
sheet1.write(0, 3, 'SOG')
sheet1.write(0, 4, 'Heading')
sheet1.write(0, 5, 'Mean wave direction')
sheet1.write(0, 6, 'Significant wave height')
sheet1.write(0, 7, 'Wave peak period')
sheet1.write(0, 8, 'Wind direction')
sheet1.write(0, 9, 'Wind speed')
sheet1.write(0, 10, 'Saved power ship[W]')
sheet1.write(0, 11, 'Effective rotor power [W]')


data = pd.read_csv('All_cases2.csv') #importing csv file

#splitting the dataframe
df1 = df.loc[(df['dt'] > '2020-08-14 01:41:00')]
df2 = df.loc[(df['dt'] > '2020-05-05 08:42:00')]

from Functions import linePlottingColorsSpeed
from Functions import WASP_Output
from Functions import Distance

mm=folium.Map(location=[75.1043,73.1950],tiles="Stamen Terrain") #creating map

time = cftime.datetime(2019, 1, 1, 6, 0, 0)#initial value for time
distance = 0 #initial value
n = -1 #initial value
for row in df1[:-1].itertuples():
    latitude_1 = row.lat
    longitude_1 = row.lon
    latitude_2 = df1.loc[row.Index + 1, 'lat']
    longitude_2 = df1.loc[row.Index + 1, 'lon']
    new_time = row.dt
    delta_time = new_time - time
    duration_in_s = delta_time.total_seconds()
    duration_in_h = divmod(duration_in_s, 3600)[0]
    # plotting map with ship routes
    color = linePlottingColorsSpeed(row.sog)  # Find the color that corresponds to the speed
    # Add line to illustrate the route
    folium.PolyLine([[latitude_1, longitude_1],
                     [latitude_2, longitude_2]],
                    color=color, weight=2.5, opacity=0.9).add_to(mm)
    distance = distance + Distance(latitude_1, longitude_1, latitude_2, longitude_2)
    if duration_in_h > 6:
        n = n + 1
        time = row.dt
        year = time.year
        month = time.month
        day = time.day
        hour = time.hour
        minute = time.minute
        second = time.second
        time_input = cftime.datetime(year, month, day, hour, minute, second)

        requested_data = downloader.get_weather(time_input, latitude_1, longitude_1)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(requested_data)

        ship_speed = row.sog
        ship_heading = row.heading
        #wave_direction = int(requested_data['mean wave direction']['value'])
        #wave_height = int(requested_data['significant wave height']['value'])
        #wave_period = int(requested_data['wave peak period']['value'])
        wind_speed = int(requested_data['wind speed in 10m height']['value'])
        wind_direction = int(requested_data['wind direction in 10m height']['value'])

        saved_power_ship, effective_rotor_power = WASP_Output(data, wind_direction, ship_heading, ship_speed, wind_speed)
        """

        true_wind_angle = wind_direction - ship_heading #calculating true wind angle
        if true_wind_angle < 0:
            true_wind_angle = true_wind_angle + 360
        if true_wind_angle > 180:
            true_wind_angle = 360 - true_wind_angle

        #rounding of to nearest column value
        ship_speed_rounded = round(ship_speed*4)/4 #nearest 0.25 and converting to m/s
        if ship_speed_rounded < 4: #This is temporary
            ship_speed_rounded = 4
        wind_speed_rounded = round(wind_speed) #nearest integer
        if wind_speed_rounded < 1:
            wind_speed_rounded = 1
        true_wind_angle_rounded = round(true_wind_angle/2)*2 #nearest even number
        print(ship_speed_rounded)
        print(wind_speed_rounded)
        print(true_wind_angle_rounded)
        

        #Finding the row corresponding to the given conditions
        corresponding_row = data.loc[(data['Ship speed [kn]'] == ship_speed_rounded) & (data['True wind speed [m/s]'] == wind_speed_rounded) & (data['True wind angle [deg]'] == true_wind_angle_rounded)]#, 'Saved power ship[W]']
        saved_power_ship = corresponding_row['Saved power ship[W]'].values[0]
        effective_rotor_power = corresponding_row['Effective rotor power [W]'].values[0]
        """


#writing to excel file
        sheet1.write(n + 1, 0, row.dt)
        sheet1.write(n + 1, 1, latitude_1) #sheet1.write(row.index + 1, 1, latitude)
        sheet1.write(n + 1, 2, longitude_2)
        sheet1.write(n + 1, 3, ship_speed)
        sheet1.write(n + 1, 4, ship_heading)
        #sheet1.write(n + 1, 5, wave_direction)
        #sheet1.write(n + 1, 6, wave_height)
        #sheet1.write(n + 1, 7, wave_period)
        sheet1.write(n + 1, 8, wind_direction)
        sheet1.write(n + 1, 9, wind_speed)
        sheet1.write(n + 1, 10, saved_power_ship)
        sheet1.write(n + 1, 11, effective_rotor_power)
        wb.save('Results.xls')

for row in df2[:-1].itertuples():
    latitude_1 = row.lat
    longitude_1 = row.lon
    latitude_2 = df2.loc[row.Index + 1, 'lat']
    longitude_2 = df2.loc[row.Index + 1, 'lon']
    new_time = row.dt
    delta_time = new_time - time
    duration_in_s = delta_time.total_seconds()
    duration_in_h = divmod(duration_in_s, 3600)[0]
    # plotting map with ship routes
    color = linePlottingColors(row.sog)  # Find the color that corresponds to the speed
    # Add line to illustrate the route
    folium.PolyLine([[latitude_1, longitude_1],
                     [latitude_2, longitude_2]],
                    color=color, weight=2.5, opacity=0.9).add_to(mm)
    distance = distance + Distance(latitude_1, longitude_1, latitude_2, longitude_2)
    if duration_in_h > 6:
        n = n + 1
        time = row.dt
        year = time.year
        month = time.month
        day = time.day
        hour = time.hour
        minute = time.minute
        second = time.second
        time_input = cftime.datetime(year, month, day, hour, minute, second)

        requested_data = downloader.get_weather(time_input, latitude_1, longitude_1)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(requested_data)

        ship_speed = row.sog
        ship_heading = row.heading
        #wave_direction = int(requested_data['mean wave direction']['value'])
        #wave_height = int(requested_data['significant wave height']['value'])
        #wave_period = int(requested_data['wave peak period']['value'])
        wind_speed = int(requested_data['wind speed in 10m height']['value'])
        wind_direction = int(requested_data['wind direction in 10m height']['value'])

        saved_power_ship, effective_rotor_power = WASP_Output(data, wind_direction, ship_heading, ship_speed, wind_speed)
        """
        true_wind_angle = wind_direction - ship_heading #calculating true wind angle
        if true_wind_angle < 0:
            true_wind_angle = true_wind_angle + 360
        if true_wind_angle > 180:
            true_wind_angle = 360 - true_wind_angle

        #rounding of to nearest column value
        ship_speed_rounded = round(ship_speed*4)/4 #nearest 0.25 and converting to m/s
        if ship_speed_rounded < 6: #This is temporary
            ship_speed_rounded = 6
        wind_speed_rounded = round(wind_speed) #nearest integer
        if wind_speed_rounded < 1:
            wind_speed_rounded = 1
        true_wind_angle_rounded = round(true_wind_angle/2)*2 #nearest even number
        print(ship_speed_rounded)
        print(wind_speed_rounded)
        print(true_wind_angle_rounded)

        #Finding the row corresponding to the given conditions
        corresponding_row = data.loc[(data['Ship speed [kn]'] == ship_speed_rounded) & (data['True wind speed [m/s]'] == wind_speed_rounded) & (data['True wind angle [deg]'] == true_wind_angle_rounded)]#, 'Saved power ship[W]']
        saved_power_ship = corresponding_row['Saved power ship[W]'].values[0]
        effective_rotor_power = corresponding_row['Effective rotor power [W]'].values[0]
        """

#writing to excel file
        sheet1.write(n + 1, 0, row.dt)
        sheet1.write(n + 1, 1, latitude_1) #sheet1.write(row.index + 1, 1, latitude)
        sheet1.write(n + 1, 2, longitude_1)
        sheet1.write(n + 1, 3, ship_speed)
        sheet1.write(n + 1, 4, ship_heading)
        #sheet1.write(n + 1, 5, wave_direction)
        #sheet1.write(n + 1, 6, wave_height)
        #sheet1.write(n + 1, 7, wave_period)
        sheet1.write(n + 1, 8, wind_direction)
        sheet1.write(n + 1, 9, wind_speed)
        sheet1.write(n + 1, 10, saved_power_ship)
        sheet1.write(n + 1, 11, effective_rotor_power)
        wb.save('Results.xls')


print(distance)
#wb.save('Results.xls')
mm.save('Map.html')
#df.to_csv('testCSV.csv', index=False)
