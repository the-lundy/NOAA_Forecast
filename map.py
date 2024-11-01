import folium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
# Sample data for points

lat = [47.4573,47.4586,47.390389,47.443298,47.467847]
long = [-121.4558,-121.4164,-121.395879,-121.379528,-121.456969]
# Create the map

mapName = "map.html"

m = folium.Map(location=[sum(lat)/len(lat), sum(long)/len(long)],
               max_bounds=True,
               zoom_control = False,
               tiles="OpenTopoMap")




m.fit_bounds([[max(lat),max(long)],[min(lat),min(long)]])

# Add markers for each point
for i in range(len(lat)):
    folium.Marker([lat[i],long[i]]).add_to(m)

# Save the map as an HTML file
m.save(mapName)
# m._to_png("test.png")
# Use Selenium to open the HTML file and take a screenshot
options = Options()
options.add_argument("--headless=new")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("file:///" + os.path.abspath(mapName))
#Adding this here to allow for loading/rendering of the html map
time.sleep(5)
driver.save_screenshot("".join(["OpenTopoMap",".png"]))
driver.quit()