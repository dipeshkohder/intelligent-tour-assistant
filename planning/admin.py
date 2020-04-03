from django.contrib import admin
from .models import places,users_details,trip_details
# Register your models here.

admin.site.register(users_details)
admin.site.register(trip_details)
admin.site.register(places)