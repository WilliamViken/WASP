import numpy as np
import pandas as pd

from xlwt import Workbook

df = pd.read_csv('Resultater.csv')#importing csv file

#creating excel file
wb = Workbook()
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')
#setting column headers
sheet1.write(0, 0, 'Time')
sheet1.write(0, 1, 'Latitude')
sheet1.write(0, 2, 'Longitude')
sheet1.write(0, 3, 'SOG')
sheet1.write(0, 4, 'Heading')
sheet1.write(0, 5, 'Wind_direction')
sheet1.write(0, 6, 'Wind_speed')
sheet1.write(0, 7, 'True_wind_angle')
sheet1.write(0, 8, 'Percent_saved')
sheet1.write(0, 9, 'Fuel_saved[kg/h]')
sheet1.write(0, 10, 'Effective_thrust[N]')
sheet1.write(0, 11, 'Required_power_ship[w]')
sheet1.write(0, 12, 'Saved_power_ship[W]')
sheet1.write(0, 13, 'Effective_rotor_power[W]')

data = pd.read_csv('All_cases6.csv') #importing csv file

#initial value
percent = 0
fuel = 0
n = 0

from Functions import WASP_Output

for row in df.itertuples():
    n = n + 1
    time = row.Time
    latitude = row.Latitude
    longitude = row.Longitude
    ship_speed = row.SOG
    ship_heading = row.Heading
    wind_direction = row.Wind_direction
    wind_speed = row.Wind_speed
    true_wind_angle = row.True_wind_angle
    saved_power_ship, effective_rotor_power, required_power_ship, effective_thrust, saved_percent, saved_fuel = WASP_Output(data, true_wind_angle, ship_heading, ship_speed, wind_speed)

    """
    #apparent wind speed
    print(true_wind_angle)
    AWS = np.sqrt(wind_speed**2 + ship_speed**2 + 2*wind_speed*ship_speed*np.cos((2*np.pi/360)*true_wind_angle))
    print(AWS)
    #apparent wind angle
    dritt = (wind_speed * np.cos(true_wind_angle) + ship_speed) / AWS
    print(dritt)
    AWA = (360/(2*np.pi))*np.arccos(dritt)
    print(AWA)
    """

    sheet1.write(row.Index + 1, 0, time)
    sheet1.write(row.Index + 1, 1, latitude)  # sheet1.write(row.index + 1, 1, latitude)
    sheet1.write(row.Index + 1, 2, longitude)
    sheet1.write(row.Index + 1, 3, ship_speed)
    sheet1.write(row.Index + 1, 4, ship_heading)
    sheet1.write(row.Index + 1, 5, wind_direction)
    sheet1.write(row.Index + 1, 6, wind_speed)
    sheet1.write(row.Index + 1, 7, true_wind_angle)
    sheet1.write(row.Index + 1, 8, saved_percent)
    sheet1.write(row.Index + 1, 9, saved_fuel)
    sheet1.write(row.Index + 1, 10, effective_thrust)
    sheet1.write(row.Index + 1, 11, required_power_ship)
    sheet1.write(row.Index + 1, 12, saved_power_ship)
    sheet1.write(row.Index + 1, 13, effective_rotor_power)
    percent = percent + saved_percent
    fuel = fuel + saved_fuel
    wb.save('Results_all.xls')

#converting excel file to csv
read_file = pd.read_excel(r'Results_all.xls')
read_file.to_csv(r'Results_all.csv', index=None, header=True)

Average_percent = percent/n
Average_fuel_savings = fuel/n
print(Average_percent)
print(Average_fuel_savings)



