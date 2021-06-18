import urllib

import urllib.request
api = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=0b7c4978dda884bbfb0397d03033509f"

sapi = "http://api.openweathermap.org/data/2.5/forecast/daily?zip=94032&appid=0b7c4978dda884bbfb0397d03033509f" 

saapi = "http://api.openweathermap.org/data/2.5/weather?q=Passau&appid=0b7c4978dda884bbfb0397d03033509f"
response = urllib.request.urlopen(saapi)
print(response)
output = response.read().decode('utf-8')

print(output)
