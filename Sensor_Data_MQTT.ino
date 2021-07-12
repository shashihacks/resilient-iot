  
#include <WiFiServer.h>
#include <WiFiClient.h>
#include <WiFi.h>
#include <PubSubClient.h> 
#include <ArduinoJson.h>
#include <SPI.h>
#include <Wire.h>
#include <math.h>

const char* ssid = "deopranav";
const char* wifi_password = "M4nj4r@linux";

const char* mqtt_server = "192.168.0.245";
const char* mqtt_topic = "/deopranav/trial";
const char* mqtt_username = "deopranav";
const char* mqtt_password = "incorrect";
const char* clientID = "myesp32";

const char* a_rain_topic = "farm/analog_rain";
const char* d_rain_topic = "farm/dig_rain";
const char* moisture_topic = "farm/moisture";
const char* temp_topic = "farm/temperature";

#define soilAnalog 14 // Pins for soil sensor
#define rainAnalog 35 // Pins for rain sensors
#define rainDigital 34
#define tempAnalog 26 //Pin for KY-028 temp sensor

int temp_value = 0;
float i = 0;
float fixtemp = 20.;
int fixInput = 560;
float fixedDegreeValue = 5.5;

const int AirValue = 3620;    // Calibration needed
const int WaterValue = 1680;  // Calibration needed
int moisture_value = 0;
int moisture_percent =0;

WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); 


void setup() {
 
  Serial.begin(115200);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
  
}

void loop() {

  int a_rain_value = analogRead(rainAnalog);
  int d_rain_value = digitalRead(rainDigital);

  temp_value = analogRead(tempAnalog);  
  fixtemp = 20;
  if (temp_value > fixInput ){  
    i = temp_value - fixInput;
    i = i /fixedDegreeValue; 
    fixtemp = fixtemp - i;
    
  }  
  else if(temp_value < fixInput)
  {
    i =  fixInput - temp_value;
    i = i /fixedDegreeValue; 
    fixtemp = fixtemp + i;
  }
  else if(temp_value == fixInput ){    
   fixtemp = 20;
  }

  moisture_value = analogRead(soilAnalog);  
  moisture_percent = map(moisture_value, AirValue, WaterValue, 0, 100);

//value check

 if( d_rain_value < 0 or d_rain_value > 4095){
    d_rain_value = 9999;
  }
  if( fixtemp < 0 or fixtemp > 75){
    fixtemp = 9999;
  }
  if( moisture_value < 0 or moisture_value > 1100){
    moisture_value = 9999;
  }

//print 

  Serial.print("\t rain_Analog_val: ");
  Serial.println(a_rain_value);
  Serial.print("\t rain_Digital_val: ");
  Serial.println(d_rain_value);

  Serial.print(" \t Temperature: ");
  Serial.print(fixtemp);
  Serial.println(" C");

  Serial.print("\t Soil_Moisture: ");
  Serial.println(moisture_value);
  Serial.print("\t Soil_Moisture_Percent: ");
  Serial.println(moisture_percent); 

// MQTT Strings & Publish

String moist="Moisture:"+ String(int(moisture_value));
String a_rain= "Analog Rain:" + String(int(a_rain_value));
String d_rain= "Digital Rain:" + String(int(d_rain_value));
String temp_send ="Temperature:" + String(float(fixtemp));

if (client.publish(a_rain_topic, String(a_rain).c_str())) {
      Serial.println("Analog rain value sent" + a_rain);
    }
else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
      client.connect(clientID, mqtt_username, mqtt_password);
      delay(10);
      client.publish(a_rain_topic,String(a_rain).c_str());
    }
 
 if (client.publish(d_rain_topic, String(d_rain).c_str())) {
      Serial.println("Digital rain value sent");
    }
else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
      client.connect(clientID, mqtt_username, mqtt_password);
      delay(10);
      client.publish(d_rain_topic, String(d_rain).c_str());
    }
  
if (client.publish(moisture_topic, String(moist).c_str())) {
      Serial.println("Moisture value sent");
    }
else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
      client.connect(clientID, mqtt_username, mqtt_password);
      delay(10);
      client.publish(moisture_topic, String(moist).c_str());
    }

if (client.publish(temp_topic, String(temp_send).c_str())) {
      Serial.println("Temp value sent");
    }
else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
      client.connect(clientID, mqtt_username, mqtt_password);
      delay(10);
      client.publish(temp_topic, String(temp_send).c_str());
    }

 delay(3000);
}
