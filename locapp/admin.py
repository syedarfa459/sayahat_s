from django.contrib import admin
from .models import Destination,Tourist,DestinationCityDetails, DestinationMetaDetails,PlaceRatings
# Register your models here.
admin.site.register(Destination)
admin.site.register(Tourist)
admin.site.register(DestinationCityDetails)
admin.site.register(DestinationMetaDetails)
admin.site.register(PlaceRatings)

