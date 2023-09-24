**[Access the running website](http://ebc-weather.ebc-team-nk.osc.eonerc.rwth-aachen.de/ "Wer das liest ist doof")**

**Station IDs and KML grid IDs**
============================================================

The station IDs for the DWD weather stations are listed [here](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/TU_Stundenwerte_Beschreibung_Stationen.txt). Aachen would be 15000.

The KML grid ids are listed [here](https://www.dwd.de/DE/leistungen/met_verfahren_mosmix/mosmix_stationskatalog.cfg?view=nasPublication&nn=16102). Aachen would be 10505.


**/api/\<station_id\>/\<start_date\>/\<enddate\>/\<data_type\>**
============================================================

start_date, end_date format : **YYYY-MM-DD**

**/api/\<station_id\>/\<start_date\>/\<enddate\>/\<enddate\>/epw**
---

Returns:

    A .EPW weather data with format IWEC for the `station_id` for the period between `start_date` and `end_date`.

**/api/\<station_id\>/\<start_date\>/\<enddate\>/mos**
---

Returns:

    A .MOS weather file for the `station_id` for the period between `start_date` and `end_date`.

**/api/\<station_id\>/\<start_date\>/\<enddate\>/pkl**
---

Returns:

    A .pkl file containing datetime dataframe for the `station_id` for the period between `start_date` and `end_date`.
    The dataframe contains metadata at index [-1].

Simple code to read .pkl file:

```
def read():
    data            =pd.read_pickle("15000_2021-01-01_2021-02-07_City_Aachen-Orsbach.pickle")
    meta            = pd.DataFrame(data.iloc[-1]).transpose().dropna(axis=1, how="all")
    weatherdata     = data.drop([0], axis=0).dropna(axis=1, how="all")

    return weatherdata, meta
```


**/api/forecast/\<grid_id\>/json**
---

Returns:

    A JSON .json containing the forecast dataframe for the `grid_id` for the next ten days.

_The Dataframe was converted to JSON using `orient = 'columns'` and needs to use the same orient to convert it back. See example below._

**/api/forecast/\<grid_id\>/mos**
---

Returns:

    A mos file for the `grid_id` for the days.


**Examples for accessing the api**
---

Download an .epw or .mos or .pkl:

```
import urllib.request

url='http://ebc-weather.ebc-team-nk.osc.eonerc.rwth-aachen.de/api/epw/15000/2021-01-01/2021-01-04/DWD/'
urllib.request.urlretrieve(url, 'D://weather.epw')
```
Download the forecast:

```
import pandas as pd
import requests


url = "http://ebc-weather.ebc-team-nk.osc.eonerc.rwth-aachen.de/api/forecast/10505/json"
r = requests.get(url).json()
forecast= pd.read_json(r, orient="columns")
```

**Information on input data types:**
---


**DWD historical:**

1. 'DryBulbTemp', 'DewPointTemp', 'RelHum', 'AtmPressure' : at indicated time
2. 'GlobHorRad', 'DiffHorRad' : 10-min sum interval
3. TotalSkyCover, Opaqueskycover : called cloudiness, hourly observation same as indicated time?
4. 'LiquidPrecD' : calculated from 6 10-minutes prec depth of preceeding hour = sum of preceeding hour
5. 'WindSpeed', 'WindDir' : avg. of preceeding hour
6. data in utc

**DWD forecast:**

1. most likely similar to historical, but there's no information online
2. data is in .kmz format

**DWD TRY2017:**

1. Timestamps:

* Temperature measurement: 1/2h before given time = avg. preceding hour
* Wind direction/wind speed: 10-minute average interval; we could not interpret exactly, probably average of the last 10 minutes before given time = indicated time
* Radiation:
* B(direct) & D(diffuse): average of preceding hour
* A(atmosphere): calculated at indicated time = at indicated time

2. Data is in UTC+1 (Start time: 01.01. 1 o'clock CET (UTC+1))

**Other TRY2017:**

1. Probably the same?
2. ?

**Hourly pulled ERC data:**

1. Timestamps refer to avg. of following hour
2. Data is in UTC

**Costum Data like CSV/Pickles** etc. should be in:

1. Timestamp refers to measurement at indicated time: for timestamp 3600 (either measurements made in 3600 or measurements is an avg. from timestamp 1800-5400)
2. Data in UTC

**Information on output data types:**
---
**.MOS file output:**
```
#C1 Time in seconds. Beginning of a year is 0s.
#C2 Dry bulb temperature in Celsius at indicated time
#C3 Dew point temperature in Celsius at indicated time
#C4 Relative humidity in percent at indicated time
#C5 Atmospheric station pressure in Pa at indicated time
#C6 Extraterrestrial horizontal radiation in Wh/m2, no measurement
#C7 Extraterrestrial direct normal radiation in Wh/m2, no measurement
#C8 Horizontal infrared radiation intensity in Wh/m2, Input: f(C3, C19, C2)
#C9 Global horizontal radiation in Wh/m2, Input: Values per 10-Minutes
#C10 Direct normal radiation in Wh/m2, Input: average preceding hour f(solar angle, radiation horizontal)
#C11 Diffuse horizontal radiation in Wh/m2,   Input: Values per 10-Minutes
#C12 Averaged global horizontal illuminance in lux during minutes preceding the indicated time, no measurement
#C13 Direct normal illuminance in lux during minutes preceding the indicated time, no measurement
#C14 Diffuse horizontal illuminance in lux  during minutes preceding the indicated time, no measurement
#C15 Zenith luminance in Cd/m2 during minutes preceding the indicated time, no measurement
#C16 Wind direction at indicated time. N=0, E=90, S=180, W=270, 
#C17 Wind speed in m/s at indicated time,  
#C18 Total sky cover at indicated time,  Input: f(cloudgrade) 
#C19 Opaque sky cover at indicated time, Input: f(cloudgrade) 
#C20 Visibility in km at indicated time, no measurement
#C21 Ceiling height in m, no measurement (default value 20000m used)
#C22 Present weather observation, no measurement
#C23 Present weather codes, no measurement
#C24 Precipitable water in mm, no measurement
#C25 Aerosol optical depth, no measurement
#C26 Snow depth in cm, no measurement
#C27 Days since last snowfall, no measurement
#C28 Albedo, no measurement
#C29 Liquid precipitation depth in mm at indicated time, no measurement
#C30 Liquid precipitation quantity, no measurement
```

**all other outputs:**
- everything at the indicated time: either value collected at the exact timestamp or an average from 30 mins before and after the timestamp
   - example: timestamp 3600 is either value read from the sensor at timestamp 3600 or an average of values from 1800-5400

