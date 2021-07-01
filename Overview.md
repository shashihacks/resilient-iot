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




### Control logic









### Task Overview (Shashi)

1. Get data from the `openweathermap` api and filter the corresponding keys necessary.
2. Create objects that combine the sensor data and api data
3. Setup the cloud database(`firebase`) and design the document structure.
4. Periodically post the sensor data to cloud(firebase).  
5. Write a `cronjob` to indicate the liveness of edge node.
6. Initialize the required data needed for edge node when replaced with new. 
7. Provide necessary data for the control logic. 
8. Code the part of control logic implementation.




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


