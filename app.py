from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Put your API key here (temporary, for learning only)
API_KEY = "0229a739e77c12bb18ee9fc28aa458c2"

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": API_KEY, "units": "metric"}

            try:
                resp = requests.get(url, params=params, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    weather = {
                        "city": data.get("name", city),
                        "temperature": round(data["main"]["temp"], 1),
                        "description": data["weather"][0]["description"].title(),
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data.get("wind", {}).get("speed")
                    }
                else:
                    message = resp.json().get("message", "Unknown error")
                    error = f"API error: {message}"
            except requests.RequestException as e:
                error = f"Network error: {e}"

    return render_template("home.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
