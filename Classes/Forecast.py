from noaa_sdk import NOAA #Package is here
import datetime, re
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

class Forecast:
    def __init__(self,
                 latitude: float = 63.0692, 
                 longitude: float = 151.0070, 
                 ForecastDuration: int = 2,
                 metrics: str = ["temperature","snowfallAmount","snowLevel","probabilityOfPrecipitation"]):
        # Inputs are defined as the following
        # lat = the latitude of the GPS position we want weather from - 
        # This has to be in the form of ...xxx.yyyy can not have more the 4 sig figs
        #
        # long = the longitude of the GPS position we want weather from - 
        # This has to be in the form of ...xxx.yyyy can not have more the 4 sig figs
        #
        # ForecastDuration = Number of days (up to 7 for Forecast duration)
        #
        # Defaults to Denali

        if ForecastDuration > 7:
            print("Can't Forecast longer then 7 days, setting Forecast to 7 days\n")
            ForecastDuration = 7
        elif ForecastDuration < 1:
            print("Can't Forecast shorter then 1 day, setting Forecast to 1 days\n")
            ForecastDuration = 1
        if round(latitude,4) != latitude:
            latitude = round(latitude,4)
            print("Can only Forecast for four decimal points of accuracy, rounding to", latitude, "latitude")
        if round(longitude,4) != longitude:
            longitude = round(longitude,4)
            print("Can only Forecast for four decimal points of accuracy, rounding to", longitude, "longitude")

        self.latitude = latitude
        self.longitude = longitude
        self.ForecastDuration = ForecastDuration

        self.metrics = metrics
        self.units = [None] * len(metrics)


    def getMetricsForecast(self):
        n = NOAA()
        forecast = n.points_forecast(self.latitude,self.longitude,type='forecastGridData')['properties'] 
   
        outputValue = [None for _ in range(len(self.metrics))] 
        outputTime = [None for _ in range(len(self.metrics))] 

        for i in range(len(self.metrics)):
            self.units[i] = forecast[self.metrics[i]]['uom']
            metricValue = forecast[self.metrics[i]]['values']

            # Parse the elevation and convert it from m to feet
            C_M_FT = 3.280839895
            elevation = forecast['elevation']['value']*C_M_FT
                
            #Sets the inital length of the arrays
            mValue = [-999]*len(metricValue)
            timeList = [0]*len(metricValue)

            #Sets the days from now for the specific filtering
            daysFromNow = metricValue[0]['value']
            daysFromNow = datetime.datetime.fromisoformat(re.sub("(.(PT|P)(\d|\d\d)(H|D))","",
                                                                 metricValue[0]['validTime'])) 
            daysFromNow = daysFromNow+datetime.timedelta(days=self.ForecastDuration)
            for j in range(len(metricValue)):

                mValue[j] = metricValue[j]['value']
                # Regex expression to remove the /PT1H from th date time, since I don't 
                # care about the persistent time of the Forecast 
                timeList[j] = datetime.datetime.fromisoformat(re.sub("(.(PT|P)(\d|\d\d)(H|D))","",
                                                                     metricValue[j]['validTime'])) 

                #Could probably improve this to remove the values more smertly, but it works for now
                if (timeList[j] > daysFromNow):

                    del timeList[j+1:]
                    del mValue[j+1:]
                    
                    break
            
            outputValue[i]=mValue
            outputTime[i]=timeList
            
            # self.plotForecast(timeList,mValue,elevation,fig,axes,i)


        return [outputValue,outputTime,elevation]

    def plotForecast(self,timeList,mValue,elevation,fig,axes,i_plt):
            fig.axes[i_plt].plot(timeList,mValue, label="".join(["Elevation: ", str(round(elevation)),"ft"]))
            fig.axes[i_plt].set_ylabel("".join([self.metrics[i_plt],' ',self.units[i_plt]]))
            fig.axes[i_plt].set_xlabel("Time")
            #TODO:Fix this xticks issue for date time
            fig.axes[i_plt].set_xticklabels(fig.axes[i_plt].get_xticklabels(),rotation=45)
            fig.axes[i_plt].grid(visible=True)
            fig.axes[i_plt].set_title(self.metrics[i_plt])