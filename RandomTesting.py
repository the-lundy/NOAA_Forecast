import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import datetime

current_file_path = os.path.dirname(__file__)
print(current_file_path)

df = pd.read_csv("".join([current_file_path,"\\NWAC_DATA\\snoqualmie-pass-snowfall_24_hour.csv"]))

t = [None]*len(df[df.columns[0]])
data = [None]*len(df[df.columns[0]])

for i in range(len(t)):
    t[i] = datetime.datetime.strptime(df[df.columns[0]][i],"%m/%d/%y %I %p")
    if df[df.columns[1]][i] < 0:
        data[i] = 0
    else:
        data[i] = df[df.columns[1]][i]


fig, axes = plt.subplots(figsize=(12, 10))
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.05)

plt.plot(t,data)

plt.xticks(rotation=45)

plt.savefig('test.png')
