import paho.mqtt.client as mqtt
import json

mqtt_username = "deopranav"
mqtt_password = "incorrect"
mqtt_topic = "farm/#"
mqtt_broker_ip = "192.168.0.245"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)

def on_connect(client, userdata, flags, rc):
    print ("Connected!", str(rc))
    client.subscribe(mqtt_topic)
 
sensorsvalue = {}
sensors    = []
def on_message(client, userdata, msg):
    message = (msg.payload).decode("UTF-8")
      
    if (msg.topic == "farm/temperature"):
        temp = message.split(":")
        sensorsvalue['Temperature'] = float(temp[1])
        
    if (msg.topic == "farm/analog_rain"):
        a_rain = message.split(":")
        sensorsvalue['Analog_Rain'] = int(a_rain[1])

    if(msg.topic == "farm/dig_rain"):
        d_rain = message.split(":")
        sensorsvalue["Digital_Rain"] = int(d_rain[1])

    if(msg.topic == "farm/moisture"):
        moist = message.split(":")
        sensorsvalue["Soil_Moisture"] = int(moist[1])
        
        
    print("Values of sensors: " , sensorsvalue)
    
    sensors.append(sensorsvalue)
    
    
    with open('sensors.json', 'w') as outfile:
        json.dump(sensors ,outfile)
        
    outfile.close()
    
    print(sensors, "sensors as array")
  
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)

client.loop_forever()
client.disconnect()
