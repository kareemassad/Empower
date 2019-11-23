

from flask import Flask, render_template, request, redirect, url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from googlemaps import convert
import googlemaps


app = Flask(__name__, template_folder="templates")
# you can also pass key here
key = "AIzaSyDzLfe1r1aV48C15pGg_-PI0m0upPwFi3U"
GoogleMaps(
    app,
    key=key
)

address = '373 Brettonwood Ridge'


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
    if not response:
        print("INVALID ADDRESS")
        return redirect(url_for('index'))
    else:
        response = geocode(address=address, region='Canada')[0]
    resp_len = len(response['address_components'])
    if resp_len == 1:
        index_shift = 0
    elif resp_len == 2:
        index_shift = 1
    else:
        index_shift = 2
    location = response['address_components'][index_shift]['long_name']
    lat = (response['geometry']['location']['lat'])
    lng = (response['geometry']['location']['lng'])
    circlemap = Map(
        identifier="circlemap",
        varname="circlemap",
        lat=lat,
        lng=lng,
        markers=[
            {
                'icon': '//maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': lat,
                'lng': lng,
                'infobox': "Hello I am a Protest, Come Protest!"
            }

        ],
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
    



@app.route('/new_protest', methods=['POST'])
def new_protest():
    global address
    address = request.form['address']
    return redirect(url_for('map_view'))

@app.route('/<path:path>')
def notFound(path):
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
