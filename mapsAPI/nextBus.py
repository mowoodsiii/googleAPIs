# Getting started with Maps API: https://developers.google.com/maps/documentation/directions/start
# Getting started with JSON requests: docs.python-requests.org/en/latest/user/quickstart/

import requests
import json
from datetime import datetime
import time

now = time.time()
timeConvert = 7*60*60

APIkey_directions = 'AIzaSyADI5yFi7H8233XBzqiXcUVwBsYqb-roBo'
APIkey_timezone = 'AIzaSyBGmEW9QvM8fjMgJYprlipOOYi_SIz2Qyg'

origin = 'Integrated+Teaching+Learning+Laboratory+Boulder+Colorado'
destination = '817+Orman+Drive+Boulder+Colorado'
travelMode = 'transit'
alternatives = 'true'

requestURL = 'https://maps.googleapis.com/maps/api/directions/json?origin='+origin+'&destination='+destination+'&mode='+travelMode+'&alternatives='+alternatives+'&key='+APIkey_directions

response = requests.get(requestURL)
if(response.status_code==requests.codes.ok):
    print('Response Received!')
else:
    print('Request Failed: ' + response.status_code)

directions = json.loads(response.content)

routes = directions['routes']
print('Routes found: '+str(len(routes)))

leg=[]
routeTypes=[]
for i in range(0,len(routes)):
    routeTypes.append([])
    temp_routeSteps = routes[i]['legs'][0]['steps']
    leg.append(temp_routeSteps)
    print('   Route '+str(i)+' has '+str(len(leg[-1]))+' steps:')
    for step in leg[-1]:
        temp_travelMode = step['travel_mode']
        temp_string = '      '+temp_travelMode
        if temp_travelMode == 'TRANSIT':
            temp_name =  step['transit_details']['line']['short_name']
            temp_depart = step['transit_details']['departure_time']['value']
            temp_lat = step['start_location']['lat']
            temp_lng = step['start_location']['lng']
            requestURL = 'https://maps.googleapis.com/maps/api/timezone/json?location='+str(temp_lat)+','+str(temp_lng)+'&timestamp='+str(temp_depart)+'&key='+APIkey_timezone
            response = requests.get(requestURL)
            temp_timezone = json.loads(response.content)
            temp_timezone_offset = temp_timezone['dstOffset']+temp_timezone['rawOffset']
            temp_depart = temp_depart + temp_timezone_offset
            routeTypes[-1].append({'method':temp_name,'departs':temp_depart})
            temp_string = temp_string+" ("+temp_name+" at "+datetime.fromtimestamp(temp_depart).strftime('%I:%M %p ')+")"
        else:
            temp_duration = step['duration']['value']
            routeTypes[-1].append({'method':'walking','duration':temp_duration})
            temp_string = temp_string+" (for "+str(temp_duration/60)+" minutes)"
        print(temp_string)

nextBus = {'STAMPEDE':9999999999,'209':9999999999}
for route in routeTypes:
    for step in route:
        if (step['method']=='209') and (step['departs']<nextBus['209']):
            nextBus['209']=step['departs']
        elif step['method']=='STAMPEDE' and (step['departs']<nextBus['STAMPEDE']):
            nextBus['STAMPEDE']=step['departs']
now = now+temp_timezone_offset
nextBus['209']=int(round((nextBus['209']-now)/60))
nextBus['STAMPEDE']=int(round((nextBus['STAMPEDE']-now)/60))
print('')
print('Next 209 in '+str(nextBus['209'])+' minutes')
print('Next STAMPEDE in '+str(nextBus['STAMPEDE'])+' minutes')

