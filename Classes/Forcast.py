from noaa_sdk import NOAA #Package is here
import datetime, re
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

class Forcast:
    def __init__(self,
                 latitude: float = 63.0692, 
                 longitude: float = 151.0070, 
                 forcastDuration: int = 2,
                 metrics: str = ["temperature","snowfallAmount","snowLevel","probabilityOfPrecipitation"]):
        # Inputs are defined as the following
        # lat = the latitude of the GPS position we want weather from - 
        # This has to be in the form of ...xxx.yyyy can not have more the 4 sig figs
        #
        # long = the longitude of the GPS position we want weather from - 
        # This has to be in the form of ...xxx.yyyy can not have more the 4 sig figs
        #
        # forcastDuration = Number of days (up to 7 for forcast duration)
        #
        # Defaults to Denali

        if forcastDuration > 7:
            print("Can't forcast longer then 7 days, setting forcast to 7 days\n")
            forcastDuration = 7
        elif forcastDuration < 1:
            print("Can't forcast shorter then 1 day, setting forcast to 1 days\n")
            forcastDuration = 1
        if round(latitude,4) != latitude:
            latitude = round(latitude,4)
            print("Can only forcast for four decimal points of accuracy, rounding to %.4f latitude",latitude)
        if round(longitude,4) != longitude:
            longitude = round(longitude,4)
            print("Can only forcast for four decimal points of accuracy, rounding to %.4f longitude",longitude)

        self.latitude = latitude
        self.longitude = longitude
        self.forcastDuration = forcastDuration

        self.metrics = metrics
        self.units = [None] * len(metrics)


    def getMetricsForcast(self):
        n = NOAA()
        forecast = n.points_forecast(self.latitude,self.longitude,type='forecastGridData')['properties'] 
        fig, axes = plt.subplots(2,2, figsize=(12, 10))
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.05)

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
            daysFromNow = daysFromNow+datetime.timedelta(days=self.forcastDuration)
            for j in range(len(metricValue)):

                mValue[j] = metricValue[j]['value']
                # Regex expression to remove the /PT1H from th date time, since I don't 
                # care about the persistent time of the forcast 
                timeList[j] = datetime.datetime.fromisoformat(re.sub("(.(PT|P)(\d|\d\d)(H|D))","",
                                                                     metricValue[j]['validTime'])) 

                #Could probably improve this to remove the values more smertly, but it works for now
                if ((self.forcastDuration == "ShortTerm" or self.forcastDuration == "MediumTerm" )  
                    and timeList[j] > daysFromNow):

                    del timeList[j+1:]
                    del mValue[j+1:]
                    
                    break
            self.plotForcast(timeList,mValue,elevation,fig,axes,i)
        #TODO: Make all of these properties of the object?
        fig.suptitle("".join(['Snoqualmie Pass Snow Metrics @ ',
                               str(round(elevation)), 'ft and' ,str(self.latitude),str(self.longitude)]))
        plt.tight_layout()
        now =  datetime.datetime.now()
        formatted_now = now.strftime("%Y%m%d_%H%M")
        plt.savefig("".join(["Snow_Metrics_" ,str(self.forcastDuration) ,"@",formatted_now,".png"]))

        return [timeList,mValue,elevation]

    def plotForcast(self,timeList,mValue,elevation,fig,axes,i_plt):
            plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.05)
            fig.axes[i_plt].plot(timeList,mValue)
            fig.axes[i_plt].set_ylabel("".join([self.metrics[i_plt],' ',self.units[i_plt]]))
            fig.axes[i_plt].set_xlabel("Time")
            #TODO:Fix this xticks issue for date time
            fig.axes[i_plt].set_xticklabels(fig.axes[i_plt].get_xticklabels(),rotation=45)
            fig.axes[i_plt].grid(visible=True)
            fig.axes[i_plt].set_title(self.metrics[i_plt])
        


sner = Forcast(47.4573,-121.4558)
    
[timeList,mValue,elevation] = sner.getMetricsForcast() 
x = 1