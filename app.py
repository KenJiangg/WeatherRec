from flask import Flask, jsonify, request
from flask_cors import CORS 
from geolocation.main import GoogleMaps 

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
        'title': 'Buffalo',
    }
]
@app.route('/index', methods=['GET','POST'])
def index():
    address = 'Buffalo'
    google_maps = GoogleMaps(api_key='API KEY') #API KEY
    location = google_maps.search(location=address) # sends search to Google Maps.
    mylocation=location.first() #uses first location query  
    lat=mylocation.lat
    lng=mylocation.lng    
    loc = {'location':'%f,%f' % (lat,lng)}
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        LOCATIONS.append({
            'title': post_data.get('title')
        })
        response_object['message'] = 'Location added!'
    else:
        response_object['yourLoc'] = LOCATIONS
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()