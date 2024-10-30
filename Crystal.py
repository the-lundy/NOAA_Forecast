from Classes.Forecast import Forecast
from noaa_sdk import NOAA #Package is here
import datetime, re
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import folium


def gps_to_map(latitude, longitude, output_file="map.html"):
    """
    Converts GPS coordinates to a map picture using Folium.
    """

    # Create a map centered on the given coordinates
    my_map = folium.Map(location=[latitude, longitude], zoom_start=15)

    # Add a marker at the specified location
    folium.Marker([latitude, longitude]).add_to(my_map)

    # Save the map as an HTML file
    my_map.save(output_file)


#Plot creation
fig, axes = plt.subplots(2,2, figsize=(12, 10))
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.05)
    # sner = Forecast(47.4573,-121.4558)

lat = [46.928330,46.943641,46.918995,46.803350]
long = [-121.504669,-121.451626,-121.462655,-121.729546]
legend = ["Silver Queen Top",
          "Burn Scar Trees summit",
          "PickHandle Basin S",
          "Panaroma Point - Rainer"]
for position in range(len(lat)):

    gps_to_map(lat[position],long[position],"".join([str(lat[position]),
                                                     str(long[position]),".html"]))
    sner = Forecast(lat[position],long[position],7)
    [outputValue,outputTime,elevation] = sner.getMetricsForecast() 
    #Iterate through all metrics to plot
    for i in range(len(sner.metrics)):
        sner.plotForecast(outputTime[i],outputValue[i],elevation,fig,axes,i)


#TODO: Make all of these properties of the object?
fig.suptitle("Crystal Area Snow Metrics")
plt.tight_layout()
fig.axes[0].legend()
fig.axes[1].legend(legend)
now =  datetime.datetime.now()
formatted_now = now.strftime("%Y%m%d_%H%M")
plt.savefig("".join(["Snow_Metrics_" ,str(sner.ForecastDuration) ,"@",formatted_now,".png"]))
