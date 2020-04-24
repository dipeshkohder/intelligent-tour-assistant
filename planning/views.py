from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from .utils import render_to_pdf
from django.template.context_processors import csrf
from django.utils.dateparse import parse_date
from .models import users_details,trip_details,places
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
from datetime import datetime
import datetime
from datetime import timedelta
from datetime import date
from sys import maxsize 
from math import radians, cos, sin, asin, sqrt
import ast
import pickle
import itertools


links = []
start = []
end = []
rating = []
e = []
pack_days = 0
pack_night = 0
trip_start1 = date.today()
trip_end1 = date.today()
location_radius = 0
OptimizedItineraryForMap = []
location_name = ""
OptimizedItinerary = []
pname = []
paddress = []
pdistance = []
pcategory = []
SuggestionList = []
istart = " "
mainobject = None
city = " "
activitypreferences = ""

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
		global location_name
		location_name = request.POST.get('place','')
		global city
		city = location_name
		
		start_itinerary_date = request.POST.get('startdate','')
		global activitypreferences
		activitypreferences = request.POST.get('activitypreferences','')
		
		#fstart = datetime.datetime.strptime(start, "%Y-%m-%d").date()
		format_str = '%m/%d/%Y'
		trip_start = datetime.datetime.strptime(start_itinerary_date,format_str).date()
		#print(datetime_obj.date())	
		
		
		end_itinanery_date = request.POST.get('enddate','')
		trip_end = datetime.datetime.strptime(end_itinanery_date,format_str).date()
		trip_start1 = datetime.datetime.strptime(start_itinerary_date,format_str).strftime('%Y-%m-%d')
		trip_end1 = datetime.datetime.strptime(end_itinanery_date,format_str).strftime('%Y-%m-%d')
		
		print(start_itinerary_date,end_itinanery_date)
		print(trip_start1,trip_end1)
		#request.session['start'] = trip_start
		#request.session['end'] = trip_end
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
		
		global pack_night
		pack_night = (trip_end - trip_start).days
		global pack_days
		pack_days = ((trip_end - trip_start) + timedelta(0,86400)).days # 1 divas add karo expicitly
		print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',type(pack_days))
		
		travel_time = 30*60 #assuming for now, 30 minutes to reach from one place to another
		end_time=start_time
		rest_time = datetime.datetime(100,1,1,21,00,00)
		
		#setup for the foursquare API
		client_id = '0XERSK2YASEXLFMV0JH4WP3NSHBKQNQJMNGRGQF1U03VXBI2'
		client_secret = 'T5YIUEZC3MXSBTSANEVPPT3BD1VUBK3ENCAEJDWBFM11WEJ2'
		version = '20120610'
		limit = 100

		category='4bf58dd8d48988d181941735'
		
		print('Enter radius : ',end = '')
		# location_radius = int(request.POST.get('radius',''))
		global location_radius
		location_radius = 150000
		if activitypreferences == "monument" :
			category='4bf58dd8d48988d12d941735'
		elif activitypreferences == "culture":
			category = '52e81612bcbc57f1066b7a32'
		elif activitypreferences == "adventure":
			category = '4eb1d4d54b900d56c88a45fc'
		elif activitypreferences == "spritual":
			category = '4bf58dd8d48988d131941735'
		elif activitypreferences == "professional":
			category = '4d4b7105d754a06375d81259'
		elif activitypreferences == "mountain":
			category = '4eb1d4d54b900d56c88a45fc'
		elif activitypreferences == "beach":
			category = '4bf58dd8d48988d1e2941735'
		elif activitypreferences == "museum":
			category = '4bf58dd8d48988d181941735'

			
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
		global e
		e = json.loads(d) 
		
		
		curr_day = 1
		global links
		global start
		global end
		global rating
		global pname
		global paddress
		global pcategory
		global pdistance
		for place in results['response']['groups'][0]['items']:
			try:
			
				
				if curr_day <= pack_days:
					
					global mainobject
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
            				
					pname.append(mainobject.p_name)
					paddress.append(mainobject.p_address)
					pcategory.append(mainobject.p_categorytype)
					pdistance.append(mainobject.p_distance)
					
				
					URL = "https://www.google.com/search?q={}".format(
						place['venue']['name']
					)
					print(URL)
					# cont = requests.get(URL).content 
					# soup = BeautifulSoup(cont, 'html.parser')
					# result=soup.find_all("span",attrs={"class":"oqSTJd"})
					# print("Rating of ", place['venue']['name'] , " is ",result[0].text)
					# mainobject.p_ratings = result[0].text    

					if( (end_time + datetime.timedelta(0,travel_time)).time() >= rest_time.time() ):
						print("TIME TO REST FOR TODAY :) See ya tomorrow morning at 9 AM. Till then Good Night!")
						print("*********** DAY ",curr_day," ENDS *****************")
						curr_day = curr_day + 1
						print("Current day : ",curr_day)
						start_time = datetime.datetime(2020,1,26,9,00,00)
						end_time = start_time
					else:
						end_time = end_time + datetime.timedelta(0,travel_time)
					
					
					urldetails = 'https://api.foursquare.com/v2/venues/'+place['venue']['id']+'?client_id={}&client_secret={}&v={}'.format(
					client_id, 
					client_secret, 
					version
					
					)
					#print("URL GOT: ",urldetails)

					dets = requests.get(urldetails).json()
	
	
					#temp_a = json.dumps(dets)
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
					for test in dets['response']['venue']['photos']['groups'][0]['items']:
						links.append(test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix'])
						mainobject.p_imageURL = test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix']		
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
					# cont = requests.get(URL).content 
					# soup = BeautifulSoup(cont, 'html.parser')
					# result=soup.find_all("span",attrs={"class":"oqSTJd"})
					# print("Rating of ", place['venue']['name'] , " is ",result[0].text)
					# mainobject.p_ratings = result[0].text    

					
					
					urldetails = 'https://api.foursquare.com/v2/venues/'+place['venue']['id']+'?client_id={}&client_secret={}&v={}'.format(
					client_id, 
					client_secret, 
					version
					
					)

					#print("URL GOT: ",urldetails)

					
					dets = requests.get(urldetails).json()
					
					
					#temp_a = json.dumps(dets)
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
					for test in dets['response']['venue']['photos']['groups'][0]['items']:
						links.append(test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix'])
						mainobject.p_imageURL = test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix']
					
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
				#main_list.append(mainobject)
				pass
		
		global OptimizedItinerary
		print("hii1")
		# if __name__ == "__main__": 
  
			
		s = 0
		print("hii2")
		#OptimizedItinerary,min_distance = travellingSalesmanProblem(main_list, s)



		# print("OptimizedItinerary has distance : ",min_distance)
		# for place in OptimizedItinerary:
			# print(place.p_name)
		# print("--- DELETION ---")
		# flag = 0
		# while( flag != 999 ):
				
			# flag = int(input("Enter index of place to delete : enter 999 to exit "))

			# if flag != 999:
				# del OptimizedItinerary[flag]
				# OptimizedItinerary,min_distance = travellingSalesmanProblem(OptimizedItinerary, s)
			# for name in OptimizedItinerary:
				# print("After Deleting  : ",name.p_name," Distance : ",min_distance)

			# print('******************************************************************************************')
	
		#print(main_list)
		
		
		
		#####################################CODE FOR MAKING OptimizedItinerary FOR DIFFERENT DAYS#############################################
			
			
		
		split_list = []
			
		split_index = 0
		for i in range(pack_days):
			split_list.append(split_index + 5)
			split_index = split_index + 5
			
			
		splited_optimizedItinenary = [main_list[i : j] for i, j in zip([0] + split_list, split_list + [None])] 
		
		#print(str(splited_optimizedItinenary))
		
		
		OptimizedItineraryWithSplited = []
		for RandomItinenary in splited_optimizedItinenary:
			if len(RandomItinenary) >= 3:
				Itinenary,min_distance = travellingSalesmanProblem(RandomItinenary,0)
				OptimizedItineraryWithSplited.append(Itinenary)

		OptimizedItinerary = list(itertools.chain.from_iterable(OptimizedItineraryWithSplited))
		
		#OptimizedItinerary = OptimizedItinerary1
		#######################################################################################################################################
		
		global istart
		istart = request.POST.get('startdate','')
		
		print(type(istart))
		return render(request,"map_page.html",{'radius':location_radius,'pname':pname,'paddress':paddress,'pdistance':pdistance,'pcategory':pcategory,'objects': e ,'city':location_name,'listabc':zip(links,start,end,rating),'istart':istart,'start':trip_start1,'end':trip_end1,'pack_days':pack_days,'pack_night':pack_night,'mainlist':OptimizedItinerary,'suggestionList' : SuggestionList,'category':activitypreferences})
		
		
def homepage(request):
	context={'request':request}
	return render(request,'myhome.html')
	
	
def deletefunction(request):

	
	deleteplacelist = request.POST.get('deleteplacelist').split(',')
	addplacelist = request.POST.get('addplacelist').split(',')

	deleteplacelistint = [int(i) for i in deleteplacelist]
	addplacelistint = [int(i) for i in addplacelist]

		
	deleteplacelistint.sort(reverse=True)
	
	if len(deleteplacelistint) != 0:
		for deleteplace in deleteplacelistint: 
			del OptimizedItinerary[deleteplace-1]
		
	if len(addplacelistint) != 0:	
		for addplace in addplacelistint:
			OptimizedItinerary.append(SuggestionList[addplace-1])
	

	SuggestionList.clear()
	#print('After Deleting : ')
	#print(OptimizedItinerary)

	#return render(request,'CustomizedItinenary.html',{'CustomizedItinenary' : OptimizedItinerary})	
	return render(request,"map_page.html",{'radius':location_radius,'pname':pname,'paddress':paddress,'pdistance':pdistance,'pcategory':pcategory,'objects': e ,'city':location_name,'listabc':zip(links,start,end,rating),'istart':istart,'start':trip_start1,'end':trip_end1,'pack_days':pack_days,'pack_night':pack_night,'mainlist':OptimizedItinerary,'suggestionList' : SuggestionList,'category':activitypreferences})


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
		if users_details.objects.filter(email=username).exists() and users_details.objects.get(email=username).password==password:
			 
			uname =users_details.objects.get(email=username).username
			request.session['username']= uname
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
	
	pas = request.POST.get('pass', '')
	
	fnam=request.POST.get('fname','')
	lnam = request.POST.get('lname', '')
	
	emai = request.POST.get('email', '')
	
	mob = request.POST.get('mobile', '')
	
	t = users_details(username = uid, password=pas,first_name=fnam,last_name=lnam,email=emai,mo_no=mob)
	t.save()
	return render(request,"login.html")



def myplans(request):
	try:
		if request.session['username']:
			uname=request.session['username']
			data = trip_details.objects.filter(username=uname).values()
			#for ob in data.values():
			#days = trip_details.objects.all(username=uname).pack_days
			#city = trip_details.objects.all(username=uname).city
			print(data.values())
			print(len(data))
			
			pasttrips = []
			upcoming = []
			current =  [] 
			
			

			today = date.today()

				
			d2 = today.strftime("%Y-%m-%d")
			
			d1 = datetime.datetime.strptime(d2,'%Y-%m-%d').date()
			
			for obj in data.values():
				start_date = obj['start_date']
				end_date = obj['end_date']
				#start_date = datetime.datetime.strptime(start,'%Y-%m-%d').date()
				#end_date = datetime.datetime.strptime(end,'%Y-%m-%d').date()
				if end_date < d1:
					pasttrips.append(obj)
				elif start_date <= d1 and d1 <= end_date:
					current.append(obj)
				else:
					upcoming.append(obj)
				
				

			return render(request,'myplans.html',{'strip':data,'upcoming':upcoming,'current' :current,'pasttrips':pasttrips})
			#,'city':city,'days': days
			
	except(AttributeError,KeyError):
		context={}
		return HttpResponseRedirect('/planning/login/',context)
	
def showIndividualmap(request):
	category = request.POST.get('category','')
	city = request.POST.get('city','')
	startmap = request.POST.get('start','')
	endmap = request.POST.get('end','')
	radius = request.POST.get('radius','')
	pack_days_string = []
	for i in range(0,pack_days):
		pack_days_string.append(0)
	 	
	focuslnt = OptimizedItinerary[0].p_lat
	focuslng = OptimizedItinerary[0].p_long
		
	return render(request,'showmap.html',{'istart' : istart,'pack_days_string':pack_days_string,'pack_days':pack_days,'OptimizedItinerary' : OptimizedItinerary,'focuslng':focuslng,'focuslnt':focuslnt,'city':city,'start':startmap,'end':endmap,'category':category,'radius':radius})


def about(request):

	return render(request,'about.html')

def contact(request):

	return render(request,'contact.html')

def logout(request):
	del request.session['username']
	auth.logout(request)
	return render(request,'myhome.html')
	
def savetrip(request):
	try:
		if request.session['username']:
			place=request.POST.get('places','')
			category = request.POST.get('category','')
			city = request.POST.get('city','')
			start_save = request.POST.get('start','')
			end_save = request.POST.get('end','')
			radius = request.POST.get('radius','')
			packdays = request.POST.get('packdays','')
			pname = request.POST.get('pname','').split(',')
			paddress = request.POST.get('paddress','').split(',')
			pcategory = request.POST.get('pcategory','').split(',')
			pdistance = request.POST.get('pdistance','').split(',')
			#print(places)
			#print(pname)
			#print(pname[0][1])
			uname = request.session['username']
			print(len(pname))
			#del request.session['start']
			#del request.session['end']
			
			for i in range(0,len(pdistance)):
				a = pname[i]
				b = pdistance[i]
				c = paddress[i]
				d = pcategory[i]
				s = places(username=uname,city =city ,pack_days = int(packdays),start_date=start_save,end_date=end_save,place_name=a,place_address=c,place_distance=b,place_category=d)
				s.save()
			t = trip_details(radius=int(radius),username=uname,trip=place,city=city,pack_days=int(packdays),start_date=start_save,end_date=end_save,category=category)
			t.save()
			
			return render(request,'myhome.html')	
		else:
			return render(request,'login.html')
			
	except(AttributeError,KeyError):
		context={}
		return HttpResponseRedirect('/planning/login/',context)		
# def viewitin(request):
	# city = request.POST.get('city','')
	# start1 = request.POST.get('start','')
	# end1 = request.POST.get('end','')
	# print(start1,end1)
	# packdays = request.POST.get('packdays','')
	# format_str = '%B %d, %Y'
	# uname=request.session['username']
	# start = datetime.datetime.strptime(start1,format_str).strftime('%Y-%m-%d')
	# end = datetime.datetime.strptime(end1,format_str).strftime('%Y-%m-%d')
	# print(start,end)
	# ob = places.objects.filter(username=uname,start_date=start,end_date=end,city =city ,pack_days=packdays).values()
	# return render(request,'map_page.html',{ 'object' : ob,'pack_days':packdays,'city':city})
	
def myaccount(request):
	if request.session['username']:
		uname=request.session['username']
		data = users_details.objects.filter(username=uname).values()
		for obj in data.values():
			fname = obj['first_name']
			lname= obj['last_name']
			password = obj['password']
			email = obj['email']
			mobile = obj['mo_no']
		return render(request,'myaccount.html',{'uname':uname,'fname':fname,'lname':lname,'email':email,'password':password,'mobile':mobile})
	else:
		return render(request,'login.html')
		
def update(request):
	cuname = request.POST.get('uname', '')
	uname= request.session['username']
	pas = request.POST.get('password', '')
	
	fnam=request.POST.get('fname','')
	lnam = request.POST.get('lname', '')
	
	emai = request.POST.get('email', '')
	
	mob = request.POST.get('mobile', '')
	
	users_details.objects.filter(username=uname).update(username=cuname,password=pas,first_name=fnam,last_name=lnam,email=emai,mo_no=mob)
	request.session['username']=cuname
	context ={}
	return HttpResponseRedirect('/planning/myaccount/',context)
	
'''def myview(request):
    results = request.POST.get('gettrip','')
	return render_to_pdf('map_page.html',{'pagesize':'A4','mylist': results,})
'''

# def get(self, request, *args, **kwargs):
        
        # getting the template
    # pdf = render_to_pdf('map_page.html')
         
         # rendering the template
    # return HttpResponse(pdf, content_type='application/pdf')	
	
def viewitin(request):
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
		location_name = request.POST.get('city','')
		start = request.POST.get('start','')
		activitypreferences = request.POST.get('category','')
		location_radius = int(request.POST.get('radius',''))
		#fstart = datetime.datetime.strptime(start, "%Y-%m-%d").date()
		format_str = '%B %d, %Y'
		trip_start = datetime.datetime.strptime(start,format_str).date()
		#print(datetime_obj.date())	
		
		end = request.POST.get('end','')
		trip_end = datetime.datetime.strptime(end,format_str).date()
		global trip_start1
		global trip_end1
		trip_start1 = datetime.datetime.strptime(start,format_str).strftime('%Y-%m-%d')
		trip_end1 = datetime.datetime.strptime(end,format_str).strftime('%Y-%m-%d')
		
		
		#request.session['start'] = trip_start
		#request.session['end'] = trip_end
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
		global pack_days
		pack_days = ((trip_end - trip_start) + timedelta(0,86400)).days # 1 divas add karo expicitly
		print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',type(pack_days))
		
		travel_time = 30*60 #assuming for now, 30 minutes to reach from one place to another
		end_time=start_time
		rest_time = datetime.datetime(100,1,1,21,00,00)
		
		#setup for the foursquare API
		client_id = '4TJZYOSVJ5BGIXANW5K3X4QMRNX25CWDD0TS4ZRBTELHF2MC'
		client_secret = 'UM53TTVUJYBV42AOCLECG2GSRKNAJSKGJXSF0AQZNLPPTRVP'
		version = '20120610'
		limit = 100

		category='4bf58dd8d48988d181941735'
		
		print('Enter radius : ',end = '')
		
		if activitypreferences == "monument" :
			category='4bf58dd8d48988d12d941735'
		elif activitypreferences == "culture":
			category = '52e81612bcbc57f1066b7a32'
		elif activitypreferences == "adventure":
			category = '4eb1d4d54b900d56c88a45fc'
		elif activitypreferences == "spritual":
			category = '4bf58dd8d48988d131941735'
		elif activitypreferences == "professional":
			category = '4d4b7105d754a06375d81259'
		elif activitypreferences == "mountain":
			category = '4eb1d4d54b900d56c88a45fc'
		elif activitypreferences == "beach":
			category = '4bf58dd8d48988d1e2941735'
		elif activitypreferences == "museum":
			category = '4bf58dd8d48988d181941735'

			
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
		pname= []
		paddress=[]
		pcategory=[]
		pdistance=[]
		for place in results['response']['groups'][0]['items']:
			try:
			
				
				if curr_day <= pack_days:
					
					global mainobject
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
            				
					pname.append(mainobject.p_name)
					paddress.append(mainobject.p_address)
					pcategory.append(mainobject.p_categorytype)
					pdistance.append(mainobject.p_distance)
					
				
					URL = "https://www.google.com/search?q={}".format(
						place['venue']['name']
					)
					print(URL)
					# cont = requests.get(URL).content 
					# soup = BeautifulSoup(cont, 'html.parser')
					# result=soup.find_all("span",attrs={"class":"oqSTJd"})
					# print("Rating of ", place['venue']['name'] , " is ",result[0].text)
					# mainobject.p_ratings = result[0].text    

					if( (end_time + datetime.timedelta(0,travel_time)).time() >= rest_time.time() ):
						print("TIME TO REST FOR TODAY :) See ya tomorrow morning at 9 AM. Till then Good Night!")
						print("*********** DAY ",curr_day," ENDS *****************")
						curr_day = curr_day + 1
						print("Current day : ",curr_day)
						start_time = datetime.datetime(2020,1,26,9,00,00)
						end_time = start_time
					else:
						end_time = end_time + datetime.timedelta(0,travel_time)
					
					
					urldetails = 'https://api.foursquare.com/v2/venues/'+place['venue']['id']+'?client_id={}&client_secret={}&v={}'.format(
					client_id, 
					client_secret, 
					version
					
					)

					#print("URL GOT: ",urldetails)

					
					dets = requests.get(urldetails).json()
					#temp_a = json.dumps(dets)
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
					for test in dets['response']['venue']['photos']['groups'][0]['items']:
						links.append(test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix'])
						mainobject.p_imageURL = test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix']
					
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
					# cont = requests.get(URL).content 
					# soup = BeautifulSoup(cont, 'html.parser')
					# result=soup.find_all("span",attrs={"class":"oqSTJd"})
					# print("Rating of ", place['venue']['name'] , " is ",result[0].text)
					# mainobject.p_ratings = result[0].text    

					
					
					urldetails = 'https://api.foursquare.com/v2/venues/'+place['venue']['id']+'?client_id={}&client_secret={}&v={}'.format(
					client_id, 
					client_secret, 
					version
					
					)

					#print("URL GOT: ",urldetails)

					
					dets = requests.get(urldetails).json()
					#temp_a = json.dumps(dets)
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
					for test in dets['response']['venue']['photos']['groups'][0]['items']:
						links.append(test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix'])
						mainobject.p_imageURL = test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix']
					
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
				#main_list.append(mainobject)
				pass
		
		global OptimizedItinerary
		print("hii1")
		# if __name__ == "__main__": 
  
			
		s = 0
		print("hii2")
		#OptimizedItinerary,min_distance = travellingSalesmanProblem(main_list, s)



		# print("OptimizedItinerary has distance : ",min_distance)
		# for place in OptimizedItinerary:
			# print(place.p_name)
		# print("--- DELETION ---")
		# flag = 0
		# while( flag != 999 ):
				
			# flag = int(input("Enter index of place to delete : enter 999 to exit "))

			# if flag != 999:
				# del OptimizedItinerary[flag]
				# OptimizedItinerary,min_distance = travellingSalesmanProblem(OptimizedItinerary, s)
			# for name in OptimizedItinerary:
				# print("After Deleting  : ",name.p_name," Distance : ",min_distance)

			# print('******************************************************************************************')
	
		#print(main_list)
		
		
		
		#####################################CODE FOR MAKING OptimizedItinerary FOR DIFFERENT DAYS#############################################
			
			
		
		split_list = []
			
		split_index = 0
		for i in range(pack_days):
			split_list.append(split_index + 5)
			split_index = split_index + 5
			
			
		splited_optimizedItinenary = [main_list[i : j] for i, j in zip([0] + split_list, split_list + [None])] 
		
		#print(str(splited_optimizedItinenary))
		
		OptimizedItineraryWithSplited = []
		for RandomItinenary in splited_optimizedItinenary:
			if len(RandomItinenary) >= 3:
				Itinenary,min_distance = travellingSalesmanProblem(RandomItinenary,0)
				OptimizedItineraryWithSplited.append(Itinenary)

		OptimizedItinerary = itertools.chain.from_iterable(OptimizedItineraryWithSplited)
		
	
		#main_list = OptimizedItinerary
		#######################################################################################################################################
		
		global istart
		istart = request.POST.get('startdate','')
		
		print(type(istart))
		return render(request,"map_page.html",{'pname':pname,'paddress':paddress,'pdistance':pdistance,'pcategory':pcategory,'objects': e ,'objs':results['response']['groups'][0]['items'],'city':location_name,'listabc':zip(links,start,end,rating),'istart':istart,'start':trip_start1,'end':trip_end1,'pack_days':pack_days,'pack_night':pack_night,'mainlist':main_list,'suggestionList' : SuggestionList,'category':activitypreferences})
	
def tripmap(request):
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
		location_name = request.POST.get('city','')
		startmap = request.POST.get('start','')
		activitypreferences = request.POST.get('category','')
		
		#fstart = datetime.datetime.strptime(start, "%Y-%m-%d").date()
		format_str = '%Y-%m-%d'
		trip_start = datetime.datetime.strptime(startmap,format_str).date()
		#print(datetime_obj.date())	
		
		endmap = request.POST.get('end','')
		trip_end = datetime.datetime.strptime(endmap,format_str).date()
		trip_start1 = datetime.datetime.strptime(startmap,format_str).strftime('%Y-%m-%d')
		trip_end1 = datetime.datetime.strptime(endmap,format_str).strftime('%Y-%m-%d')
		
		
		print(trip_start1,trip_end1)
		#request.session['start'] = trip_start
		#request.session['end'] = trip_end
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
		global pack_days
		pack_days = ((trip_end - trip_start) + timedelta(0,86400)).days # 1 divas add karo expicitly
		print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',type(pack_days))
		
		travel_time = 30*60 #assuming for now, 30 minutes to reach from one place to another
		end_time=start_time
		rest_time = datetime.datetime(100,1,1,21,00,00)
		
		#setup for the foursquare API
		client_id = 'M2QVKFEINCIFSIVH1OCONVATMWRPQNWTAPX5Q42VN3BDRMB5'
		client_secret = 'LUU5AZWGRJIMVDTVSP3UQBN50TC0YHS5XZ44NHSXXM5KWRRQ'
		version = '20120610'
		limit = 100

		category='4bf58dd8d48988d181941735'
		
		print('Enter radius : ',end = '')
		location_radius = int(request.POST.get('radius',''))
		if activitypreferences == "monument" :
			category='4bf58dd8d48988d12d941735'
		elif activitypreferences == "culture":
			category = '52e81612bcbc57f1066b7a32'
		elif activitypreferences == "adventure":
			category = '4eb1d4d54b900d56c88a45fc'
		elif activitypreferences == "spritual":
			category = '4bf58dd8d48988d131941735'
		elif activitypreferences == "professional":
			category = '4d4b7105d754a06375d81259'
		elif activitypreferences == "mountain":
			category = '4eb1d4d54b900d56c88a45fc'
		elif activitypreferences == "beach":
			category = '4bf58dd8d48988d1e2941735'
		elif activitypreferences == "museum":
			category = '4bf58dd8d48988d181941735'

			
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
		pname= []
		paddress=[]
		pcategory=[]
		pdistance=[]
		for place in results['response']['groups'][0]['items']:
			try:
			
				
				if curr_day <= pack_days:
					
					global mainobject
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
            				
					pname.append(mainobject.p_name)
					paddress.append(mainobject.p_address)
					pcategory.append(mainobject.p_categorytype)
					pdistance.append(mainobject.p_distance)
					
				
					URL = "https://www.google.com/search?q={}".format(
						place['venue']['name']
					)
					print(URL)
					# cont = requests.get(URL).content 
					# soup = BeautifulSoup(cont, 'html.parser')
					# result=soup.find_all("span",attrs={"class":"oqSTJd"})
					# print("Rating of ", place['venue']['name'] , " is ",result[0].text)
					# mainobject.p_ratings = result[0].text    

					if( (end_time + datetime.timedelta(0,travel_time)).time() >= rest_time.time() ):
						print("TIME TO REST FOR TODAY :) See ya tomorrow morning at 9 AM. Till then Good Night!")
						print("*********** DAY ",curr_day," ENDS *****************")
						curr_day = curr_day + 1
						print("Current day : ",curr_day)
						start_time = datetime.datetime(2020,1,26,9,00,00)
						end_time = start_time
					else:
						end_time = end_time + datetime.timedelta(0,travel_time)
					
					
					urldetails = 'https://api.foursquare.com/v2/venues/'+place['venue']['id']+'?client_id={}&client_secret={}&v={}'.format(
					client_id, 
					client_secret, 
					version
					
					)

					#print("URL GOT: ",urldetails)

					
					dets = requests.get(urldetails).json()
					#temp_a = json.dumps(dets)
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
					for test in dets['response']['venue']['photos']['groups'][0]['items']:
						links.append(test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix'])
						mainobject.p_imageURL = test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix']
					
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
					# cont = requests.get(URL).content 
					# soup = BeautifulSoup(cont, 'html.parser')
					# result=soup.find_all("span",attrs={"class":"oqSTJd"})
					# print("Rating of ", place['venue']['name'] , " is ",result[0].text)
					# mainobject.p_ratings = result[0].text    

					
					
					urldetails = 'https://api.foursquare.com/v2/venues/'+place['venue']['id']+'?client_id={}&client_secret={}&v={}'.format(
					client_id, 
					client_secret, 
					version
					
					)

					#print("URL GOT: ",urldetails)

					
					dets = requests.get(urldetails).json()
					#temp_a = json.dumps(dets)
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
					for test in dets['response']['venue']['photos']['groups'][0]['items']:
						links.append(test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix'])
						mainobject.p_imageURL = test['prefix']+str(test['width'])+'x'+str(test['height'])+test['suffix']
					
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
				#main_list.append(mainobject)
				pass
		
		global OptimizedItinerary
		print("hii1")
		# if __name__ == "__main__": 
  
			
		s = 0
		print("hii2")
		#OptimizedItinerary,min_distance = travellingSalesmanProblem(main_list, s)



		# print("OptimizedItinerary has distance : ",min_distance)
		# for place in OptimizedItinerary:
			# print(place.p_name)
		# print("--- DELETION ---")
		# flag = 0
		# while( flag != 999 ):
				
			# flag = int(input("Enter index of place to delete : enter 999 to exit "))

			# if flag != 999:
				# del OptimizedItinerary[flag]
				# OptimizedItinerary,min_distance = travellingSalesmanProblem(OptimizedItinerary, s)
			# for name in OptimizedItinerary:
				# print("After Deleting  : ",name.p_name," Distance : ",min_distance)

			# print('******************************************************************************************')
	
		#print(main_list)
		
		
		
		#####################################CODE FOR MAKING OptimizedItinerary FOR DIFFERENT DAYS#############################################
			
			
		
		split_list = []
			
		split_index = 0
		for i in range(pack_days):
			split_list.append(split_index + 5)
			split_index = split_index + 5
			
			
		splited_optimizedItinenary = [main_list[i : j] for i, j in zip([0] + split_list, split_list + [None])] 
		
		#print(str(splited_optimizedItinenary))
		
		OptimizedItineraryWithSplited = []
		for RandomItinenary in splited_optimizedItinenary:
			if len(RandomItinenary) >= 3:
				Itinenary,min_distance = travellingSalesmanProblem(RandomItinenary,0)
				OptimizedItineraryWithSplited.append(Itinenary)

		OptimizedItinerary = itertools.chain.from_iterable(OptimizedItineraryWithSplited)
		
	
		#main_list = OptimizedItinerary
		#######################################################################################################################################
		
		global istart
		istart = request.POST.get('startdate','')
		
		print(type(istart))
		return render(request,"map_page.html",{'radius':location_radius,'pname':pname,'paddress':paddress,'pdistance':pdistance,'pcategory':pcategory,'objects': e ,'objs':results['response']['groups'][0]['items'],'city':location_name,'listabc':zip(links,start,end,rating),'istart':istart,'start':trip_start1,'end':trip_end1,'pack_days':pack_days,'pack_night':pack_night,'mainlist':main_list,'suggestionList' : SuggestionList,'category':activitypreferences})
		
