from flask import Flask, jsonify, request, render_template
from flask_cors import CORS 
from geolocation.main import GoogleMaps 
import uuid
import requests

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
LOCATIONS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Buffalo',
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'New York City',
    }
]
@app.route('/index', methods=['GET', 'POST'])
def all_weather():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        LOCATION = {
            'id': uuid.uuid4().hex,
            'title':request.json['title']
        }
        LOCATIONS.append(LOCATION)
        response_object['message'] = 'Location added!'
    else:
        response_object['yourLoc'] = LOCATIONS
    return jsonify(response_object)

@app.route('/index/<loc_ID>', methods=['PUT', 'DELETE'])
def single_location(loc_ID):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        remove_location(loc_ID)
        LOCATION = {
            'id': uuid.uuid4().hex,
            'title':request.json['title']
        }
        LOCATIONS.append(LOCATION)
        response_object['message'] = 'Location updated!'
    if request.method == 'DELETE':
        remove_location(loc_ID)
        response_object['message'] = 'Location removed!'
    return jsonify(response_object)
def remove_location(loc_ID):
    for loc in LOCATIONS:
        if loc['id'] == loc_ID:
            LOCATIONS.remove(loc)
            return True
    return False

@app.route('/index/weather', methods=['PUT'])
def openWeather():
    response_object = {'status' : 'success'}
    # Google Maps API #
    weather_title = request.json['title']
    google_maps = GoogleMaps(api_key='AIzaSyA5woJnkAkBYXLBgrTv9CX9j_C0Lrv6yvY') #API KEY
    location = google_maps.search(location=weather_title) # sends search to Google Maps.
    mylocation=location.first() #uses first location query  
    lat=mylocation.lat
    lng=mylocation.lng 

    # Dark Sky API # 
    response = requests.get('https://api.darksky.net/forecast/de94c907962cc871c040f2f15a3562e1/' + str(lat) + ',' + str(lng))
    data = response.json()
    weather_icon = str(data['currently']['icon'])
    temperature = str(int(data['currently']['temperature']))
    temperatureMax = data['daily']['data'][0]['temperatureHigh']
    temperatureMin = data['daily']['data'][0]['temperatureLow']
    RAIN_WARNING = data['daily']['data'][0]['precipProbability']
    if RAIN_WARNING == 0:
        rain_commentary = "No rain today"
    elif 0 < RAIN_WARNING <= .5:
        rain_commentary = "Unlikely to rain but grab your umbrella if you're wary"
    elif  RAIN_WARNING > .5:
        rain_commentary = "Grab your umbrella, you'll need it"
    
    
    weather_info = [{
        'temperature' : temperature,
        'max' : temperatureMax,
        'min' : temperatureMin,
        'rain' : rain_commentary
    }]
    response_object['location'] = str(weather_title)
    response_object['icon'] = weather_icon
    response_object['info'] = weather_info
    return jsonify(response_object)
if __name__ == '__main__':
    app.run()