from django.db import models
from jsonfield import JSONField
#from djangotoolbox import fields
#from django.db.models.fields import DurationField

# Create your models here.
class users_details(models.Model):
	username = models.CharField(max_length=20,unique=True)
	password = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	mo_no = models.IntegerField()
	
class trip_details(models.Model):
	username = models.CharField(max_length=20)
	city = models.CharField(max_length=30,null=True)
	pack_days = models.IntegerField()
	trip = JSONField()
	start_date = models.DateField()		
	end_date = models.DateField()
	category= models.CharField(max_length=20)
	radius = models.IntegerField()
	
class places(models.Model):
	username = models.CharField(max_length=20)
	city = models.CharField(max_length=30,null=True)
	pack_days = models.IntegerField()
	start_date = models.DateField()		
	end_date = models.DateField()
	place_name = models.CharField(max_length=200)
	place_address = models.CharField(max_length=200)
	place_category = models.CharField(max_length=20)
	#place_ratings = models.DecimalField(null=True,max_digits=2, decimal_places=1)
	place_distance = models.CharField(max_length=10)