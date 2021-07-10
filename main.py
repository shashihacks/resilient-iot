from os import write
import urllib
import json
import pprint
import urllib.request
from datetime import date
import time
api = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=0b7c4978dda884bbfb0397d03033509f"
sapi = "http://api.openweathermap.org/data/2.5/forecast/daily?zip=94032&appid=0b7c4978dda884bbfb0397d03033509f" 

saapi = "http://api.openweathermap.org/data/2.5/weather?q=Passau&appid=0b7c4978dda884bbfb0397d03033509f"

sensor_state = {
    "Analog_Rain": 1,
    "Digital_Rain": 1,
    "Temp": 1,
    "Soil_Moisture": 1,
}

def getDate():
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    return d1

irrigation_state = {
    "irrgatedToday" : False,
    "date": getDate()
}


# Reading Sensor data 
with open("sensors.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

currentSensorvalues = jsonObject[0]
lastMoistureValue = {

}
if(currentSensorvalues['Soil_Moisture'] <= 1200):
    lastRecordedMoistureValue = currentSensorvalues['Soil_Moisture']
    lastRecordedTime =timestamp = int(time.time()*1000.0)
    lastMoistureValue['Soil_Moisture'] =  lastRecordedMoistureValue
    lastMoistureValue['time'] = lastRecordedTime


print(currentSensorvalues)


def saveState():
    print("saving state to a file")
    with open("sensors_state.json", "w") as f:
        print("writing")
        json.dump(sensor_state, f)
    f.close()


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
    saveState()
    

def doNotIrrigate(time):
    print(sensor_state)
    print("Not irrigating now")
    saveState()


def getEstimatedMoisture():
    #  decreases in time , check the last recorded value
    currentTemperature = currentSensorvalues['Temperature']
    currentTimestamp = int(time.time()*1000.0)
    difference = currentTimestamp -  lastMoistureValue['time']
    moist = currentSensorvalues['Soil_Moisture'] - ((difference/1000) * currentTemperature)
    return moist

def controlLogic():

    # Fix missing sensor data with api
    try:
        cloud_data = getCurrentWeatherConditions()
    except:
        cloud_data = "Unable to fetch"
    # pprint.pprint(cloud_data)
    if(currentSensorvalues['Soil_Moisture'] == 9999):
        # currentSensorvalues['Soil_Moisture'] = getEstimatedMoisture()
        # print("estimated moisture")
        # print(currentSensorvalues['Soil_Moisture'])
        sensor_state['Soil_Moisture'] = 0

 
    if ( currentSensorvalues['Digital_Rain'] == 9999 or  currentSensorvalues['Analog_Rain'] == 9999):
         sensor_state['Digital_Rain'] = 0
         sensor_state['Analog_Rain'] = 0
         if(cloud_data == 'Unable to fetch'):
             return showWarnings()            

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






