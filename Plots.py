import pandas as pd
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
#plotly.graph_object

df = pd.read_csv('All_cases6.csv')#importing csv file
data = df.loc[(df['Ship speed [kn]'] == 16.5)]#setting speed in knots
n = - 1#initial value
size = len(data)

#setting which column that will be used for "color" in plot
#column_name = 'Constraint limit [-]'
column_name = 'Percental savings'
for row in range(size):
    n = n + 1
    #m = size + 1
    true_wind_speed = data['True wind speed [m/s]'].values[n]
    true_wind_angle = 360 - data['True wind angle [deg]'].values[n]
    value = data[column_name].values[n]
    if true_wind_angle != 180:
        new_row = {'True wind speed [m/s]': true_wind_speed,
                   'True wind angle [deg]': true_wind_angle, column_name: value}
        data = data.append(new_row, ignore_index=True)
fig = px.bar_polar(data, r='True wind speed [m/s]', theta='True wind angle [deg]',
                   color=column_name, #labels={
                     #'True wind speed [m/s]': 'True wind speed [m/s]',
                     #'True wind angle [deg]': 'True wind angle [deg]',
                    # 'Percental savings': '[%]'},
                        color_continuous_scale=px.colors.diverging.Portland)

'''                   
R = data['True wind speed [m/s]']
Theta = data['True wind angle [deg]']
Color = data['Saved power ship[W]']

fig = go.Figure(go.Barpolar(r=R, theta=Theta, marker_color=Color))
fig.update_layout(polar_bargap=0)
'''

fig.show()
pio.write_image(fig, 'rose_constraint.png')
