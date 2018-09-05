from flask import Flask, jsonify, request
from flask_cors import CORS 
from geolocation.main import GoogleMaps 
import uuid

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

@app.route('/index/<index_id>', methods=['PUT'])
def single_location(location_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        remove_location(location_id)
        LOCATION = {
            'id': uuid.uuid4().hex,
            'title':request.json['title']
        }
        LOCATIONS.append(LOCATION)
        response_object['message'] = 'Location updated!'
    else:
        response_object['yourLoc'] = LOCATIONS
    return jsonify(response_object)
def remove_location(location_id):
    for loc in LOCATIONS:
        if loc['id'] == location_id:
            LOCATIONS.remove(loc)
            return True
    return False
if __name__ == '__main__':
    app.run()