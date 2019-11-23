

from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

app = Flask(__name__, template_folder="templates")

# you can also pass key here
GoogleMaps(
    app,
    key=" AIzaSyDzLfe1r1aV48C15pGg_-PI0m0upPwFi3U"
)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/newProtest")
def newProtest():
    return render_template('newProtest.html')


@app.route("/nearMe")
def mapview():
    lat = 40.7128
    long = 74.0060

    circlemap = Map(
        identifier="circlemap",
        varname="circlemap",
        lat=lat,
        lng=-long,
        markers=[
            {
                'icon': '//maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': lat,
                'lng': -long,
                'infobox': "Hello I am <b style='color:green;'>GREEN</b>!"
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
        location='New York City'
    )
    
@app.route('/<path:path>')
def notFound(path):
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
