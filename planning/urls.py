
from django.urls import path
from planning.views import login,adduser_info,trip,homepage,distance,travellingSalesmanProblem,next_permutation,deletefunction,auth_view,signup,myaccount
from . import views
from django.conf.urls import url
urlpatterns = [
 path('', views.index, name='index'),
 url(r'^trip/$', trip),
 url(r'^home/$', homepage),
 url(r'^trip/planning/deletefunction/$',deletefunction),
 url(r'^login/$',login),
 url(r'^checklogin/$',auth_view),
 url(r'^signup/$',signup),
 url(r'^adduser/$',adduser_info),
 url(r'^myaccount/$',myaccount),
 #url(r'^show/$',show),
]
