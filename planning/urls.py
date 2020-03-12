
from django.urls import path
from planning.views import trip,homepage,distance,travellingSalesmanProblem,next_permutation,deletefunction
from . import views
from django.conf.urls import url
urlpatterns = [
 path('', views.index, name='index'),
 url(r'^trip/$', trip),
 url(r'^home/$', homepage),
 url(r'^trip/planning/deletefunction/$',deletefunction)
 #url(r'^show/$',show),
]
