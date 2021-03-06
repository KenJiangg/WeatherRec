from flask import Flask, jsonify, request, render_template
from flask_cors import CORS 
import uuid
import requests
import weathers 
# configuration
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
ERROR = [1]
COORDS = [
    {
        "coords": [ 42.8867166, -78.8783922 ],
        "title": "Buffalo",
        "weather": weathers.getWeather("Buffalo")
    },
    {
        "coords": [ 40.7308619, -73.9871558 ],
        "title": "New York City",
        "weather": weathers.getWeather("New York City")
    },
]
LOCATIONS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Buffalo',
        'emoji': COORDS[0]['weather']['emoji']
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'New York City',
        'emoji': COORDS[1]['weather']['emoji']
    }
]
LOWKEY = ['Buffalo','New York City']
#Gets the list of current cities and can also be used to add new cities
@app.route('/index', methods=['GET', 'POST'])
def all_weather():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        if request.json['title'] in LOWKEY: 
            ERROR.append(2)
        else:
            ifvalid = weathers.getLats(request.json['title'])
            if len(ifvalid) == 2:
                COORD = {
                    "coords" : ifvalid,
                    "title": request.json['title'],
                    "weather": weathers.getWeather(request.json['title'])
                }
                COORDS.append(COORD)
                LOCATION = {
                    'id': uuid.uuid4().hex,
                    'title':request.json['title'],
                    'emoji': COORD['weather']['emoji']
                }
                LOCATIONS.append(LOCATION)
                LOWKEY.append(request.json['title'])
                ERROR.append(1)
            else:
                ERROR.append(0)
    else:
        response_object['yourLoc'] = LOCATIONS
        response_object['lat_long'] =  COORDS
        if ERROR[-1] == 1:
            response_object['message'] = 'Location Added!'
        elif ERROR[-1] == 0:
            response_object['message'] = 'Location entered is not valid!'
        elif ERROR[-1] == 2:
            response_object['message'] = 'Location already entered'
    return jsonify(response_object)

#Deletes and Updates Cities in the list 
@app.route('/index/<loc_ID>', methods=['PUT', 'DELETE'])
def single_location(loc_ID):
    response_object = {'status': 'success'}
    '''
    if request.method == 'PUT':
        remove_location(loc_ID)
        LOCATION = {
            'id': uuid.uuid4().hex,
            'title':request.json['title']
        }
        LOCATIONS.append(LOCATION)
        response_object['message'] = 'Location updated!'
    '''
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

#Weather Dashboard Back-end
@app.route('/index/weather', methods=['PUT'])
def openWeather():
    #response_object = {'status' : 'success'}
    # Google Maps API #
    weather_title = request.json['title']
    response_object = weathers.makeGraphData(weather_title)
    return jsonify(response_object)
if __name__ == '__main__':
    app.run()