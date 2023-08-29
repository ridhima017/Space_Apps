import json
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from .models import MapPoint
from geopy.geocoders import Nominatim
def home(request):
    return render(request,'index.html')

def monitor_map(request):
    points = MapPoint.objects.all()
    points_data = [
        {'latitude': point.latitude, 'longitude': point.longitude, 'name': point.name}
        for point in points
    ]
    points_data_json = json.dumps(points_data)
    return render(request,'monitor_map.html', {'points_data_json': points_data_json})

