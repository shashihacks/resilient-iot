## RIoTI project B: Resilient	smart	irrigation	system



### Introduction

Irrigation system controllers operate on progammed schedules and timer, While this project aims to use IoT devices and components to monitor weather, soil conditions,  and water usage to automatically adjust the watering schedule depending on the local conditions. In this project we aim to provide smart irrigation by setting up the monitoring system that is capable of notifying the user for irrigation by displaying the right conditions that are determined through a control logic unit. The edge is setup in such a way, thjat the  user is notified in case of any component failure or failure of edge node itself. 



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
3. Periodically post the sensor data to cloud(firebase).  
4. Write a cronjob to indicate the liveness of edge node.
5. Initialize the required data needed for edge node when replaced with new. 
6. Provide necessary data for the control logic 
7. Code the part of control logic implementation