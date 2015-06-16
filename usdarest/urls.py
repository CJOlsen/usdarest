from django.conf.urls import include, url
from restful.views import home_response


urlpatterns = [
    url(r'^$', home_response),
    url(r'^', include('restful.urls')),
]
