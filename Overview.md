## RIoTI project B: Resilient	smart	irrigation	system



### Introduction

Irrigation system controllers operate on progammed schedules and timer, While this project aims to use IoT devices and components to monitor weather, soil conditions,  and water usage to automatically adjust the watering schedule depending on the local conditions. In this project we aim to provide smart irrigation by setting up the monitoring system that is capable of notifying the user for irrigation by displaying the right conditions that are determined through a control logic unit. The edge is setup in such a way, thjat the  user is notified in case of any component failure or failure of edge node itself. 




### Setup 
Task: Getting data from the sensors and using MQTT protocol over WiFi to transport data from ESP32 [publisher] to Raspberry pi [broker + subscriber]

__Sensors:__

- KY 028 temp sensors
- Capacitive soil moisture sensor v1.2
- Mh-rd raindrop sensor

__Microcontroller:__

- Raspberry pi 4
- Wroom wifi ESP32





### Description.

- An edge node is setup with moisture, rain and temperature sensors where it periodically collects the data, which in our case, set every 60 seconds.
- These sensors are calibrated to give the closest values.
- In case of failure of any component, or missing value from the sensor(which is either delayed or misread),  is replaced with the data obtained from `opeanweathermap` api.
- The api respond contains forecast data for the day for the current location and is fetched periodically which is set to run every 120 seconds.

- The application programs combines these two data sources and send to control logic unit, which determines when to irrgiate and display best time to irrigate.


#### Checkpointing and recovery

- The sensor data is written to local file system and also, is sent to the `firebase`. (`replication`)
- In case of data loss in the local file system, the data can be fetched from the cloud database. (`recovery`)
- In case of edge node failure,  sensor data is retrieved from the cloud and stored in the new node when initialised to continue from the last step of the old edge node. (`checkpoint`)




### Control logic (Shashi)

1. Get the data from the `openwathermap` api and save.
2. validate the input data for identifying the sensor state
    - `9999` indicates that  sensors has failed, as the read value is not in the acceptable range and state of the current sensors is shown to the user as warning.

__Senors value and its ranges__
    1. Analog rain 

|  Range |  Description |
|---|---|
|  1-2500 | High Rain  |
|  2500 - 3000 | Medium Rain  |
|  3000 - 4000 | Low Rain  |
|  4000 & above | No Rain  |

 2. Digital rain 

 |  Range |  Description |
|---|---|
|  1 |  Rain  |
|  0 | No Rain  |

3. Soil Moisture

 |  Range |  Description |
|---|---|
|  0-300 |  No - Low Moisture  |
|  300-700 | Medium Moisture  |
|700 & above | High Moisture|

__Determining condition to irrigate__
1. If soil moisture is less than 300 (No moisture) and Ananlog rain sensors value is greater than 3000 (No rain), then irrigates for ceratin amount of time (5 minutes chosen in our case).
2. This is run as scheduled task and checked for every hour


__Fault Tolerance and Replication__ (Dealing with sensor failures)

1. If the Analog or rain sensor value is fault, the corresponding values are replaved with cloud api, depending on the received conditions for the day.



2. Senors data is alwyas writting to `json` file and stored on the edge device
3. Sensors state at any point is saved in a file, depending upon the obatained values, a value of `1` is written if it is working and `0` if data is faulty.
4. A cron job is setup to run every 30 minutes to save the current sensors state and values into the cloud store along with its timestamp.


__Detecting Liveness of Edge node__

1. Cron job that is set up pings the machine in local network every 30 minutes to indicate that it is alive.


__Failure of Internet connectivity__
1. In case of network  and sensor failure, warning message is show to user.









## Test cases




### Task Overview (Shashi)

__Openweathermap__
1. Set up the account with  `openweathermap`  and connect the api.
2. Get releant data(e.g by specifying city, pincode and country) from the api and filter the corresponding keys necessary.
3. Create and save objects that combine the sensor data and api data.

__Firestore setup__
1. Setup the cloud database(`firestore`) and design the document structure to store sensors data.
2. Periodically post the sensor data to `firestore`.  

__Cronjob__
5. Written a `cronjob` to indicate the liveness of edge node.
6. Initialize the required data needed for edge node when replaced with new. 
7. Send data to cloudstore periodically
8. Delete the logs after saving the data to cloud.

__Control logic code__
1. Code the  control logic implementation that satsisifes irrigation needs.




### Task overview (Pranav)


__ESP32 and Sensor connections:__

- Wired connection between sensors to `EPS32`
- Digital and Analog inputs from the rain sensor
- Analog inputs from temp and soil moisture sensors
- Use of Arduino code to receive sensor inputs to the serial monitor
- Use of `ArduinoJson` lib to write output to a JSON file.



__USING MQTT TO ESTABLISH CONNECTION BTW ESP32 AND RASP-Pi__

__Setup folder structure used:__

- fieldname/cropname/temp
- fieldname/cropname/rain_analog
- fieldname/cropname/rain_digital
- fieldname/cropname/soil_moisture

__Setting MQTT broker to receive data:__

1. Install mosquito and required libs
2. Modify the default Mosquitto config at /etc/mosquitto/conf.d 
3. Removed anonymous logins
4. Save passwords in separate files
5. Use port 1883
6. Set up a new username & password

__Setup WiFi connection on ESP32 and enable MQTT Publish__

- Use PubSubClient lib for enabling `MQTT` publishing and use WiFILibrary for enabling WiFi.
- Use `connect_MQTT()` to connect to the broker
- Publish data over `MQTT` 


__Setup subscriber to recieve data from broker__

- Install python mqtt language bindings (`paho-mqtt`)
Python script to check what happened to connection.

- `on_connect()` - callback for client recieving a CONNACK from broker
- `on_message()` for callback when PUBLISH message from broker



__Task Overview: (Aurika)__
__Decide the control logic of irrigation (how much to put water), depending on local sensor data.__
- We have three input variables, such as a temperature sensor, a soil moisture sensor, and a rain sensor. 
- All three variables have their measurements of values. At this step, after obtaining all input values we must convert them into the actual soil moisture value. 
- The other block which we should consider calculating a value position is the desired soil moisture. It should calculate desired soil moisture that is different for any kind of plant, type of growth, and kind of soil. 
- Two measurements (The actual soul moisture based on sensors and desired soil moisture) should be compared and extract one measurement in the range between 0 and 100. 
- The soil evaporation model (the actual soil moisture) considers the evaporation of the ground and translates back the amount of water added into the soil moisture in the ground.
- Based on references and , the input values are defined in the range between – 100 and 100. For taking the decision when we should put water based on fuzzy logic, the authors implement the control system as if the desired moisture value is larger or equal than the actual moisture value, a valve should be closed. If the desired moisture value is less than the actual moisture value, then we should open a valve for irrigating.  



