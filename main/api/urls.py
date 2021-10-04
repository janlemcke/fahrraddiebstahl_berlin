# -*- coding: utf-8 -*-
from django.urls import path

from main.api.views import (
    get_FahrradtypByDateTimeForPie,
    get_FahrradtypByDateTimeForBar,
    get_SchadenByDateForLine,
    get_SchadenByTimeForLine,
    get_DelictByDateTimeForBar,
    get_ReasonByDateTimeForBar,
    get_TriesByDateTimeForBar,
    get_geojson
)

app_name = 'main'

urlpatterns = [
    path('fahrradByDateTimeForPie', get_FahrradtypByDateTimeForPie),
    path('fahrradByDateTimeForBar', get_FahrradtypByDateTimeForBar),
    path('DmgByDateForLine', get_SchadenByDateForLine),
    path('DmgByTimeForLine', get_SchadenByTimeForLine),
    path('DelictByDateTimeForPie', get_DelictByDateTimeForBar),
    path('ReasonByDateTimeForPie', get_ReasonByDateTimeForBar),
    path('TriesByDateTimeForPie', get_TriesByDateTimeForBar),
    path('geojson', get_geojson),
]