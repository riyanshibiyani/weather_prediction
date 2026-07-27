from flask import Flask, render_template, request
import requests


app = Flask(__name__)

# Replace with your OpenWeatherMap API Key
API_KEY = "5d28eb458ce001c2314db81bb68980e3"


def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    print(data)

    if response.status_code == 200:
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind": data["wind"]["speed"],
            "condition": data["weather"][0]["main"]
        }
        return weather
    else:
        return None


def predict_weather(weather):
    """
    Rule-based weather prediction based on current conditions.
    Uses temperature, humidity, pressure, wind speed, and condition
    to predict what the weather is likely to be like in the next few hours.
    """
    if weather is None:
        return None

    temp      = weather["temperature"]
    humidity  = weather["humidity"]
    pressure  = weather["pressure"]
    wind      = weather["wind"]
    condition = weather["condition"].lower()

    # ── Storm / Thunderstorm ──────────────────────────────────────────────────
    if condition in ["thunderstorm"] or (humidity > 85 and pressure < 1000 and wind > 10):
        return {
            "label":  "⛈ Thunderstorm Expected",
            "icon":   "⛈",
            "detail": "Heavy rain with thunder and strong winds expected. Stay indoors and avoid travel.",
            "level":  "danger"
        }

    # ── Heavy Rain ────────────────────────────────────────────────────────────
    if condition in ["rain", "drizzle"] or (humidity > 80 and pressure < 1008):
        return {
            "label":  "🌧 Rain Expected",
            "icon":   "🌧",
            "detail": "Rainfall is likely in the next few hours. Carry an umbrella and wear waterproof clothing.",
            "level":  "warning"
        }

    # ── Foggy / Misty ─────────────────────────────────────────────────────────
    if condition in ["fog", "mist", "haze"] or (humidity > 90 and wind < 3):
        return {
            "label":  "🌫 Fog / Low Visibility",
            "icon":   "🌫",
            "detail": "Expect poor visibility due to fog or mist. Drive carefully and use low-beam headlights.",
            "level":  "warning"
        }

    # ── Extreme Heat ──────────────────────────────────────────────────────────
    if temp > 38 and humidity < 40:
        return {
            "label":  "🥵 Extreme Heat Warning",
            "icon":   "🥵",
            "detail": "Dangerously high temperatures. Stay hydrated, avoid direct sun, and limit outdoor activity.",
            "level":  "danger"
        }

    # ── Hot & Humid ───────────────────────────────────────────────────────────
    if temp > 32 and humidity > 70:
        return {
            "label":  "🌡 Hot & Humid Conditions",
            "icon":   "🌡",
            "detail": "Feels hotter than actual temperature due to high humidity. Keep hydrated and stay cool.",
            "level":  "caution"
        }

    # ── Windy ─────────────────────────────────────────────────────────────────
    if wind > 15:
        return {
            "label":  "💨 Strong Winds",
            "icon":   "💨",
            "detail": "Strong winds expected. Secure loose objects outdoors and be cautious while driving.",
            "level":  "caution"
        }

    # ── Partly Cloudy ─────────────────────────────────────────────────────────
    if condition in ["clouds"] or (humidity > 60 and pressure < 1015):
        return {
            "label":  "⛅ Partly Cloudy",
            "icon":   "⛅",
            "detail": "Cloudy skies with mild conditions. Weather may change — keep an eye on updates.",
            "level":  "ok"
        }

    # ── Cold ──────────────────────────────────────────────────────────────────
    if temp < 5:
        return {
            "label":  "🥶 Cold Weather",
            "icon":   "🥶",
            "detail": "Very cold temperatures ahead. Wear warm layers and watch out for frost or ice on roads.",
            "level":  "caution"
        }

    # ── Clear & Sunny (default good weather) ─────────────────────────────────
    return {
        "label":  "☀ Clear & Pleasant",
        "icon":   "☀",
        "detail": "Great weather conditions! Enjoy outdoor activities — comfortable temperature and clear skies.",
        "level":  "good"
    }


@app.route("/", methods=["GET", "POST"])
def home():

    weather1    = None
    weather2    = None
    prediction1 = None
    prediction2 = None
    error       = None

    if request.method == "POST":

        city1 = request.form["city1"].strip()
        city2 = request.form["city2"].strip()

        if city1:
            weather1    = get_weather(city1)
            prediction1 = predict_weather(weather1)

        if city2:
            weather2    = get_weather(city2)
            prediction2 = predict_weather(weather2)

        if city1 and weather1 is None:
            error = "First city is invalid."

        elif city2 and weather2 is None:
            error = "Second city is invalid."

        elif not city1 and not city2:
            error = "Please enter at least one city."

    return render_template(
        "index.html",
        weather1=weather1,
        weather2=weather2,
        prediction1=prediction1,
        prediction2=prediction2,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)