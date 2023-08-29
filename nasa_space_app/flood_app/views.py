from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import random
from io import BytesIO
import base64
from geopy.geocoders import Nominatim
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def home(request):
    return render(request,'index2.html')

def get_level(parameter, low, mid, high):
    if parameter <= low:
        return 1
    elif low < parameter <= mid:
        return 2
    elif mid < parameter <= high:
        return 3
    else:
        return 4

def get_lat_long(place_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(place_name)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None
def calculate_flood_risk(temperature, rainfall, pressure, humidity, winds, sea):
    # Assign weights for different parameters
    sea_weight = 0.3
    rainfall_weight = 0.3
    pressure_weight = 0.1
    humidity_weight = 0.1
    winds_weight = 0.2

    rain_score = get_level(rainfall, 20, 50, 100)
    pressure_score = get_level(pressure, 1000, 1500, 2000)
    humidity_score = get_level(humidity, 30, 60, 90)
    wind_score = get_level(winds, 3, 8, 10)
    sea_score = get_level(sea, 0.5, 1, 2.0)

    aggregated_risk_score = (
        rain_score * rainfall_weight
        + pressure_score * pressure_weight
        + humidity_score * humidity_weight
        + wind_score * winds_weight
        + sea_score * sea_weight
    )

    return aggregated_risk_score

def get_weather_data(latitude, longitude, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

def index(request):
    if request.method == 'POST':
        location = request.POST['location']
        latitude, longitude = get_lat_long(location)
        api_key = 'e2fa4d903b9c0fbf63476b698429f66b'
        
        if latitude is not None and longitude is not None:
            weather_data = get_weather_data(latitude, longitude, api_key)

            timestamps = []
            risk_levels = []

            for entry in weather_data["list"]:
                timestamp = entry["dt"]
                dt = datetime.utcfromtimestamp(timestamp)
                if dt > datetime.utcnow():
                    timestamps.append(dt)
                    temperature = entry["main"]["temp"]
                    rainfall = random.uniform(0, 100)
                    # Fetch actual pressure, humidity, winds, sea data from weather_data here
                    pressure = entry["main"]["pressure"]
                    humidity = entry["main"]["humidity"]
                    winds = entry["wind"]["speed"]
                    sea = 1.4  # Example sea level

                    risk_level = calculate_flood_risk(temperature, rainfall, pressure, humidity, winds, sea)
                    risk_levels.append(risk_level)

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(timestamps, risk_levels, marker='o')
            ax.set_xlabel('Date/Time')
            ax.set_ylabel('Flood Risk Level')
            ax.set_title('Flood Risk Levels Over Time')
            ax.grid(True)
            plt.xticks(rotation=45)

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close(fig)

            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            print(image_base64)
            return render(request, 'display.html', {'location': location,'image_base64': image_base64})

    return render(request, 'index.html')

