#import plotly.express as px
#import plotly.graph_objects as go
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import folium
from Functions import linePlottingColorsPercent

df = pd.read_csv('Results_all.csv')#importing csv file


'''
#windrose plot
ax = WindroseAxes.from_ax()
ax.bar(df['True_wind_angle'], df['Wind_speed'], bins=np.arange(0, 15, 2), edgecolor='white')
ax.set_legend()
plt.savefig('WindRose.jpg')
plt.close()

fig = plt.figure()
x = df['Time']
y = df['Saved_power_ship[W]']
plt.xlabel('Datetime')
plt.ylabel('saved power')
plt.plot(x, y, color='blue')
plt.show()
'''
'''
#calculating average savings for each trip and plotting in histogram
df['bin'] = pd.cut(x=df['Time'],
                    bins=[43839, 43855, 43891, 43913, 43949, 43980, 44004, 44034, 44059, 44080, 44096, 44106, 44115, 44131, 44159, 44178, 44193],#'2020-01-09', '2020-01-25', '2020-02-29', '2020-03-21', '2020-04-24', '2020-05-24',
                         # '2020-06-16', '2020-07-15', '2020-08-08', '2020-08-29', '2020-09-13', '2020-09-23',
                          #'2020-10-10', '2020-10-26', '2020-11-23', '2020-12-12', '2020-12-28'],
                    include_lowest=True,
                    labels=['Route 1', 'Route 2', 'Route 3', 'Route 4', 'Route 5', 'Route 6', 'Route 7', 'Route 8',
                            'Route 9', 'Route 10', 'Route 11', 'Route 12', 'Route 13', 'Route 14', 'Route 15',
                            'Route 16'])
group = df.groupby('bin')
list = []
for i in group.groups:
    group_i = group.get_group(i)
    percent_saved_mean = group_i['Percent_saved'].mean()
    list.append(percent_saved_mean)
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
plt.bar(x, list)
plt.axhline(y=6.9, color="#FF0000")
plt.xlabel("Route number")
plt.ylabel("Fuel saved [%]")
plt.savefig("fuel_saved_percent.jpg")
plt.show()
'''
#map with line colors based on the percent saved
df['bin'] = pd.cut(x=df['Time'],
                    bins=[43831, 43956.4, 44195],
                    include_lowest=True,
                    labels=['Route 1', 'Route 2'])
mm=folium.Map(location=[75.1043, 73.1950], tiles="Stamen Terrain") #creating map
group = df.groupby('bin')
for i in group.groups:
    group_i = group.get_group(i)
    for row in group_i[:-1].itertuples():
        latitude_1 = row.Latitude
        longitude_1 = row.Longitude
        latitude_2 = df.loc[row.Index + 1, 'Latitude']
        longitude_2 = df.loc[row.Index + 1, 'Longitude']
        # plotting map with ship routes
        color = linePlottingColorsPercent(row.Percent_saved)  # Find the color that corresponds to the speed
        # Add line to illustrate the route
        folium.PolyLine([[latitude_1, longitude_1],
                        [latitude_2, longitude_2]],
                         color=color, weight=2.5, opacity=0.9).add_to(mm)
mm.save('Map_percent_savings.html')
'''
top_values = df['Percent_saved'].dropna().quantile(0.90)
line = np.mean(top_values)
print(line)
with sns.axes_style("white"):
    fig=sns.displot(df['Percent_saved'],bins=30,kde=False)
    plt.xlim(-5, 50)
    plt.xlabel('Fuel savings [%]')
    plt.axvline(x=6.9, ymin=0, ymax=400, color="#FF0000")
    plt.axvline(x=line, ymin=0, ymax=400, color="#FF9912")
    plt.savefig('savings_count.png')
plt.show()
'''