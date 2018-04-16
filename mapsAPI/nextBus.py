# Getting started with Maps API: https://developers.google.com/maps/documentation/directions/start
# Getting started with JSON requests: docs.python-requests.org/en/latest/user/quickstart/

import requests

APIkey = 'AIzaSyADI5yFi7H8233XBzqiXcUVwBsYqb-roBo'
origin = '817+Orman+Drive+Boulder+Colorado'
destination = 'Integrated+Teaching+Learning+Laboratory+Boulder+Colorado'
travelMode = 'transit'
alternatives = 'true'

requestURL = 'https://maps.googleapis.com/maps/api/directions/json?origin='+origin+'&destination='+destination+'&mode='+travelMode+'&alternatives='+alternatives+'&key='+APIkey

response = requests.get(requestURL)
if(response.status_code==requests.codes.ok):
    print('Response Received!')
else:
    print('Request Failed: ' + response.status_code)
