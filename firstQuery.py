from noaa_sdk import NOAA #Package is here
import datetime, re
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

import folium

# import numpy as np
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


def main(lat: float, long: float, forcastDuration: str):

    # Inputs are defined as the following
    # lat = the lattitude of the GPS position we want weather from - 
    # This has to be in the form of ...xxx.yyyy can not have more the 4 sig figs
    #
    # long = the longitude of the GPS position we want weather from - 
    # This has to be in the form of ...xxx.yyyy can not have more the 4 sig figs
    #
    # forcastDuration = "Short Term/MediumTerm/LongTerm" Gives the short term forcast (1 day)
    # Medium term (2 days) or long term forcast (7 days)

    if not(forcastDuration == "ShortTerm" or forcastDuration == "LongTerm" or forcastDuration == "MediumTerm"):
        raise ValueError("ForcastDuration must be either 'ShortTerm' or 'LongTerm'")

    #Sets the number of days that the forcast will be for
    if forcastDuration == "ShortTerm":
        forcastTimeDuration = 1
    else:
        forcastTimeDuration = 2


    n = NOAA()
    gps_to_map(lat,long)
    # Inputs here have to be %.4f precision
    forecast = n.points_forecast(lat, long,type='forecastGridData')['properties'] 

    # Parse the elevation and convert it from m to feet
    C_M_FT = 3.280839895
    elevation = forecast['elevation']['value']*C_M_FT

    metricsSnow = ["temperature","snowfallAmount","snowLevel","probabilityOfPrecipitation"]
    metricsOther = ["skyCover","windSpeed"]

    # Gets the current date time of the script running for possible filtering of shorterm forcast
    # and final plot formatting
    now =  datetime.datetime.now()
    formatted_now = now.strftime("%Y%m%d_%H%M")

    fig, axes = plt.subplots(2,2, figsize=(12, 10))
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.05)
    for i in range(len(metricsSnow)):
        #Gets the unit of measure so we know what to convert from and too
        unit = forecast[metricsSnow[i]]['uom']
        metricValue = forecast[metricsSnow[i]]['values']

        #Sets the inital length of the arrays
        mValue = [-999]*len(metricValue)
        timeList = [0]*len(metricValue)

        daysFromNow = metricValue[0]['value']
        daysFromNow = datetime.datetime.fromisoformat(re.sub("(.(PT|P)(\d|\d\d)(H|D))","",metricValue[0]['validTime'])) 
        daysFromNow = daysFromNow+datetime.timedelta(days=forcastTimeDuration)
        for j in range(len(metricValue)):

            mValue[j] = metricValue[j]['value']
            #Regex expression to remove the /PT1H from th date time, since I don't care about the persistent time of the forcast 
            timeList[j] = datetime.datetime.fromisoformat(re.sub("(.(PT|P)(\d|\d\d)(H|D))","",metricValue[j]['validTime'])) 

            #Poor filtering here, need to fix this at some point since the length of the array will be changing for the short term forcast
            if ((forcastDuration == "ShortTerm" or forcastDuration == "MediumTerm" )  and timeList[j] > daysFromNow):
                del timeList[j+1:]
                del mValue[j+1:]
                break
        
        fig.axes[i].plot(timeList,mValue)
        fig.axes[i].set_ylabel("".join([metricsSnow[i],' ',unit]))
        fig.axes[i].set_xlabel("Time")
        fig.axes[i].set_xticklabels(fig.axes[i].get_xticklabels(),rotation=45)
        fig.axes[i].grid(visible=True)
        fig.axes[i].set_title(metricsSnow[i])

    #Format the common properties of all of the plots
    fig.suptitle("".join(['Snoqualmie Pass Snow Metrics @ ', str(round(elevation)), 'ft and' ,str(lat),str(long)]))
    plt.tight_layout()
    plt.savefig("".join(["Snow_Metrics_" ,forcastDuration ,"@",formatted_now,".png"]))
    

    # plt.pause(1) this will show the figurein deubg but has some werid bugs. Interesting...
        # if (metricsSnow[i] == "temperature") or (metricsSnow[i] == "windSpeed"): 
        #     fig.axes[i].gca().yaxis.set_major_locator(MultipleLocator(0.5))
        #     fig.axes[i].gca().xaxis.set_major_locator(MultipleLocator(1))



if __name__ == '__main__':

#https://coordinates-converter.com/en/decimal/47.457300,-121.455800?karte=OpenStreetMap&zoom=15
    #Between Snow Lake and Source Lake
    lat = 47.4573
    long = -121.4558
    # #Top of Snoqalmine Mountain
    lat = 47.4586
    long = -121.4164
    forcastDuration = "ShortTerm"

    main(lat, long, forcastDuration)