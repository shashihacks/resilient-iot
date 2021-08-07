import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import time
import os



ip_address = "192.168.1.2"
port = 4444
firebaseConfig = {
  'apiKey': "AIzaSyBqfc4B-gg7wBvqC1QBQMeq1giC1HpcYwc",
  'authDomain': "resilient-c8d95.firebaseapp.com",
  'projectId': "resilient-c8d95",
  'storageBucket': "resilient-c8d95.appspot.com",
  'messagingSenderId': "60843286594",
  'appId': "1:60843286594:web:52eeb949ced715f6cc0ddb",
  'measurementId': "G-XE7KRGQW2Z"
};
# Use the application default credentials


cred = credentials.Certificate("./creds.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
with open("sensors.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
data = jsonObject


# send sensors state to cloud
with open("sensors_state.json") as stateFile:
    jsonObject = json.load(stateFile)
    stateFile.close()
state_data = jsonObject

print(data)
print(time.time(), "time")
timestamp = int(time.time()*1000.0)
print(timestamp)
try:
    
    db.collection(u'sensors').document(f"{timestamp}").set(data[0])
    db.collection(u'state').document(f"{timestamp}").set(state_data)
except:
    print("unable to connect or send data")


os.system("nc " + ip_address  +" " + port )
timestamp = int(time.time()*1000.0)
print(timestamp)

# Delete the files
# os.remove("sensors.json")
# os.remove("sensors_state.json")
