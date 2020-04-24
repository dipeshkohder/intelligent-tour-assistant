
from django.urls import path
from planning.views import tripmap,update,viewitin,logout,savetrip,login,adduser_info,trip,homepage,distance,travellingSalesmanProblem,next_permutation,deletefunction,auth_view,signup,showIndividualmap,myaccount,myplans,about,contact
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
 url(r'^myplans/$',myplans),
 url(r'^showmap/$',showIndividualmap),
 url(r'^about/$',about),
 url(r'^contact/$',contact),
 url(r'^logout/$',logout),
 url(r'^savetrip/$',savetrip),
 url(r'^viewitin/$',viewitin),
 url(r'^update/$',update),
  url(r'^tripmap/$',tripmap),
 #url(r'^show/$',show),
]
