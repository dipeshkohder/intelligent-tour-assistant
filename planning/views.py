from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.utils.dateparse import parse_date
from .models import user_details
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render
from pandas.io.json import json_normalize
import folium
from geopy.geocoders import Nominatim 
import requests
import json
from django.http import HttpResponse
import wikipedia
import requests
from bs4 import BeautifulSoup
try:
	from googlesearch import search
except ImportError:
	print("No module named 'google' found")
import urllib.request , json
from datetime import time
import datetime
from datetime import timedelta
from datetime import date
from sys import maxsize 
from math import radians, cos, sin, asin, sqrt
import ast
import pickle



OptimizedItinerary = []
SuggestionList = []

def index(request):
	return HttpResponse("hello World!! Django is unchained!")

def distance(lat1, lat2, lon1, lon2): 

    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
    
    r = 6371
    return(c * r) 

def travellingSalesmanProblem(main_list, s): 
  
    V = len(main_list)
    lengthofplacelist = len(main_list)

    #retrive the longitude and latitude of the first place

    graph = []

    for i in range(lengthofplacelist):
        graphrow = []
        for j in range(lengthofplacelist):
            graphrow.append(distance(main_list[i].p_lat,main_list[j].p_lat,main_list[i].p_long,main_list[j].p_long))
        graph.append(graphrow)

    print(graph)

    # store all vertex apart from source vertex 
    vertex = [] 
    for i in range(V): 
        if i != s: 
            vertex.append(i) 
  
    # store minimum weight Hamiltonian Cycle 
    min_path = maxsize 
  
    

    while True: 
  
        # store current Path weight(cost) 
        current_pathweight = 0
        Tempitinerary = []

        # compute current path weight 
        k = s 
        for i in range(len(vertex)): 
            current_pathweight += graph[k][vertex[i]] 
            # Tempitinerary.append(names[k])
            Tempitinerary.append(main_list[k])
            k = vertex[i] 
        current_pathweight += graph[k][s] 
        # Tempitinerary.append(names[k])
        Tempitinerary.append(main_list[k])
        
        # print(Tempitinerary," with ",current_pathweight)
        # update minimum 

        if min_path > current_pathweight :
            min_path = current_pathweight
            OptimizedItinerary = Tempitinerary
        #min_path = min(min_path, current_pathweight) 
  
        if not next_permutation(vertex): 
            break
  
    for i in OptimizedItinerary:
        print(i.p_name)

    print( " with total distance ",min_path)
    return OptimizedItinerary,min_path

  
# next_permutation implementation 
def next_permutation(L): 
  
    n = len(L) 
  
    i = n - 2
    while i >= 0 and L[i] >= L[i + 1]: 
        i -= 1
  
    if i == -1: 
        return False
  
    j = i + 1
    while j < n and L[j] > L[i]: 
        j += 1
    j -= 1
  
    L[i], L[j] = L[j], L[i] 
  
    left = i + 1
    right = n - 1
  
    while left < right: 
        L[left], L[right] = L[right], L[left] 
        left += 1
        right -= 1
  
    return True



def trip(request):
#code for finding out coordinates of given address
		#c = {}
	    #c.update(csrf(request))
		class Place_Info:
			p_name=''
			p_categoryid=''
			p_lat=0
			p_long=0
			p_categorytype=''
			p_distance=0
			p_address=''
			p_summary=''
			p_imageURL=''
			p_ratings=''

			def Place_Info_print(self):
				return "Place Name : ",self.p_name," Category Type : ",self.p_categorytype," Place Ratings : ",self.p_ratings," Place s : ",self.p_name

		main_list = []
		global SuggestionList
		suggestionListSize = 0
		print("Enter City Name : ",end = '')
		location_name = request.POST.get('place','')
		start = request.POST.get('startdate','')
		#fstart = datetime.datetime.strptime(start, "%Y-%m-%d").date()
		format_str = '%m/%d/%Y'
		trip_start = datetime.datetime.strptime(start,format_str).date()
		#print(datetime_obj.date())	
		
		end = request.POST.get('enddate','')
		trip_end = datetime.datetime.strptime(end,format_str).date()
		#print(datetime_obj.date())
		
		nom = Nominatim(user_agent="my-application")
		coordinates = nom.geocode(location_name)
		if coordinates == None :
			print('Not found')
		else:  
			print(coordinates.address)
			longitude = str(coordinates.longitude)
			latitude = str(coordinates.latitude)
			location_coordinates =  latitude + ',' + longitude 
			print(location_coordinates)

		
		start_time = datetime.datetime(2020,1,26,9,00,00) #trip start date
		#trip_start = datetime.datetime(2020,1,26) 
		#trip_end = datetime.datetime(2020,1,30) # pela -> yy |  then ->  mm  | then -> dd
		
		pack_night = (trip_end - trip_start).days
		pack_days = ((trip_end - trip_start) + timedelta(0,86400)).days # 1 divas add karo expicitly
		
		travel_time = 30*60 #assuming for now, 30 minutes to reach from one place to another
		end_time=start_time
		rest_time = datetime.datetime(100,1,1,21,00,00)
		
		#setup for the foursquare API
		client_id = 'M2QVKFEINCIFSIVH1OCONVATMWRPQNWTAPX5Q42VN3BDRMB5'
		client_secret = 'LUU5AZWGRJIMVDTVSP3UQBN50TC0YHS5XZ44NHSXXM5KWRRQ'
		version = '20120610'
		limit = 100

		print('Enter radius : ',end = '')
		location_radius = int(request.POST.get('radius',''))
		category='4bf58dd8d48988d181941735'
		url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}&sortByDistance={}&categoryId={}'.format(
			client_id, 
			client_secret, 
			version, 
			latitude, 
			longitude,
			location_radius, 
			limit,1,
			category
			)
		print(url)
		results = requests.get(url).json()
		d = json.dumps(results)
		e = json.loads(d) 
		
		alist=[]
		curr_day = 1
		links= []
		start =[]
		end =[]
		rating=[]
		for place in results['response']['groups'][0]['items']:
			try:
			
				
				if curr_day <= pack_days:
					
					mainobject = Place_Info()
					
					print("=====  DAY ",curr_day," of ",pack_days,"=======")
					start_time = end_time
					end_time = start_time + datetime.timedelta(0,7200) 
					start.append(start_time.time())
					end.append(end_time.time())
					print("Duration : ",start_time.time()," - ",end_time.time())
					
					print("Place id : ",place['venue']['id'])
					print("Place name : ",place['venue']['name'])
					print("Place distance : ",place['venue']['location']['distance'])
					print("Place address : ",place['venue']['location']['formattedAddress'][0])
					print("Place category type : ",place['venue']['categories'][0]['name'])
				
				
					mainobject.p_categoryid = place['venue']['id']
					mainobject.p_name = place['venue']['name']
					mainobject.p_address = place['venue']['location']['formattedAddress'][0]
					mainobject.p_categorytype = place['venue']['categories'][0]['name']
					mainobject.p_distance = place['venue']['location']['distance']
					mainobject.p_lat=place['venue']['location']['lat']
					mainobject.p_long = place['venue']['location']['lng']
            				
					
					
				
					URL = "https://www.google.com/search?q={}".format(
						place['venue']['name']
					)
					print(URL)
					cont = requests.get(URL).content 
					soup = BeautifulSoup(cont, 'html.parser')
					result=soup.find_all("span",attrs={"class":"oqSTJd"})
					print("Rating of ", place['venue']['name'] , " is ",result[0].text)
					mainobject.p_ratings = result[0].text    

					if( (end_time + datetime.timedelta(0,travel_time)).time() >= rest_time.time() ):
						print("TIME TO REST FOR TODAY :) See ya tomorrow morning at 9 AM. Till then Good Night!")
						print("*********** DAY ",curr_day," ENDS *****************")
						curr_day = curr_day + 1
						start_time = datetime.datetime(2020,1,26,9,00,00)
						end_time = start_time
					else:
						end_time = end_time + datetime.timedelta(0,travel_time)
					
					
					'''urldetails = 'https://api.foursquare.com/v2/venues/'+place['venue']['id']+'?client_id={}&client_secret={}&v={}'.format(
					client_id, 
					client_secret, 
					version
					
					)

					#print("URL GOT: ",urldetails)

					
					dets = requests.get(urldetails).json()
					'''#temp_a = json.dumps(dets)
					#temp_b = json.loads(temp_a) 
					#links.append(temp_b)
					# print("PLACE DETAILS : ",dets['response'])
					#for test in dets['response']['venue']:
					#	print(test)
					print('*******************************')
					#print(dets['response'])
					#alist.append(dets)
					#for test in dets['response']['venue']['tips']['groups'][0]['items']:
					#	print(test['text'])
					#	mainobject.p_summary = test['text']
					#print("============================================================================================================")
					'''for test in dets['response']['venue']['photos']['groups'][0]['items']:
						links.append(test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix'])
						mainobject.p_imageURL = test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix']
					'''
					#for rating
					'''key = "rating"
					flag = 1
					for obj in dets['response']['venue']:
						if obj == key:
							flag = 0
					if flag == 0:
						print("Place Ratings : ",dets['response']['venue']['rating'])
						rating.append(dets['response']['venue']['rating'])
					if (flag == 1):
						print("*** Ratings Not Found ***") 
						rating.append("No Ratings")
					'''
					#query = place['venue']['name']
					#links=[]
					#for j in search(query, tld="co.in", num=10, stop=1, pause=2):
					#	print(j)
					#	links.append(j)
					#print("---------------------------/////////---------------------")
					#print(wikipedia.summary(place['venue']['name'],sentences=3))
					#alist.append(wikipedia.summary(place['venue']['name'],sentences=3))
					#print("--------------------------//////////-----------------------")
					
					main_list.append(mainobject)
					print("Object mathi",mainobject.p_name)
					SuggestionList.clear()
									
				else:
				
					
					############################CODE FOR SUGGESTION LIST#########################################
					mainobject = Place_Info()
					
					
					print("Place id : ",place['venue']['id'])
					print("Place name : ",place['venue']['name'])
					print("Place distance : ",place['venue']['location']['distance'])
					print("Place address : ",place['venue']['location']['formattedAddress'][0])
					print("Place category type : ",place['venue']['categories'][0]['name'])
				
				
					mainobject.p_categoryid = place['venue']['id']
					mainobject.p_name = place['venue']['name']
					mainobject.p_address = place['venue']['location']['formattedAddress'][0]
					mainobject.p_categorytype = place['venue']['categories'][0]['name']
					mainobject.p_distance = place['venue']['location']['distance']
					mainobject.p_lat=place['venue']['location']['lat']
					mainobject.p_long = place['venue']['location']['lng']
            				
					
					
				
					URL = "https://www.google.com/search?q={}".format(
						place['venue']['name']
					)
					print(URL)
					cont = requests.get(URL).content 
					soup = BeautifulSoup(cont, 'html.parser')
					result=soup.find_all("span",attrs={"class":"oqSTJd"})
					print("Rating of ", place['venue']['name'] , " is ",result[0].text)
					mainobject.p_ratings = result[0].text    

					
					
					'''urldetails = 'https://api.foursquare.com/v2/venues/'+place['venue']['id']+'?client_id={}&client_secret={}&v={}'.format(
					client_id, 
					client_secret, 
					version
					
					)

					#print("URL GOT: ",urldetails)

					
					dets = requests.get(urldetails).json()
					'''#temp_a = json.dumps(dets)
					#temp_b = json.loads(temp_a) 
					#links.append(temp_b)
					# print("PLACE DETAILS : ",dets['response'])
					#for test in dets['response']['venue']:
					#	print(test)
					print('*******************************')
					#print(dets['response'])
					#alist.append(dets)
					#for test in dets['response']['venue']['tips']['groups'][0]['items']:
					#	print(test['text'])
					#	mainobject.p_summary = test['text']
					#print("============================================================================================================")
					'''for test in dets['response']['venue']['photos']['groups'][0]['items']:
						links.append(test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix'])
						mainobject.p_imageURL = test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix']
					'''
					#for rating
					'''key = "rating"
					flag = 1
					for obj in dets['response']['venue']:
						if obj == key:
							flag = 0
					if flag == 0:
						print("Place Ratings : ",dets['response']['venue']['rating'])
						rating.append(dets['response']['venue']['rating'])
					if (flag == 1):
						print("*** Ratings Not Found ***") 
						rating.append("No Ratings")
					'''
					#query = place['venue']['name']
					#links=[]
					#for j in search(query, tld="co.in", num=10, stop=1, pause=2):
					#	print(j)
					#	links.append(j)
					#print("---------------------------/////////---------------------")
					#print(wikipedia.summary(place['venue']['name'],sentences=3))
					#alist.append(wikipedia.summary(place['venue']['name'],sentences=3))
					#print("--------------------------//////////-----------------------")
					
					SuggestionList.append(mainobject)
					
					suggestionListSize = suggestionListSize + 1
					if suggestionListSize == 5:
						break
					print("Object mathi",mainobject.p_name)
					
					
					############################CODE FOR SUGGESTION LIST ENDS ###################################
					
					
			
				print('******************************************************************************************')
					
			except:
				main_list.append(mainobject)
				pass
		
		global OptimizedItinerary
		print("hii1")
		# if __name__ == "__main__": 
  
			
		s = 0
		print("hii2")
		OptimizedItinerary,min_distance = travellingSalesmanProblem(main_list, s)



		print("OptimizedItinerary has distance : ",min_distance)
		for place in OptimizedItinerary:
			print(place.p_name)
		print("--- DELETION ---")
		flag = 0
		while( flag != 999 ):
				
			flag = int(input("Enter index of place to delete : enter 999 to exit "))

			if flag != 999:
				del OptimizedItinerary[flag]
				OptimizedItinerary,min_distance = travellingSalesmanProblem(OptimizedItinerary, s)
			for name in OptimizedItinerary:
				print("After Deleting  : ",name.p_name," Distance : ",min_distance)

			# print('******************************************************************************************')
	
		#print(main_list)
		return render(request,"map_page.html",{'objects': e ,'objs':results['response']['groups'][0]['items'],'city':location_name,'listabc':zip(links,start,end,rating),'start':trip_start,'end':trip_end,'pack_days':pack_days,'pack_night':pack_night,'mainlist':OptimizedItinerary,'suggestionList' : SuggestionList})
		
		
def homepage(request):
	context={'request':request}
	return render(request,'myhome.html')
	
	
def deletefunction(request):
	
	deleteplacelist = request.POST.get('deleteplacelist').split(',')
	addplacelist = request.POST.get('addplacelist').split(',')
		
	deleteplacelist.sort(reverse=True)
	
	
	for deleteplace in deleteplacelist: 
		#print(ord(deleteplace)-ord('0'))
		del OptimizedItinerary[ord(deleteplace)-ord('0')-1]
		
		
	for addplace in addplacelist:
		OptimizedItinerary.append(SuggestionList[ord(addplace)-ord('0')-1])
	

	SuggestionList.clear()
	#print('After Deleting : ')
	#print(OptimizedItinerary)

	return render(request,'CustomizedItinenary.html',{'CustomizedItinenary' : OptimizedItinerary})	

def login(request):
	
	return render(request,'login.html')


def auth_view(request):
	username = request.POST.get('email', '')
	password = request.POST.get('pass', '')
	user = auth.authenticate(username=username,password=password)
	print(username)
	print(password)
	
	print(user)
	if user is not None:
		auth.login(request, user)
		if(user.is_superuser):
			request.session['name']=username
			ab = request.session['name']
			context={'ab' : ab,}
			return HttpResponseRedirect('/planning/home/',context)
	else:
		if user_details.objects.filter(email=username).exists() and user_details.objects.get(email=username).password==password:
			 
			
			request.session['username']=username
			ab = request.session['username']
			
			context={'ab' : ab,}
			context['request']=request
			#print(details)
			print(request.session['username'])
			return HttpResponseRedirect('/planning/home/',context)
		else:
			context={}
			return HttpResponseRedirect('/planning/login/',context)


def signup(request):
	
	return render(request,'signup.html')
	
def adduser_info(request):
	#c = RequestContext(request)
	#c = {}
	#c.update(csrf(request))
	uid = request.POST.get('uname', '')
	
	pas = request.POST.get('password', '')
	
	fnam=request.POST.get('fname','')
	lnam = request.POST.get('lname', '')
	
	emai = request.POST.get('email', '')
	
	mob = request.POST.get('mobile', '')
	
	t = user_details(username = uid, password=pas,first_name=fnam,last_name=lnam,email=emai,mo_no=mob)
	t.save()
	return render(request,"login.html")
