# Function that create a list of colors to use for plotting. n is the number of different colors needed.


#Function that calculates WASP performance based on inputs in line below
def WASP_Output(dataframe, wind_direction, ship_heading, ship_speed, wind_speed):
    true_wind_angle = wind_direction - ship_heading  # calculating true wind angle
    if true_wind_angle < 0:
        true_wind_angle = true_wind_angle + 360
    if true_wind_angle > 180:
        true_wind_angle = 360 - true_wind_angle

    # rounding of to nearest column value
    ship_speed_rounded = round(ship_speed * 4) / 4  # nearest 0.25 and converting to m/s
    if ship_speed_rounded < 4:  # This is temporary
        ship_speed_rounded = 4
    if ship_speed_rounded > 22:
        ship_speed_rounded = 22
    wind_speed_rounded = round(wind_speed)  # nearest integer
    if wind_speed_rounded < 1:
        wind_speed_rounded = 1
    true_wind_angle_rounded = round(true_wind_angle / 2) * 2  # nearest even number

    # Finding the row corresponding to the given conditions
    corresponding_row = dataframe.loc[
        (dataframe['Ship speed [kn]'] == ship_speed_rounded) & (dataframe['True wind speed [m/s]'] == wind_speed_rounded) & (
                    dataframe['True wind angle [deg]'] == true_wind_angle_rounded)]  # , 'Saved power ship[W]']
    saved_power_ship = corresponding_row['Saved power ship[W]'].values[0]
    effective_rotor_power = corresponding_row['Effective rotor power [W]'].values[0]
    required_power_ship = corresponding_row['Effective rotor power [W]'].values[0]
    effective_thrust = corresponding_row['Effective thrust [N]'].values[0]
    saved_percent = corresponding_row['Percental savings'].values[0]
    saved_fuel = corresponding_row['Fuel saved [kg/h]'].values[0]/1000

    return saved_power_ship, effective_rotor_power, required_power_ship, effective_thrust, saved_percent, saved_fuel

#function that calculates distance between two coordinates
#could also use geopy.distance.geodesic, but running time is doubled
def Distance(lat1, lon1, lat2, lon2):
    import numpy as np
    R = 6371 * 0.539956803 # Earth radius in nautical miles
    #lat1 = dataframe.iloc[row, 2]  # latitude point 1
    #lat2 = dataframe.iloc[row + 1, 2]  # latitude point 2
    #lon1 = dataframe.iloc[row, 3]  # longitude point 1
    #lon2 = dataframe.iloc[row + 1, 3]  # longitude point 2
    φ1 = lat1 * np.pi/180 # φ, λ in radians
    φ2 = lat2 * np.pi/180
    Δφ = (lat2-lat1) * np.pi/180
    Δλ = (lon2-lon1) * np.pi/180
    a = np.sin(Δφ/2) * np.sin(Δφ/2) + np.cos(φ1) * np.cos(φ2) * np.sin(Δλ/2) * np.sin(Δλ/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = c * R
    return distance

#Author: Andreas Isaksen, andrisa@stud.ntnu.no
# Function that create a list of colors to use for plotting. n is the number of different colors needed.
def linePlottingColorsSpeed(speed):
    a = 18
    b = 16
    c = 14
    d = 10
    if speed > a:
        color = "#0000FF" #blue
    elif speed <= a and speed > b: # <18, 16]
        color = "#00b500"  # green
    elif speed <= b and speed > c: # <14, 16]
        color = "#FFFF00" # yellow
    elif speed <= c and speed > d: # <10, 14]
        color = "#FF0000" # red
    elif speed <= d and speed >= 0: # [0, 10]
        color = "#FF00ae"  # pink
    else:
        color = "#000000" #black
    return color

def linePlottingColorsPercent(percental_saving):
    speed = percental_saving
    a = 25
    b = 10
    if speed > a:
        color = "#0000FF"  # blue
    elif speed <= a and speed > b: # <14, 16]
        color = "#00b500"  # green
    elif speed <= b and speed > 0: # [0, 10]
        color = "#FFFF00" # yellow
    else:
        color = "#FF0000" # red
    return color
