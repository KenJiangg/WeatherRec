import requests
from opencage.geocoder import OpenCageGeocode
import time 

icon_database = [
    { 'name' : 'clear-day','link' : 'https://images.unsplash.com/photo-1522518961115-07c922089dd4?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=d6304d66e4c9199d1b80fbd5581f9538&auto=format&fit=crop&w=668&q=80'},
    { 'name' : 'clear-night', 'link' : 'https://images.unsplash.com/photo-1532978379173-523e16f371f2?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4b755064e507b39cc84a0fe8ec71e1e0&auto=format&fit=crop&w=1350&q=80'},
    { 'name' : 'rain', 'link' : 'https://images.unsplash.com/photo-1517842187497-033b8b8cea1e?ixlib=rb-0.3.5&s=12c41e56a023d84e7d4ed05eb28b11b2&auto=format&fit=crop&w=668&q=80'},
    { 'name' : 'snow', 'link' : 'https://images.unsplash.com/photo-1511131341194-24e2eeeebb09?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=ca564acbbaae2f5f6f2f230a8822ea52&auto=format&fit=crop&w=1350&q=80'},        { 'name' : 'sleet', 'link' : 'https://images.unsplash.com/photo-1507181080368-cc2195abcde1?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=978125364de8367b8209b7b9a7e1fad5&auto=format&fit=crop&w=1778&q=80'},
    { 'name' : 'wind', 'link' : 'https://images.unsplash.com/photo-1530466273513-3626af215477?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=b0027c02f3703403f20a342d59a04bb5&auto=format&fit=crop&w=668&q=80'},
    { 'name' : 'fog', 'link' : 'https://images.unsplash.com/photo-1519982714547-54ccfb2c121e?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=8426b2784b877ef59b32c1e50c0bfeb6&auto=format&fit=crop&w=1373&q=80'},
    { 'name' : 'cloudy', 'link' : 'https://images.unsplash.com/photo-1500740516770-92bd004b996e?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=060deca22958f2e0baa11467858a1252&auto=format&fit=crop&w=1352&q=80'},
    { 'name' : 'partly-cloudy-day', 'link' : 'https://images.unsplash.com/photo-1432059964050-d4eba2ef368a?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=b6e8e41824f404aa1c158ea165764076&auto=format&fit=crop&w=1778&q=80'},
    { 'name' : 'partly-cloudy-night', 'link' : 'https://images.unsplash.com/photo-1429305336325-b84ace7eba3b?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=91549c9ca63cdfdc0470b956c22edfdf&auto=format&fit=crop&w=1350&q=80'}
]
'''
recAlbum_database = [
    { 'name' : 'weatherRain', 'link' : 'https://imgur.com/a/2gTNq'},
    { 'name' : 'weatherSnow', 'link' : 'https://imgur.com/a/D5ypX'},
    { 'name' : 'weatherCold', 'link' : 'https://imgur.com/a/9KoGi'},
    { 'name' : 'weatherWarm', 'link' : 'https://imgur.com/a/tpDEZ'},
    { 'name' : 'weatherBreezy', 'link' : 'https://imgur.com/a/0EhTi'},
    { 'name' : 'weatherNormal', 'link' : 'https://imgur.com/a/Aao8j'},
] 
'''
key = '41e4fb5354be4849ac0149710c4e3515'
geocoder = OpenCageGeocode(key)
def getLats(weather_title):
    result = geocoder.geocode(weather_title)
    if len(result) > 0:
        firstloc = result[0]
        arr = []
        arr.append(firstloc['geometry']['lat'])
        arr.append(firstloc['geometry']['lng'])
        return arr 
    else:
        string = 'not valid'
        return string 
def getWeather(weather_title):
    response_object = {}
    '''
    key = '41e4fb5354be4849ac0149710c4e3515'
    geocoder = OpenCageGeocode(key)
    result = geocoder.geocode(weather_title)
    firstloc = result[0]
    lat=firstloc['geometry']['lat']
    lng=firstloc['geometry']['lng']
    '''
    arr = getLats(weather_title)
    lat = arr[0]
    lng = arr[1]
    # Dark Sky API # 
    response = requests.get('https://api.darksky.net/forecast/de94c907962cc871c040f2f15a3562e1/' + str(lat) + ',' + str(lng))
    data = response.json()
    weather_icon = str(data['currently']['icon'])
    temperature = str(int(data['currently']['temperature']))
    temperatureMax = data['daily']['data'][0]['temperatureHigh']
    temperatureMin = data['daily']['data'][0]['temperatureLow']
    #RAIN_WARNING = data['daily']['data'][0]['precipProbability']
    #PRECIP_WARNING = data['daily']['data'][0]['precipType']
    #highWinds = data['daily']['data'][0]['windSpeed']
    #####
    #Rain Commentary #
    '''
    if RAIN_WARNING == 0 and PRECIP_WARNING == 'rain':
        rain_commentary = "No rain today"
    elif 0 < RAIN_WARNING <= .5 and PRECIP_WARNING == 'rain':
        rain_commentary = "Unlikely to rain but grab your umbrella if you're wary"
    elif  RAIN_WARNING > .5 and PRECIP_WARNING == 'rain':
        rain_commentary = "Grab your umbrella, you'll need it"
    '''
    #matches the weather icon with a picture related to the weather (one of fifteen)
    matches = [d['link'] for d in icon_database if d['name'] == weather_icon]
    matches = matches[0]
    #picture = str(matches[0])

    #packing the weather info into a dictionary 
    weather_info = {
        'temperature' : temperature,
        'max' : temperatureMax,
        'min' : temperatureMin,
        'matches' : matches
    }

    #matches the weather information to a clothing album (one of ten)
    '''
    clothes = ""
    if int(temperature) > 70:
        clothes = 'weatherWarm'
    if int(temperature) < 70 and int(temperature) > 40:
        clothes = 'weatherNormal'
    if int(temperature) < 40:
        clothes = 'weatherCold'
    if highWinds > 25:
        clothes = 'weatherBreezy'
    if RAIN_WARNING > .5 and PRECIP_WARNING == 'rain':
        clothes = 'weatherRain'
    if PRECIP_WARNING == 'snow':
        clothes = 'weatherSnow'
    recMatch= [d['link'] for d in recAlbum_database if d['name'] == clothes]
'''
    #stores all the information into a response object and sends information through axios/AJAX 
#    response_object['location'] = str(weather_title)
#    response_object['info'] = weather_info
#    response_object['pic'] = picture
#    response_object['icon'] = weather_icon
#    response_object['rec'] = recMatch
    return weather_info
def makeGraphData(weather_title):
    response_object = {}
    arr = getLats(weather_title)
    lat = arr[0]
    lng = arr[1]
    # Dark Sky API # 
    '''
    to make graph data work in d3.js, I would need to input a list of coordinates 
    both y-axis and x-axis in order to graph out a line
    I will only being doing line graphs because I have previous exp. with it and it
    shouldn't be too difficult.
    First, get all the data, we will be using 7 api requests for a line graph and we will 
    take each request's data and input it into an array. 
    The loop for api requests I will be using will have to have the import time library
    so we can retrieve the date and get the next seven days by incrementing on the 
    forecast date. Luckily the demo date is December 3rd so I don't have to worry about
    the different months.
    I will make an dictionary where it will have all the data I need in separate arrays.
    Array #1 - Precipitation Data (7 data points)
    Array #2 - Wind Speed Data (7 data points)
    Array #3 - Dew Point Data (7 data points)
    Array #4 - Humidity Data (7 data points)
    '''
    response = requests.get('https://api.darksky.net/forecast/de94c907962cc871c040f2f15a3562e1/' + str(lat) + ',' + str(lng))
    data = response.json()
    arrays = data['daily']['data']
    precipData = []
    windSpeedData = [] 
    humidityData = []
    tempData = {'maxTemp': [], 'minTemp' : []}
    for i in arrays:
        precipData.append(i['precipProbability'])
        windSpeedData.append(i['windSpeed'])
        humidityData.append(i['humidity'])
        tempData['maxTemp'].append(i['temperatureHigh'])
        tempData['minTemp'].append(i['temperatureLow'])
    response_object['precip'] = precipData
    response_object['wind'] = windSpeedData
    response_object['hum'] = humidityData
    response_object['minMax'] = tempData
    return response_object
    