#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mpl.rcParams.update({'font.size': 10})
plt.switch_backend('agg')


# open the text file and create arrays of temperature and humidity

temp = tuple(open("/home/pi/winecellar/tmpdata/today.temp", 'r'))
humid = open("/home/pi/winecellar/tmpdata/today.humid", 'r')

# round values and remove newline chars

temp = [round(float(x[:len(x)-1]),1) for x in temp]

humid = [round(float(x[:len(x)-1]),1) for x in humid]

#humid = [x[:4] for x in t]

#make sure the array of temps is same length as array of humids

if (len(temp) != len(humid)):
	if (len(temp) > len(humid)):
		temp = np.resize(temp, len(humid))
	else:
		humid = np.resize(humid, len(temp))

# set up x-axis from start time til now with the number of intervals in the temp and humid arrays

initialDatetime = datetime.datetime.now() - datetime.timedelta(minutes=20*len(temp))
initialDatetime = initialDatetime.replace(hour=4, minute=0)
t = [(initialDatetime + datetime.timedelta(minutes=i*20)).strftime('%H:%M') for i in range(len(temp))]

#plot values

fig, ax = plt.subplots()
ax.plot(temp, label='Temperatur ($^\circ$C)', color='blue' )
ax.plot(humid, label='Luftfugtighed (%)', color='coral')
ax.legend(bbox_to_anchor=(0.21, 1.19), loc=1, borderaxespad=0, fancybox=True, framealpha=0.5)

# set labels
today = str(datetime.datetime.now().strftime("%d. %m. %Y"))
danishTitle = "Seneste døgn (" + today + ")"
danishTitle= danishTitle.decode('utf-8') 

ax.set(xlabel='Klokkeslet', 
	ylabel='' ,# Temp. ($^\circ$C) --  Luftfugtighed (%)',
	title=danishTitle)
ax.grid()
plt.gcf().autofmt_xdate()

plt.gcf().subplots_adjust(left=0.12)
plt.gcf().subplots_adjust(top=0.84)
ax.set_xticks(range(len(t)-2))
ax.set_xticklabels(t)
#ax.set_xticklabels(t, minor=False)


# hide some values in labels
n = 5 
for index, label in enumerate(ax.xaxis.get_ticklabels()):
       if index % n   != 0 and index != len(t)-3 :
               label.set_visible(False)

ax.margins(x=0)

#save file

fig.savefig("/home/pi/winecellar/img/today.png", bbox_inches='tight',pad_inches = 0, dpi = 200)
