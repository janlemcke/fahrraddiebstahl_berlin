import datetime
import json

from django.shortcuts import render
from django.views.generic import ListView
from pyproj import Transformer
from . import models

def convertJSON():
    with open('./data/lor_plr.geojson') as json_file:
        geojson = json.load(json_file)
        for feature in geojson["features"]:
            for i in range(0,len(feature["geometry"]["coordinates"])):
                transformer = Transformer.from_crs("EPSG:25833", "EPSG:4326")
                convertedCoordinates = list(map(lambda x: transformer.transform(x[0],x[1]), feature["geometry"]["coordinates"][i]))
                feature["geometry"]["coordinates"][i] = list(map(lambda  x: [round(x[1],4), round(x[0],4)], convertedCoordinates))
        with open('./data/lor_plr_min.geojson', 'w') as outfile:
            json.dump(geojson, outfile)

def main_view(request):
    context = {}
    #get_data(schedule=10, repeat=86400)
    #convertJSON()
    context["data_unavailable"] = models.Report.objects.filter(createdDay__gte=datetime.date.today()- datetime.timedelta(days=1)).count()
    return render(request, "main.html", context)

def FahrradtypByDateTime(request):
    return render(request, "ByDateTime/FahrradtypByDateTime.html", {})

def DmgByDateTime(request):
    return render(request, "ByDateTime/SchadenByDateTime.html", {})

def DelictByDateTime(request):
    return render(request, "ByDateTime/DelictByDateTime.html", {})

def ReasonByDateTime(request):
    return render(request, "ByDateTime/ReasonByDateTime.html", {})

def TriesByDateTime(request):
    return render(request, "ByDateTime/VersucheByDateTime.html", {})

def datenschutz(request):
    return render(request, "datenschutz.html", {})

def impressum(request):
    return render(request, "impressum.html", {})

class datenListView(ListView):
    model = models.Report
    ordering = ["createdDay"]
    paginate_by = 20
    template_name = "daten.html"
    queryset = models.Report.objects.filter(createdDay__gte=datetime.date.today()- datetime.timedelta(days=1))