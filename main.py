import urllib

import urllib.request
api = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=0b7c4978dda884bbfb0397d03033509f"

sapi = "http://api.openweathermap.org/data/2.5/forecast/daily?zip=94032&appid=0b7c4978dda884bbfb0397d03033509f" 

saapi = "http://api.openweathermap.org/data/2.5/weather?q=Passau&appid=0b7c4978dda884bbfb0397d03033509f"
response = urllib.request.urlopen(saapi)
print(response)
output = response.read().decode('utf-8')

print(output)



# Variables required 
#1   "Soil_Moisture": 256, [0-300]= No - low moisture  [300-700] Medium  [700] High
#2.  "Analog_Rain": 4095, [1-2500 High] [2500-3000 Medium] [3000-4000 Low] [4000+ No rain]
#3.  "Digital_Rain": 1, (No rain)
#4.  "Temp": 18.18182,(celsius)


# Api

# 1. Temperature    "temp":286.89, (convert)

# "humidity":95 (moisture - fault tolerance - determine moisture) 


#  Control logic
# irrigate at 18:00

# 1. Mositure should be around <700
# 2. Digital rain - 1 & analog> 3500 







