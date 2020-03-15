from django.db import models

# Create your models here.
class user_details(models.Model):
	username = models.CharField(primary_key=True,max_length=20)
	password = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	mo_no = models.IntegerField()