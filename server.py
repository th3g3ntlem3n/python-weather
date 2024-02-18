from flask import Flask, render_template, request
from waitress import serve
from weather import get_current_weather

app = Flask(__name__)  # this makes our app a flask app


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/weather")
def get_weather():
    city = request.args.get("city")
    # check for empty string
    if not bool(city.strip()):
        city = "Paris"  # default value
    weather_data = get_current_weather(city)
    # if city is not found by the API
    if not weather_data["cod"] == 200:
        return render_template("city-not.html")

    return render_template(
        "weather.html",
        titel=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
