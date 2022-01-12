import json
import math

from django.db.models import Count, Sum
from numpy import arange
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from main.api.serializers import ReportSerializer
from main.models import Report


def get_start_endDate(query_params):
    return query_params["start"].split("T")[0], query_params["end"].split("T")[0]


@api_view(['GET', ])
@permission_classes([])
def get_FahrradtypByDateTimeForPie(request):
    try:
        startDate, endDate = get_start_endDate(request.GET)
        data = Report.objects.filter(createdDay__gte=startDate, createdDay__lt=endDate).values('typeOfBike').annotate(
            count=Count('typeOfBike')).order_by("count")
        return Response(data)
    except:
        return Response()


@api_view(['GET', ])
@permission_classes([])
def get_FahrradtypByDateTimeForBar(request):
    try:
        startDate, endDate = get_start_endDate(request.GET)
        data = Report.objects.filter(createdDay__gte=startDate, createdDay__lt=endDate).values('typeOfBike',
                                                                                               'createdDay').annotate(
            count=Count('typeOfBike')).order_by("typeOfBike")
        return Response(data)
    except:
        return Response()


@api_view(['GET', ])
@permission_classes([])
def get_SchadenByDateForLine(request):
    try:
        startDate, endDate = get_start_endDate(request.GET)
        data = Report.objects.filter(createdDay__gte=startDate, createdDay__lt=endDate).values('createdDay').annotate(
            amount=Sum('damage')).order_by("createdDay")
        return Response(data)
    except:
        return Response()


@api_view(['GET', ])
@permission_classes([])
def get_SchadenByTimeForLine(request):

    startDate, endDate = get_start_endDate(request.GET)
    data = Report.objects.filter(createdDay__gte=startDate, createdDay__lt=endDate).values('beginHour', 'endHour',
                                                                                           'beginDay', 'endDay',
                                                                                           'damage')

    newDataset = [0 for x in range(0, 24)]

    for i in data:
        dayDifference = abs((i["beginDay"] - i["endDay"]).days)
        if dayDifference > 1:
            tmpDays = [0 for x in range(0, dayDifference * 24)]
            amountOfHours = (i['endHour'] - i['beginHour']) % 24
            amountOfHours += (dayDifference - 1) * 24
            if amountOfHours != 0:
                avg = round(i["damage"] / amountOfHours, 2)
            else:
                avg = i["damage"]

            for j in range(i["beginHour"], i["beginHour"] + amountOfHours):
                tmpDays[j % (24 * dayDifference)] += avg

            for k in range(0, len(tmpDays)):
                newDataset[k % 24] += tmpDays[k]
        else:
            j = (i['endHour'] - i['beginHour']) % 24
            if j != 0:
                avg = round(i["damage"] / j, 2)
            else:
                avg = i["damage"]
            for tmp in range(i['beginHour'], i['beginHour'] + j):
                newDataset[tmp % 24] += avg
    newDataset = list(map(lambda x: round(x, 2), newDataset))
    return Response(newDataset)


@api_view(['GET', ])
@permission_classes([])
def get_geojson(request):

    try:
        startDate, endDate = get_start_endDate(request.GET)
        mapType = request.GET["type"]
        data = Report.objects.filter(createdDay__gte=startDate, createdDay__lt=endDate).values('lor').annotate(
            count=Count('createdDay'))

        key = mapType.upper()+"_ID"
        summe = 0
        with open('./data/lor_'+mapType+'_min.geojson') as json_file:
            geojson = json.load(json_file)
            for d in data:
                for feature in geojson["features"]:
                    if d["lor"].startswith(feature["properties"][key]):
                        if "count" not in feature["properties"]:
                            feature["properties"]["count"] = d["count"]
                        else:
                            feature["properties"]["count"] += d["count"]
                        summe += d["count"]
            steps = summe/len(geojson["features"])

            if steps >= 1:
                geojson["proportions"] = [round(x) for x in arange(0, steps*7, steps)]
            else:
                geojson["proportions"] = [round(x * summe) for x in arange(0, 0.15, 0.0225)]
            return Response(geojson)
    except:
        return Response()


@api_view(['GET', ])
@permission_classes([])
def get_DelictByDateTimeForBar(request):
    try:
        startDate, endDate = get_start_endDate(request.GET)
        data = Report.objects.filter(createdDay__gte=startDate, createdDay__lt=endDate).values('delict', 'createdDay').annotate(
                count=Count('delict')).order_by("delict")

        return Response(data)
    except:
        return Response()

@api_view(['GET', ])
@permission_classes([])
def get_ReasonByDateTimeForBar(request):
    try:
        startDate, endDate = get_start_endDate(request.GET)
        data = Report.objects.filter(createdDay__gte=startDate, createdDay__lt=endDate).values('reason', 'createdDay').annotate(
                count=Count('reason')).order_by("reason")

        return Response(data)
    except:
        return Response()

@api_view(['GET', ])
@permission_classes([])
def get_TriesByDateTimeForBar(request):
    try:
        startDate, endDate = get_start_endDate(request.GET)
        data = Report.objects.filter(createdDay__gte=startDate, createdDay__lt=endDate).values('tryBike', 'createdDay').annotate(
                count=Count('tryBike')).order_by("tryBike")

        return Response(data)
    except:
        return Response()