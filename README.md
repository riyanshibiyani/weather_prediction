# WeatherIQ

WeatherIQ is a Flask web app that displays current weather for up to two cities and provides a short-term, rule-based weather outlook. Current conditions are retrieved from the OpenWeatherMap API.

## Features

- Look up current conditions for one or two cities.
- View temperature, humidity, pressure, wind speed, sunrise, and sunset.
- Get a simple outlook based on current weather conditions.

The outlook uses fixed rules; it is not a machine-learning forecast.

## Requirements

- Python 3
- An OpenWeatherMap API key

## Setup

1. Clone or download this project and open a terminal in its folder.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Set your OpenWeatherMap API key for the current PowerShell session:

   ```powershell
   $env:OPENWEATHERMAP_API_KEY = "your_api_key"
   ```

## Run

Start the development server:

```powershell
python app.py
```

Open the local address shown in the terminal (by default, `http://127.0.0.1:5000`), enter one or two city names, and submit the form.

The API key must be set in each new terminal session before starting the app. Do not commit your API key to source control.
