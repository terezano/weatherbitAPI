# weatherbitAPI

This script connect to Weatherbit API and downloads chosen data as JSON for all desired values,
based on provided CSV with ID, Lat, Lon (degrees) and year of observations. 
The result is two merged dataframes (information about stations + values from weatherbitAPI)

###### Copyright: Copyright 2022, weatherbitAPI
###### Version: 1.0
###### E-mail: teznovakova@gmail.com

### Input Data
- CSV with point stations: 
```
ID,Latitude__S_,Longitude__W_,Year
1,-36.0502777777777,-63.6080555555555,2021
2,-35.4744444444444,-60.9441666666666,2021
```
- Your API key

### Requirements
```
osgeo==0.0.1
pandas==1.4.2
```

### Output
```
ID,Latitude__S_,Longitude__W_,Year,2021-01-01,2021-02-01
1,-36.0502777777777,-63.6080555555555,2021,15.6,12.8
2,-35.4744444444444,-60.9441666666666,2021,16.8,13.2
3,-32.4938888888888,-58.9741666666666,2021,3.9,17.5
```
