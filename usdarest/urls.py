from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse


def home_response():
    return HttpResponse("""
    Server is up.  Available url trees are:
    /foods/<food_id>/seqs/<seq_id>/nutrients/<nutr_id>
    /nutrients/<nutrient id>""")

urlpatterns = [
    url(r'^$', home_response()),
    url(r'^', include('restful.urls')),
]
