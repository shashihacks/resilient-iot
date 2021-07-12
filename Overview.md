## RIoTI project B: Resilient	smart	irrigation	system



### Introduction


This project aims at implementing a resilient irrigation system, that operates on programmed schedules. We make use of IoT devices and components to monitor weather and soil conditions, and adjust the irrigation schedule aptly based on the local conditions. This system is enabled with a control logic that is capable of notifying the user about the irrigation parameters and conditions. Any failure in the component or the failure of the edge node itself is quicky recognised, accounted and adjusted for, as well as notified to the user.

Such systems prove to have quite a few advantages. These systems will not only help users save time and financial resources, but also ensure that only the right amount of water is used for irrigation. Irrigating sparsely and only when required saves water, and is highly beneficial to plants, as both over-irrigating and under-irrigating have negative implications on plant growth and yields. The system also help enhance the beauty and health of local landscapes.


### Project Description

Our project uses a combination of various monitoring sensors, various microcontrollers for logic implementation and use various weather forecast APIs couples with cloud based storage capabilities. Given below is an abstract implemention of the project itself.

![project setup](https://user-images.githubusercontent.com/86833585/125267344-fedae780-e306-11eb-84a3-3f4f49ae9c0a.jpg)


### Task Descriptions

#### Task 1: Sensor setup and getting data from the sensors. (Pranav)

Sensors:
- KY 028 temp sensors
- Capacitive soil moisture sensor v1.2
- Mh-rd raindrop sensor

Microcontrollers:
- Raspberry pi 4
- Wroom wifi ESP32

Task Description:

- The main aim of this task is to gather sensor readings and then transmit them to the raspberry pi, in order to be fed into the control logic. 
- Two of the three sensors, namely the KY028 temperature sensor and the Capacitive soil moisture sensor are only capable of providing analog inputs while the Mh-Rd raindrop module can provide both a digital and analog input.
- The raspberry pi is not capable of accepting any analog inputs.
- Analog inputs tend to be more sensitive and accurate as opposed to digital inputs, and thus were of more importance.
- As such, an ESP32 WiFi enabled dev board was used instead to connect to the sensors and gather data.
- While the code collects data, it also checks if the sensor values are in the correct range, and verifies that the sensors work. If not, the code sends a predefined input that notifies the control logic of failing sensors or incorrect data.

The figure below shows the sensor values, their input type and input value range with it's indication.

|Sensor|Input Type|Input Range and Indication|
|---|---|---|
|Rain Sensor|Digital|{0 = No rain} & { 1 = Rain}|
|Rain Sensor|Analog|Ranging from { 4095 = No rain } to {0 = Heavy rain }|
|Soil Moisture Sensor|Analog|Ranging from { 0 - 300 : Low moisture} { 300 - 700 : Medium Moisture} {700 - 1200 : High Moisture}
|Temperature Sensor|Analog|Value in Celcius|


#### Task 2: Using MQTT protocol over WiFi to transport data from ESP32 [publisher] to Raspberry pi [broker + subscriber] (Pranav)

The ESP32 board has WiFi capabilities, and as such, the easiest way to send data over WiFi was via the MQTT protocol

__Structure of MQTT protocol:__

MQTT stands for Message Queuing Telemetry Transport, and the protocol works on a Publish/Subscribe based Machine-to-Machine communication. The system consists of a ‘publisher’ that publishes messages, a ‘subscriber’ that subscribes to these messages and a ‘broker’ that acts as an intermediary between these two.

![MQTT Basic (3)](https://user-images.githubusercontent.com/86833585/125269537-161ad480-e309-11eb-921e-c06e17721698.jpg)

Some features of MQTT that are of interest to us are as follows: 
- MQTT protocol is bi-direction in nature, thus allowing all subsystems to interact with each other.
- MQTT maintains a stateful session awareness, and thus if our sensor gets disconnected from the system, MQTT will notify us regarding it.
- MQTT is lightweight in nature, and does not have stringent computing resource requirements. This is again in our favour, as the ESP32 board has limited computing power.
- Being lightweight in nature, MQTT consumes less energy, making it suitable for use with battery operated nodes.

__Our Setup for MQTT:__

![our setup (1)](https://user-images.githubusercontent.com/86833585/125269582-203cd300-e309-11eb-8c42-9584ea50a97b.jpg)


__MQTT Publisher:__
![Screenshot from 2021-07-11 11-14-18](https://user-images.githubusercontent.com/86833585/125239659-3fc40380-e2e9-11eb-825f-50aa8128b26f.png)

- We enable the ESP32 board  to act as the MQTT Publisher. 
- It publishes sensor data every 10 mins to the broker. The ‘PubSubClient’ library is used to establish MQTT connections and publish messages to the MQTT broker.
- The publisher publishes messages across four topics, intended for the four sensor inputs.The topics that we assign are:
        /farm/analog_rain
        /farm/dig_rain
        /farm/moisture
        /farm/temperature
        
The figure below shows the 'ESP32' sucessfully publishing data to 'MQTT broker'.   
![Screenshot from 2021-07-11 11-15-35](https://user-images.githubusercontent.com/86833585/125239455-f673b400-e2e8-11eb-958c-56ee3de46ff9.png)

The figure below shows a failed 'ESP32' connection.
![Screenshot from 2021-07-11 11-17-34](https://user-images.githubusercontent.com/86833585/125239464-fa9fd180-e2e8-11eb-9bd2-ad4de88fc357.png)

__MQTT Broker:__
- We use the Raspberry pi as the broker. 
- For this, the Mosquito software is installed on the Pi, and configured such that no unauthorized device can connect and publish or subscribe to the broker.
- A username and password is set for the broker to be accessed. 
- The default port ‘1883’ is used to listen to all communications.

The figure below shows the 'Broker' reporting publisher connection along with 'publisher' identity.
![Screenshot from 2021-07-11 11-14-18](https://user-images.githubusercontent.com/86833585/125239672-4783a800-e2e9-11eb-9e9d-458f4d1f14ef.png)

The figure below shows the 'Broker' reporting failed publisher connection
![Screenshot from 2021-07-11 11-14-48](https://user-images.githubusercontent.com/86833585/125239685-4d798900-e2e9-11eb-9949-31b3c5e214d4.png)

__MQTT Client:__
- The Raspberry pi acts as the ‘client’ device as well, and subscribes to the messages of the topic “farm/#”. The wildcard ‘#’ enables the client to listen on any topic that has a main heading of ‘farm’. 
- The client runs a python script that reads all the messages on our subscribed topic.
- These values are then saved in a JSON format file, and passed on to the control logic.

#### Task 3: Control logic (Shashi)

1. Set up the account with  `openweathermap`  and connect the api.
2. Get the data from the `openwathermap` api and save. The relevant data(e.g by specifying city, pincode and country) from the api and filter the corresponding keys necessary is procured.
3. Create and save objects that combine the sensor data and api data.
4. validate the input data for identifying the sensor state
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

1. If soil moisture is less than 300 (No moisture) and Ananlog rain sensors value is greater than 3000 (No rain), then irrigates for certain amount of time (5 minutes chosen in our case).
2. This is run as scheduled task and checked for every hour


__Fault Tolerance and Replication__ (Dealing with sensor failures)

1. If the Analog or rain sensor value is fault, the corresponding values are replaced with the data from cloud api, depending on the received conditions for the day.
2. Senors data is alwyas writting to `json` file and stored on the edge device
3. Sensors state at any point is saved in a file, depending upon the obatained values, a value of `1` is written if it is working and `0` if data is faulty.
4. A cron job is setup to run every 30 minutes to save the current sensors state and values into the cloud store along with its timestamp.


__Detecting Liveness of Edge node__

1. Cron job that is set up pings the machine in local network every 30 minutes to indicate that it is alive.


__Failure of Internet connectivity__
1. In case of network  and sensor failure, warning message is show to user.


#### Task 4: Checkpointing and recovery

- The sensor data is written to local file system and also, is sent to the `firebase`. (`replication`)
- In case of data loss in the local file system, the data can be fetched from the cloud database. (`recovery`)
- In case of edge node failure,  sensor data is retrieved from the cloud and stored in the new node when initialised to continue from the last step of the old edge node. (`checkpoint`)



#### Task 5: Test Runs and Cases (Aurika)

- The code was tested by random input variables to ensure that the logic control was sound and that the system worked as desired.
- The following input parameters were feeded into the system, shown along with the outcomes.

|Test Case| Case 1 | Case 2| Case 3 | Case 4 | Case 5 |
|---|---|---|---|---|---|
|Analog Rain Input| 2000 | 4095 | 3500  | 9999 (Replaced with cloud api = No Rain) | 4095 |
|Soil Moisture Input| 100 | 700 | 250 | 150 | 9999 |
|Output| No Irrigation | No Irrigation | Irrigation | Irrigation | No Irrigation (Sensor failure) |

Given below are the results of the test runs:

- Test Case 1

![test1](https://user-images.githubusercontent.com/86833585/125242893-94697d80-e2ed-11eb-89ce-2e99b81a421d.png)


- Test Case 2

![test2](https://user-images.githubusercontent.com/86833585/125242908-98959b00-e2ed-11eb-903b-3a67facf3f2b.png)


- Test Case 3

![test3](https://user-images.githubusercontent.com/86833585/125242915-9d5a4f00-e2ed-11eb-848d-58be48091723.png)


- Test Case 4

![test4](https://user-images.githubusercontent.com/86833585/125242919-a0553f80-e2ed-11eb-9cfb-fd062e06bc76.png)


- Test Case 5

![test5](https://user-images.githubusercontent.com/86833585/125242924-a3503000-e2ed-11eb-8e5a-8b4902bbb36c.png)





 



