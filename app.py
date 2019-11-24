from flask import Flask, render_template, request, redirect, url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from googlemaps import convert
import pymongo
import googlemaps

client = pymongo.MongoClient(
    "mongodb+srv://gabrielelkadki:Pn1plAR6hhGyOoL1@revolution-uimiu.azure.mongodb.net/test?retryWrites=true&w=majority"
)

db = client.test
collection = db.coordinates


app = Flask(__name__, template_folder="templates")
# you can also pass key here
key = "AIzaSyDzLfe1r1aV48C15pGg_-PI0m0upPwFi3U"
GoogleMaps(
    app,
    key=key
)

address = 'Moscow'


def geocode(address=None, components=None, bounds=None, region=None,
            language=None):
    """
    Geocoding is the process of converting addresses
    (like ``"1600 Amphitheatre Parkway, Mountain View, CA"``) into geographic
    coordinates (like latitude 37.423021 and longitude -122.083739), which you
    can use to place markers or position the map.
    :param address: The address to geocode.
    :type address: string
    :param components: A component filter for which you wish to obtain a
        geocode, for example: ``{'administrative_area': 'TX','country': 'US'}``
    :type components: dict
    :param bounds: The bounding box of the viewport within which to bias geocode
        results more prominently.
    :type bounds: string or dict with northeast and southwest keys.
    :param region: The region code, specified as a ccTLD ("top-level domain")
        two-character value.
    :type region: string
    :param language: The language in which to return results.
    :type language: string
    :rtype: list of geocoding results.
    """

    client = googlemaps.Client(key)

    params = {}

    if address:
        params["address"] = address

    if components:
        params["components"] = convert.components(components)

    if bounds:
        params["bounds"] = convert.bounds(bounds)

    if region:
        params["region"] = region

    if language:
        params["language"] = language

    return client._request("/maps/api/geocode/json", params).get("results", [])


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/newProtest")
def newProtest():
    return render_template('newProtest.html')


@app.route("/nearMe")
def map_view():
    response = geocode(address=address, region='Canada')
    print(response)
    if not response:
        print("INVALID ADDRESS")
        return redirect(url_for('index'))
    else:
        response = response[0]
    resp_len = len(response['address_components'])
    location = response['address_components'][int(resp_len/2 - 2)]['long_name']
    search_lat = (response['geometry']['location']['lat'])
    search_lng = (response['geometry']['location']['lng'])

    markers = [{
        'icon': '//maps.google.com/mapfiles/ms/icons/red-dot.png',
        'lat': search_lat,
        'lng': search_lng
    }]

    my_cursor = collection.find()
    for item in my_cursor:
        markers.append({
            "icon": '//maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': item['lat'],
            'lng': item['lng'],
            'infobox': item['bio']
        })
        print(item)

    circlemap = Map(
        identifier="circlemap",
        varname="circlemap",
        lat=search_lat,
        lng=search_lng,
        markers=markers,
        style=(
            "height:500px;"
            "width:80%;"
                ),
    )

    return render_template(
        'nearMe.html',
        circlemap=circlemap,
        GOOGLEMAPS_KEY=request.args.get('apikey'),
        location=location
    )


@app.route('/newProtest', methods=['POST'])
def new_protest():
    global address
    location = request.form['location']
    response = geocode(address=location)
    latitude = response['geometry']['location']['lat']
    longitude = response['geometry']['location']['lng']
    collection.insert_one({
        "_id": 1,
        "name": request.form['title'],
        "lat": latitude,
        "lng": longitude,
        "confirm_count": -2,
        "Bio": "Kareem rights are important! They're people too.",
    })
    return redirect(url_for('map_view'))


@app.route('/<path:path>')
def notFound(path):
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
