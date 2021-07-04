from os import write
import urllib
import json
import pprint
import urllib.request
api = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=0b7c4978dda884bbfb0397d03033509f"
sapi = "http://api.openweathermap.org/data/2.5/forecast/daily?zip=94032&appid=0b7c4978dda884bbfb0397d03033509f" 

saapi = "http://api.openweathermap.org/data/2.5/weather?q=Passau&appid=0b7c4978dda884bbfb0397d03033509f"
# response = urllib.request.urlopen(saapi)
# print(response)
# output = response.read().decode('utf-8')
# print(output)
lastRecorded = 60
sensor_state = {
      
    "Analog_Rain": 1,
    "Digital_Rain": 1,
    "Temp": 1,
    "Soil_Moisture": 1,

}

irrgatedToday = False

# Reading Sensor data 
with open("sensors.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

currentSensorvalues = jsonObject[0]
print(currentSensorvalues)
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

def showWarnings():
    print("Sensors have failed and could not fetch data from cloud")
    exit(1)

def getCurrentWeatherConditions():
    response = urllib.request.urlopen(saapi)
    output = response.read().decode('utf-8')
    return  json.loads(output)

def irrigate(time):
    print(sensor_state)
    print("Irrgating for "+ str(time) + " minutes")
    irrgatedToday = True
    

def doNotIrrigate(time):
    print(sensor_state)
    print("Not irrigating now")

def getEstimatedMoisture():
    #  decreases in time , check the last recorded value
    return 400

def controlLogic():
    # print("logic", currentSensorvalues)

    # Fix missing sensor data with api
    try:
        cloud_data = getCurrentWeatherConditions()
    except:
        cloud_data = "Unable to fetch"
    # pprint.pprint(cloud_data)
    if(currentSensorvalues['Soil_Moisture'] == 9999):
        currentSensorvalues['Soil_Moisture'] = getEstimatedMoisture()
        sensor_state['Soil_Moisture'] = 0

 
    if ( currentSensorvalues['Digital_Rain'] == 9999 or  currentSensorvalues['Analog_Rain'] == 9999):
         sensor_state['Digital_Rain'] = 0
         sensor_state['Analog_Rain'] = 0
         if(cloud_data == 'Unable to fetch'):
             return showWarnings()
             
        #  print("cloud data rain", cloud_data['weather'][0]['main']) 
            

         if(cloud_data['weather'][0]['main']=='Rain' or cloud_data['weather'][0]['main']=='Light rain'):
             currentSensorvalues['Digital_Rain'] = 1
             print(currentSensorvalues)
             currentSensorvalues['Analog_Rain'] = 2500
             

         else:
            currentSensorvalues['Digital_Rain'] = 0
            currentSensorvalues['Analog_Rain'] = 4000



    if( currentSensorvalues['Soil_Moisture'] <300 and  (currentSensorvalues['Analog_Rain']>3000 and currentSensorvalues['Analog_Rain']<4500)):
        irrigate(5)
    else:
        doNotIrrigate(5)




controlLogic()






